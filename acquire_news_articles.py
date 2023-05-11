from requests import get
from bs4 import BeautifulSoup
import os
import requests
import itertools
import json
import pickle
import pandas as pd

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

def get_sports_df():
    sports_list = get_inshorts_dicts('https://inshorts.com/en/read/sports', 'sports')
    sports_df = pd.DataFrame(sports_list)
    return sports_df

def get_business_df():
    business_list = get_inshorts_dicts('https://inshorts.com/en/read/business', 'business')
    business_df = pd.DataFrame(business_list)
    return business_df

def get_technology_df():
    technology_list = get_inshorts_dicts('https://inshorts.com/en/read/technology', 'technology')
    technology_df = pd.DataFrame(technology_list)
    return technology_df

def get_entertainment_df():
    entertainment_list = get_inshorts_dicts('https://inshorts.com/en/read/entertainment', 'entertainment')
    entertainment_df = pd.DataFrame(entertainment_list)
    return entertainment_df

def get_inshorts_df():
    sports_df = get_sports_df()
    business_df = get_business_df()
    entertainment_df = get_entertainment_df()
    technology_df = get_technology_df()

    df = pd.concat([sports_df, business_df, technology_df, entertainment_df], axis = 0)

    return df

def get_inshorts_text():
    # if we already have the data, read it locally
    if os.path.exists('inshorts.txt'):
        with open('inshorts.txt') as f:
            return f.read()
    
    else:
        df = get_inshorts_df()
        with open('inshorts.txt', 'w') as f:
            f.write(df.text)
            return f.read()