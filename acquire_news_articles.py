from requests import get
from bs4 import BeautifulSoup
import os
import requests
import itertools
import json
import pickle

def get_inshorts_dicts(url, category): 

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    article_headlines = soup.find_all('span', itemprop="headline")
    article_contents = soup.find_all('div', itemprop='articleBody')

    headline_list = []
    for item in article_headlines:
        headline_list.append(item.contents)
    
    content_list = []
    for item in article_contents:
        content_list.append(item.contents)
    
    article_list = []
    for headline, content in itertools.zip_longest(headline_list, content_list):
        category_dict = (
        {
            'title': headline[0], 
            'content': content[0],
            'category': category
        })
        article_list.append(category_dict)
    
    return article_list

def get_sports_list():
    sports_list = get_inshorts_dicts('https://inshorts.com/en/read/sports', 'sports')
    return sports_list

def get_business_list():
    business_list = get_inshorts_dicts('https://inshorts.com/en/read/business', 'business')
    return business_list

def get_technology_list():
    technology_list = get_inshorts_dicts('https://inshorts.com/en/read/technology', 'technology')
    return technology_list

def get_entertainment_list():
    entertainment_list = get_inshorts_dicts('https://inshorts.com/en/read/entertainment', 'entertainment')
    return entertainment_list

def get_inshorts_list():
    
    sports_list = get_sports_list()
    business_list = get_business_list()
    technology_list = get_technology_list()
    entertainment_list = get_entertainment_list()

    
    inshorts_list = []
    inshorts_list.append(sports_list)
    inshorts_list.append(business_list)
    inshorts_list.append(technology_list)
    inshorts_list.append(entertainment_list)

    return inshorts_list

def get_inshorts_text():
    # if we already have the data, read it locally
    if os.path.exists('inshorts.txt'):
        with open('inshorts.txt') as f:
            return f.read()

    # load the content
    inshorts = get_business_list()

    # save it for next time

    with open('inshorts.txt', 'w') as fout:
        pickle.dump(inshorts, fout)

    return fout