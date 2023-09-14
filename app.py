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

load_dotenv()

BOOKS_API_KEY = os.getenv('BOOKS_API_KEY')

app = FastAPI()

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
    return base + urllib.parse.urlencode({
        "q": keywords.replace(" ", "+")
        })

@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}

@app.get("/search/{keywords}")
async def search(keywords: str) -> dict:
    params = {"key":BOOKS_API_KEY}
    r = requests.get(search_url_builder(keywords), params=params)
    return r