import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

import acquire as a
import os


def lower(some_string):
    some_string = some_string.lower()
    return some_string

def normalize(some_string):
    some_string = unicodedata.normalize('NFKD', some_string).encode('ascii', 'ignore').decode('utf-8')
    some_string = re.sub(r'[^a-zA-Z0-9\'\s]', '', some_string)
    return some_string

def basic_clean(some_string):
    some_string = lower(some_string)
    some_string = normalize(some_string)
    return some_string

def tokenize(some_string):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(some_string, return_str=True)

def lemmatize(some_string):
    lemmatizer = nltk.WordNetLemmatizer()
    return ' '.join(
        [lemmatizer.lemmatize(word) for word in some_string.split()])

def stem(some_string):
    stemmer = nltk.porter.PorterStemmer()
    return ' '.join(
        [stemmer.stem(word) for word in some_string.split()])

def remove_stopwords(some_string, extra_words=[], keep_words=[]):
    stopwords_custom = set(stopwords.words('english')) - \
    set(keep_words)
    stopwords_custom = list(stopwords_custom.union(extra_words))
    return ' '.join([word for word in some_string.split()
                     if word not in stopwords_custom])

def transform_data(df, extra_words=[], keep_words=[]):
    df = df.rename(columns={'content': 'original'})
    df['clean'] = df['original'].apply(basic_clean).apply(
        tokenize).apply(remove_stopwords)
    df['stemmed'] = df['clean'].apply(stem)
    df['lemmatized'] = df['stemmed'].apply(lemmatize)
    return df

def prepare_news_df():
    news_df = a.get_inshorts_df()
    news_cleaned = transform_data(news_df)
    return news_cleaned

def prepare_codeup_df():
    codeup_df = a.get_blog_df()
    codeup_cleaned = transform_data(codeup_df)
    return codeup_cleaned
