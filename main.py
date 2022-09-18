from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

import secrets
import validators

from database import SessionLocal, engine

import models,schemas

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def raise_bad_request(message):
    raise HTTPException(status_code=400,detail=message)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url
    
# @app.post("/url")
# def create_url(url: schemas.URLBase):
#     if not validators.url(url.target_url):
#         raise_bad_request(message="Invalid URL provided")

#     return f"TODO: create database entry for: {url.target_url}"
@app.get('/')
def root():
    return {"ping":"pong"}