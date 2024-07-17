from sqlalchemy import Column, Integer, String
from requests.database import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, unique=True)
    views = Column(Integer, default=0)