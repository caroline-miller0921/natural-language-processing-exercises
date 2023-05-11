from requests import get
from bs4 import BeautifulSoup
import os
import requests
import pandas as pd

def get_blog_dicts():

    url = 'https://codeup.com/data-science/math-in-data-science/'
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text)
    article = soup.find('div', id='main-content')

    article_links = soup.find_all('a', class_="wp-block-latest-posts__post-title")

    link_list = []
    for item in article_links:
        link_list.append(item['href'])

    article_list = []
    for link in link_list:
        url = link
        headers = {'User-Agent': 'Codeup Data Science'} 
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        blog_title = soup.find('h1').contents
        blog_content = soup.find('div', class_='entry-content').find_all('p')
    
        article_dict = (
            {
            'title': blog_title[0],
            'content': [f'{blog_content}']
         }
         )
        
        article_list.append(article_dict)

    return article_list


def get_blog_df():
    article_list = get_blog_dicts()
    df = pd.DataFrame(article_list)
    return df

def get_blog_text():
    # if we already have the data, read it locally
    if os.path.exists('codeup_blogs.txt'):
        with open('codeup_blogs.txt') as f:
            return f.read()
    
    else:
        df = get_blog_df()
        with open('codeup_blogs.txt', 'w') as f:
            f.write(df.to_string(header=False, index=False))
            return f.read()