# My Library
This is a demonstration of Google's Books API. This is a simple backend designed
to allow a user to interact with the API's search finctionality and browse for 
books by keyword.

## Getting Started

First, run the development server:

```
uvicorn app:app --host 0.0.0.0 --port 80
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Design
The design of this system is simple and straightforward. `App.py` houses all of
the code. The bulk of the code is boilerplate material to get our endpoint up and 
running. The remainder is the FastAPI endpoint exposed at `/results/{keywords}`
and a simple but extensible url builder designed to neatly handle the params.
