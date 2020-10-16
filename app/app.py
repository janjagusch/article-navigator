import datetime
import logging

import connexion
from connexion import NoContent

SUPERMARKETS = {
    0: {
        "id": 0,
        "name": "Test Supermarket",
        "sections": {
            0: {"id": 0, "type": "entrance", "location": {"x": 0, "y": 0}},
            1: {"id": 1, "type": "isle", "location": {"x": 0, "y": 1}},
            2: {"id": 2, "type": "isle", "location": {"x": 1, "y": 1}},
            3: {"id": 3, "type": "checkout", "location": {"x": 1, "y": 0}},
        },
    }
}

ARTICLES = {
    0: {
        "id": 0,
        "name": "Nutella",
        "imageUrl": "https://commons.wikimedia.org/wiki/File:Nutella_ak.jpg#/media/File:Nutella_ak.jpg",
    }
}

SUPERMARKET_ARTICLE_SECTIONS = {0: {0: 0}}


def _format_supermarket(supermarket):
    return {
        "id": supermarket["id"],
        "name": supermarket["name"],
        "sections": list(supermarket["sections"].values()),
    }


def get_articles():
    return list(ARTICLES.values())


def get_article(article_id):
    return ARTICLES[article_id]


def get_supermarkets():
    return [_format_supermarket(supermarket) for supermarket in SUPERMARKETS.values()]


def get_supermarket(supermarket_id):
    return _format_supermarket(SUPERMARKETS[supermarket_id])


def get_supermarket_articles(supermarket_id):
    return [
        ARTICLES[article_id]
        for article_id in SUPERMARKET_ARTICLE_SECTIONS[supermarket_id].keys()
    ]


def get_supermarket_section(supermarket_id, section_id):
    return SUPERMARKETS[supermarket_id]["sections"][section_id]


def get_supermarket_article_section(supermarket_id, article_id):
    return SUPERMARKETS[supermarket_id]["sections"][
        SUPERMARKET_ARTICLE_SECTIONS[supermarket_id][article_id]
    ]


def get_supermarket_shortest_path(supermarket_id, from_section, to_section):
    return [
        SUPERMARKETS[supermarket_id]["sections"][section_id]
        for section_id in [from_section, to_section]
    ]


def get_supermarket_shortest_tour(supermarket_id, visit_sections):
    return [
        SUPERMARKETS[supermarket_id]["sections"][section_id]
        for section_id in visit_sections
    ]


logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api("app.yml")
application = app.app

if __name__ == "__main__":
    app.run(port=8080, server="gevent", debug=True)
