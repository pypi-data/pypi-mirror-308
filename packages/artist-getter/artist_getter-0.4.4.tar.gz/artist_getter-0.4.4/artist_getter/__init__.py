import json
import urllib
from io import BytesIO

import pycurl
import requests
from Levenshtein import distance
from wikidata.client import Client
from functools import cache


# returns entire set of data from given ulan
def get_getty_artist_data(ulan):
    url = "http://vocab.getty.edu/ulan/%s.json" % ulan
    result = requests.get(url)
    data = json.loads(result.content)
    return data


# returns artist name from given ulan
@cache
def get_getty_artist_name(ulan):
    return get_getty_artist_data(ulan)['_label']


# returns artist sex from given ulan
@cache
def get_getty_artist_sex(ulan):
    classifications = get_getty_artist_data(ulan)["classified_as"]
    for classification in classifications:
        if classification["_label"] in ["male", "female"]:
            return classification["_label"]
    return None

# returns artist birth year given ulan
@cache
def get_getty_artist_birth_year(ulan):
    timespan = get_getty_artist_data(ulan)["born"]["timespan"]["begin_of_the_begin"][:4]
    return int(timespan)

# returns a list of ulans and their relationship to the provided ulan
@cache
def get_getty_relationship(ulan):
    data = get_getty_artist_data(ulan)
    relationships = list()
    ulan_relationships = data['la:related_from_by']

    for relationship in ulan_relationships:
        if relationship['type'] == "la:Relationship" and 'id' in relationship['la:relates_to'] and relationship[
            'classified_as']:
            for c in relationship['classified_as']:
                if type(c) is dict:
                    relationship_display = c['_label'].split('-')[0].strip()
                    object_ulan = relationship['la:relates_to']['id'].split('/ulan/')[1]

                    relationship = {'relationship_type': relationship_display, 'object_ulan': object_ulan}
                    relationships.append(relationship)
    return relationships


# returns a best guess ulan based on artist's name (formatted: Lastname, Firstname) and some basic info
@cache
def get_getty_ulan(artist):
    # artists with apostrophies in their names need escaping
    if (artist.find("'") != -1):
        artist = artist.replace("'", "\\\'")

    # get rid of any whitespace and encode to utf8
    artist = artist.replace('\n', ' ').replace('\r', '')
    artist_encoded = urllib.parse.quote(artist.encode('utf8'));

    # sparql query that could use some refining
    getty_url = 'http://vocab.getty.edu/sparql.json?query=select+%3FSubject+%3FTerm+%3FParents+%3FScopeNote+%7B%0D%0A++%3FSubject+a+skos%3AConcept%3B+luc%3Aterm+%27+%22' + artist_encoded + '%22+%27%3B%0D%0A+++++gvp%3AprefLabelGVP+%5Bxl%3AliteralForm+%3FTerm%5D.%0D%0A++optional+%7B%3FSubject+gvp%3AparentStringAbbrev+%3FParents%7D%0D%0A++optional+%7B%3FSubject+skos%3AscopeNote+%5Bdct%3Alanguage+gvp_lang%3Aen%3B+rdf%3Avalue+%3FScopeNote%5D%7D%7D&_implicit=false&implicit=true&_equivalent=false&_form=%2Fsparql'

    # curl is required due to requests package tripping on some character strings
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, getty_url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    result = buffer.getvalue()
    data = json.loads(result)
    bindings = data['results']['bindings']

    ulans = list()
    if (bindings):
        for b in bindings:
            b_subject = b['Subject']['type']
            if (b_subject == 'uri'):
                b_uri = b['Subject']['value']
                uri_parts = b_uri.split('/ulan/')
                if (len(uri_parts) == 2):
                    ulan = uri_parts[1]
                else:
                    # these URIs tend to lead to other vocabularies (TGN, AAT etc)
                    continue

            b_type = b['Parents']['value']
            b_term = b['Term']['value']

            # prepare apostrophies for insertion into psql db, TO DO: move this to the view logic
            b_term = b_term.replace("'", "''")

            if ('ScopeNote' in b):
                b_scopenote = b['ScopeNote']['value']
                b_scopenote = b_scopenote.replace("'", "''")
            else:
                b_scopenote = None

            getty_data = {'ulan': ulan, 'scopenote': b_scopenote, 'type': b_type, 'term': b_term}
            ulans.append(getty_data)

    # for queries with multiple results apply some filtering:
    # levenshtein distance
    # todo: query getty for pseudonyms of artist? filter on birth year?
    if len(ulans) > 1:
        d = 100  # declare high value as default and take record with lowest d
        accepted_ulan = None
        for ulan in ulans:
            if ulan['ulan'] is False:
                continue

            dist = distance(artist, ulan['term'])
            if dist < d:
                # set returned record to lowest levenshtein distance
                d = dist

                # don't accept distances that are too high
                if d < 3:
                    accepted_ulan = ulan
                else:
                    continue

            elif dist == d:
                # TO DO more refining against birthdate or pseudonyms
                # for now don't send anything back if results are ambiguous
                accepted_ulan = None

        if accepted_ulan is None:
            # return empty list of no definitive ulan was found
            ulans = list()
        else:
            ulans = [accepted_ulan]

    return ulans


def __get_wiki_entity(id):
    client = Client()
    return client.get(id, load=True)

# returns entire set of data from given wiki id
@cache
def get_wiki_artist_data(id):
    return __get_wiki_entity(id)


# returns artist name from given wiki id
@cache
def get_wiki_artist_name(id) -> str:
    return get_wiki_artist_data(id).label.texts['en']


@cache
def get_wiki_artist_sex(id) -> str:
    artist = get_wiki_artist_data(id)
    P21_entity = __get_wiki_entity('P21') # 'sex or gender'
    try:
        return artist.get(P21_entity).label.texts['en-gb']
    except Exception:
        return None


@cache
def get_wiki_artist_birth_year(id) -> str:
    artist = get_wiki_artist_data(id)
    P569_entity = __get_wiki_entity('P569') # 'date of birth'
    try:
        return artist.get(P569_entity).year
    except Exception:
        return None


@cache
def get_wiki_artist_nationality(id) -> str:
    artist = get_wiki_artist_data(id)
    P27_entity = __get_wiki_entity('P27') # 'country of citizenship'
    try:
        return artist.get(P27_entity).label.texts['en']
    except Exception:
        return None
