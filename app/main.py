from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .db import Base, engine
from . import models, schemas
from .deps import get_db
from .security import hash_password

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to Ferrum Webhook Relay!"}

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = models.User(
        email = user.email,
        password_hash = hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post("/webhooks", response_model=schemas.WebhookOut)
def create_webhook(
    webhook: schemas.WebhookCreate,
    db: Session = Depends(get_db)
):
    db_webhook = models.Webhook(
        user_id=1,  # TEMP: we don’t have auth yet
        url=webhook.url,
        event_type=webhook.event_type
    )

    db.add(db_webhook)
    db.commit()
    db.refresh(db_webhook)

    return db_webhook


@app.get("/webhooks", response_model=list[schemas.WebhookOut])
def list_webhooks(db: Session = Depends(get_db)):
    return db.query(models.Webhook).all()

@app.post("/events")
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db)
):
    db_event = models.Event(
        user_id=1,
        payload=event.payload
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return {"event_id": db_event.id}