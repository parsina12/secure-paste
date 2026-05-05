from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Paste(Base):
    __tablename__ = 'pastes'
    id = Column(Integer, primary_key=True, index=True)
    short_id = Column(String(16), unique=True, index=True)
    iv = Column(String(44))
    ciphertext = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class FilePaste(Base):
    __tablename__ = 'filepastes'
    id = Column(Integer, primary_key=True, index=True)
    short_id = Column(String(16), unique=True, index=True)
    filename = Column(String)
    iv = Column(String(44))
    ciphertext = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
