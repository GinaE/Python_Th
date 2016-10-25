# tbay.py
# type: "sudo service postgresql start" before starting a session.
# also, to clean the database and create one anew: "dropdb tbay && createdb tbay"

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship


engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

'''
# adding relationships:
# Users should be able to auction multiple items 
# Users should be able to bid on multiple items 
# Multiple users should be able to place a bid on an item
'''

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    # Users should be able to auction multiple items, the items belong to one person with owner_id = users.id
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
   
    # Users should be able to bid on multiple items,   
    bids = relationship("Bid", backref="object")
   
    # Multiple users should be able to place a bid on an item
    

class User(Base):
    __tablename__ = "users"   
    '''
    The user model should contain three columns:
    An integer id, which is the primary key
    A username string, which cannot be null
    A password string, which cannot be null
    '''
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    # Users should be able to auction multiple items
    items = relationship("Item", backref="owner")  
    
    # Users should be able to bid on multiple items
    bids = relationship("Bid", backref="owner")
    
    # Multiple users should be able to place a bid on an item
    

class Bid(Base):
    __tablename__ = "bids"
    '''
    The bid model should contain two columns:
    An integer id, which is the primary key
    A floating-point price, which cannot be null
    '''
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    
    # Users should be able to bid on multiple items
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    
Base.metadata.create_all(engine)

beyonce = User(username="bknowles", password="uhohuhohuhohohnana")
elvis = User(username="king", password="suspiciousmind")
bob = User(username="Robert", password="Bobby")
session.add(beyonce)
session.add(elvis)
session.add(bob)

baseball = Item( name = 'Ball', description = 'World series winning ball', owner=beyonce)  # or beyonce.items.append(baseball)
session.add(baseball)

# Have each other user place two bids on the baseball

elvis_bid1 = Bid(price=100)    
elvis.bids.append(elvis_bid1)
baseball.bids.append(elvis_bid1)
session.add(elvis_bid1)

elvis_bid2 = Bid(price=101)    
elvis.bids.append(elvis_bid2)
baseball.bids.append(elvis_bid2)

bob_bid1 = Bid(price=90)
bob.bids.append(bob_bid1)
baseball.bids.append(bob_bid1)

bob_bid2 = Bid(price=150)
bob.bids.append(bob_bid2)
baseball.bids.append(bob_bid2)

session.commit()

# Perform a query to find out which user placed the highest bid
top_bid = session.query(Bid).order_by(Bid.price.desc()).first() 
print(top_bid.owner.username)


''' to submit to git '''