import collections
import datetime
import logging
import pickle

import connexion
import yaml
from connexion import NoContent

from api.validators import RequestBodyValidator

with open("supermarkets.pkl", "rb") as file_pointer:
    SUPERMARKETS = pickle.load(file_pointer)

with open("articles.yml", "r") as file_pointer:
    ARTICLES = {article["id"]: article for article in yaml.safe_load(file_pointer)}

with open("supermarket_article_sections.yml", "r") as file_pointer:
    SUPERMARKET_ARTICLE_SECTIONS = yaml.safe_load(file_pointer)


def health_check():
    """ Check whether the API is healthy. """
    return NoContent, 204


def get_articles():
    return list(ARTICLES.values())


def get_article(article_id):
    return ARTICLES[article_id]


def get_supermarkets():
    return [supermarket.to_dict() for supermarket in SUPERMARKETS.values()]


def get_supermarket(supermarket_id):
    return SUPERMARKETS[supermarket_id].to_dict()


def get_supermarket_articles(supermarket_id):
    return [
        ARTICLES[article_id]
        for article_id in SUPERMARKET_ARTICLE_SECTIONS[supermarket_id].keys()
    ]


def get_supermarket_section(supermarket_id, section_id):
    return SUPERMARKETS[supermarket_id]._sections[section_id]


def get_supermarket_article_section(supermarket_id, article_id):
    return SUPERMARKETS[supermarket_id]._sections[
        SUPERMARKET_ARTICLE_SECTIONS[supermarket_id][article_id]
    ]


def get_supermarket_shortest_path(supermarket_id, from_section, to_section):
    key = frozenset([from_section, to_section])
    path = SUPERMARKETS[supermarket_id]._path_matrix[key]
    if path[0] != from_section:
        path = path[::-1]
    return list(SUPERMARKETS[supermarket_id]._sections[sec_id] for sec_id in path)


def get_supermarket_shortest_tour(supermarket_id, visit_sections):
    tour = SUPERMARKETS[supermarket_id].calc_tour(visit_sections)
    return list(SUPERMARKETS[supermarket_id]._sections[sec_id] for sec_id in tour)


logging.basicConfig(level=logging.INFO)
app = connexion.App(
    __name__,
    options={"swagger_ui": True},
)

app.add_api(
    "api.yml",
    strict_validation=True,
    validate_responses=True,
    validator_map={"body": RequestBodyValidator},
)
application = app.app

if __name__ == "__main__":
    app.run(port=8080, server="gevent", debug=True)
