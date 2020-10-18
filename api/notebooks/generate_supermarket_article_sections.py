# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: easy-way-api
#     language: python
#     name: easy-way-api
# ---

import sys
sys.path.append("..")

import pickle
import yaml
import random

from api.supermarket import Supermarket

# +
with open("../supermarkets.pkl", "rb") as file_pointer:
    supermarkets = pickle.load(file_pointer)
    
with open("../articles.yml") as file_pointer:
    articles = yaml.safe_load(file_pointer)
# -

supermarket_article_sections = {supermarket._supermarket_id: {article["id"]: random.choice(list(supermarket._sections.keys())) for article in articles} for supermarket in supermarkets.values()}

with open("../supermarket_article_sections.yml", "w") as file_pointer:
    yaml.dump(supermarket_article_sections, file_pointer)
