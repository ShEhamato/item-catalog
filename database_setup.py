import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship ,  backref
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id= Column(Integer, primary_key= True)
    name=Column(String(80), nullable=False)
    email=Column(String(80), nullable=False)
    picture = Column(String(250))

class Catalog(Base):
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key =True)
    name = Column(String(250) , nullable = False)
    description = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    
    

class CatalogItem(Base):
    __tablename__ = 'catalog_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    duration = Column(String(250))
    catalog_id = Column(Integer, ForeignKey('catalog.id'))
    catalog = relationship(Catalog, backref=backref("items", cascade="all,delete"))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    


engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)