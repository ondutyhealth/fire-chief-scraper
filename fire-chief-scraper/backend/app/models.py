from sqlalchemy import Column, Integer, String
from .database import Base

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    state = Column(String)
    name = Column(String)
    title = Column(String)
    email = Column(String)
    url = Column(String)