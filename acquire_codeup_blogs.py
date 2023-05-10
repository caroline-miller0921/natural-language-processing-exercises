from requests import get
from bs4 import BeautifulSoup
import os
import requests

def get_article_text():
    # if we already have the data, read it locally
    if os.path.exists('article.txt'):
        with open('article.txt') as f:
            return f.read()

    # otherwise go fetch the data
    url = 'https://codeup.com/data-science/math-in-data-science/'
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text)
    article = soup.find('div', id='main-content')

    # save it for next time
    with open('article.txt', 'w') as f:
        f.write(article.text)

    return article.text

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

