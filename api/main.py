# api/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api import crud, schemas

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Welcome to the Telegram Analytics API"}

@app.get("/api/reports/top-products", response_model=list[schemas.TopProduct])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_products(db, limit)

@app.get("/api/channels/{channel_name}/activity", response_model=list[schemas.ChannelActivity])
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    return crud.get_channel_activity(db, channel_name)

@app.get("/api/search/messages", response_model=list[schemas.SearchMessage])
def search(query: str, db: Session = Depends(get_db)):
    return crud.search_messages(db, query)
