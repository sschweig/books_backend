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
from dotenv import load_dotenv
#from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

#.env handling
load_dotenv()
BOOKS_API_KEY = os.getenv('BOOKS_API_KEY')

origins = [
    "*",
    "localhost", 
    "localhost:3000", 
    "http://localhost", 
    "http://localhost:3000"
    "https://localhost", 
    "https://localhost:3000",
    "http://0.0.0.0",
    "http://0.0.0.0/results/*",
    "http://localhost:80"
]
middleware = [
    Middleware(CORSMiddleware, allow_origins=origins)
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
async def root() -> dict:
    return {"message": "Hello World"}

@app.get("/results/{keywords}")
def search(keywords):
    params = {"key":BOOKS_API_KEY}
    url = search_url_builder(keywords)
    r = requests.get(url, params=params)
    if r.status_code == 200:
        filtered = [{
            'uid': idx,
            'book_id': el['id'],
            'title': el['volumeInfo'].get('title', ''),
            'authors': el['volumeInfo'].get('authors', []),
            'imagePreview': el['volumeInfo']['imageLinks'].get('smallThumbnail', ''),
            'description': el['searchInfo'].get('textSnippet', '')
            } for idx, el in enumerate(r.json()['items'])]
            
        return {'books': filtered}
    return r.json()