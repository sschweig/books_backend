# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 04:33:33 2023

@author: Steven Schweiger
"""
import os
import requests
import typing
import urllib
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
#from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

#.env handling
load_dotenv()

#Replace me 
BOOKS_API_KEY = os.getenv('BOOKS_API_KEY')
#BOOKS_API_KEY = "API KEY HERE"

LIB_CACHE = []

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]

app = FastAPI(middleware=middleware)


def search_url_builder(keywords: str) -> str:
    """Build URL for search functionality.
    

    Parameters
    ----------
    keywords : String
        String passed to us from the frontend's search functionality. 
        USER-GENERATED, BEWARE.

    Returns
    -------
    String
        Url string complete with query parameters.
        
    Notes
    -----
        TODO: Add advanced filtering as described in
        https://developers.google.com/books/docs/v1/using#PerformingSearch

    """
    base = "https://www.googleapis.com/books/v1/volumes?"
    
    if len(keywords) == 0:
        return base
    
    return base + urllib.parse.urlencode({
        "q": keywords.replace(" ", "+")
        })

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/details/{uid}")
def search(uid):
    return jsonable_encoder(LIB_CACHE[uid])

@app.get("/results/{keywords}")
def search(keywords):
    params = {"key":BOOKS_API_KEY}
    url = search_url_builder(keywords)
    r = requests.get(url, params=params)
    
    if r.status_code == 200:
        LIB_CACHE = r.json()
        filtered = [{
            'uid': idx,
            'book_id': el['id'],
            'title': el['volumeInfo'].get('title', ''),
            'authors': ", ".join(el['volumeInfo'].get('authors', [])),
            'imagePreview': el['volumeInfo'].get('imageLinks', {}).get('smallThumbnail', ''),
            'publishedDate': el['volumeInfo'].get('publishedDate', ''),
            'averageRating': el['volumeInfo'].get('averageRating', 0),
            'ratingsCount': el['volumeInfo'].get('ratingsCount', 0),
            'description': el.get('searchInfo', {}).get('textSnippet', '')
            } for idx, el in enumerate(r.json()['items'])]
            
        return jsonable_encoder(filtered)
    return r.json()