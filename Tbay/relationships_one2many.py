# relationships_one2many.py

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, ForeignKey  # ForeignKey is important for the relationships
from sqlalchemy.orm import relationship

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/guitars')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Manufacturer(Base):
    __tablename__ = 'manufacturer'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    guitars = relationship("Guitar", backref="manufacturer")

class Guitar(Base):
    __tablename__ = 'guitar'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'),
                             nullable=False)

Base.metadata.create_all(engine) # has to be created in the data base before adding rows

fender = Manufacturer(name="Fender")
strat = Guitar(name="Stratocaster", manufacturer=fender)
tele = Guitar(name="Telecaster")
fender.guitars.append(tele)

session.add_all([fender, strat, tele])
session.commit()

for guitar in fender.guitars:
    print(guitar.name)
print(tele.manufacturer.name)