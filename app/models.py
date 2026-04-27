from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .db import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

class Webhook(Base):
    __tablename__ = 'webhooks'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    url = Column(String)
    event_type = Column(String)

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    payload = Column(JSON)
    status = Column(String, default='pending')
    event_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Delivery(Base):
    __tablename__ = 'deliveries'
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    webhook_id = Column(Integer, ForeignKey('webhooks.id'))
    status = Column(String)
    retries = Column(Integer, default=0)
    latency_ms = Column(Integer)
    response_code = Column(Integer)
    attempted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=True)
    next_retry_at = Column(DateTime, nullable=True)
