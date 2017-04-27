from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base() 

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    bids = relationship("Bid", backref="item")
    auctioner = Column(Integer, ForeignKey('users.id'), nullable=False)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    bids = relationship("Bid", backref="user")
    auctions = relationship("Item", backref="user")
    
class Bid(Base):
    __tablename__ = "bids"
    id = Column(Integer, primary_key=True)
    
    userid = Column(Integer, ForeignKey('users.id'), nullable=False)
    itemid = Column(Integer, ForeignKey('items.id'), nullable=False)

    price = Column(Float, nullable=False)
    
    
    
    
#user to bid, (one to many)
#item to bid (one to many)
#
    
Base.metadata.create_all(engine)


tony = User(username="thoang", password="whitby")
deepak = User(username="dsurti", password="thinkful")
bill = User(username="bgates", password="microsoft")
session.add_all([tony, deepak, bill])
session.commit()

baseball = Item(name="Baseball", description="ordinary", auctioner=3)
session.add(baseball)
session.commit()

tonybid = Bid(userid=1,itemid=2,price=187.25)
deepakbid = Bid(userid=2, itemid=2, price=300.00)
tonybid2 = Bid(userid=1,itemid=2,price=450)
deepakbid2 = Bid(userid=2, itemid=2, price=999.99)
session.add_all([tonybid,deepakbid,tonybid2,deepakbid2])
session.commit()

##Question: PK ID is generated at record creation.
##Since bids use FKs via the PK ID, do I have to create 1 batch of record, query for PK ID, then create bid?
##Or is there a way to create all these records with 1 session.commit()? the userid and itemid and auctioner,
##I got them from querying AFTER creation of the PK.

session.query(User.username, Bid.price).order_by(Bid.price.desc()).filter(User.id == Bid.userid).first()
