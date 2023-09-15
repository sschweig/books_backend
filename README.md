# My Library
This is a demonstration of Google's Books API. This is a simple backend designed
to allow a user to interact with the API's search functionality and browse for 
books by keyword.

## Getting Started

First, uncomment line 23 and comment out line 22, then insert your own Books API Key. 
After that, run the development server by executing the following command from the 
same folder as main.py:

```
uvicorn app:app --host 0.0.0.0 --port 80
```

The server will go through a short boot process and then be ready to go. Open 
[http://localhost:80](http://localhost:80) with your browser to see the result.

## Design
The design of this system is simple and straightforward. `App.py` houses all of
the code. The bulk of the code is boilerplate material to get our endpoint up and 
running. The remainder is the FastAPI endpoint exposed at `/results/{keywords}`
and a simple but extensible url builder designed to neatly handle the params.

## TODDO
Extend url builder to handle more advanced query methods.
User management for favoirtes/saved?
