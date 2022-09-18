from email.policy import HTTP
from fastapi import FastAPI, HTTPException
import validators

import schemas

app = FastAPI()

def raise_bad_request(message):
    raise HTTPException(status_code=400,detail=message)


@app.post("/url")
def create_url(url: schemas.URLBase):
    if not validators.url(url.target_url):
        raise_bad_request(message="Invalid URL provided")

    return f"TODO: create database entry for: {url.target_url}"
@app.get('/')
def root():
    return {"ping":"pong"}