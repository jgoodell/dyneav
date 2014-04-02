import types

from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import create_engine

from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///eav.db")
metadata = MetaData(engine)

Session = sessionmaker(bind=engine)
DBSession = Session()

class EAVType(object):
    def __init__(self, entity, attribute, value):
        '''Stable state constructor, the combination of all members constitutes the unique
        constraint. The addition of the namespace member allows for the duplication of the
        other members.
        
        Arguments:
        entity,     The entity the instance will represent.
        attribute,  The attribute the instance will represent.
        value,      The value the instance will represent.
        '''
        self.entity = entity
        self.attribute = attribute
        self.value = value
        DBSession.add(self)
        DBSession.flush()

    def __repr__(self):
        return "%s:%s='%s'" % (entity, attribute, value,)

    def __str__(self):
        return "%s:%s='%s'" % (entity, attribute, value,)

    def __eq__(self,other):
        if self.entity == other.entity and self.attribute == other.attribute and self.value == other.value:
            return True
        else:
            return False

eav_type = Table(
    'eav_types', metadata,
    Column('id', Integer, primary_key=True),
    Column('entity', String),
    Column('attribute', String),
    Column('value', String),)


mapper(EAVType, eav_type)

class DynamicType(object):
    def __init__(self,entity):
        self.entity = entity
        
    def __repr__(self):
        return str(self.entity)

    def __str__(self):
        return str(self.entity)

    @classmethod
    def with_uri(cls,uri):
        '''Creates an object using a URI to retrieve the attribute of the object from the DB.

        Arguments,
        uri,  String URI
        '''
        instance = cls(uri)
        attributes = DBSession.query(EAVType).filter_by(entity=uri).all()
        for attribute in attributes:
            setattr(instance,attribute.attribute,attribute.value)
        return instance

if __name__ == "__main__":
    metadata.create_all()
    #Load up the DB
    entry10 = EAVType("/rollings/j/harry_potter/philosophers_stone","date","3/5/2014")
    entry11 = EAVType("/rollings/j/harry_potter/philosophers_stone","title","The Philosopher's Stone")
    entry20 = EAVType("/rollings/j/harry_potter/chamber_of_secrets","date","3/5/2014")
    entry21 = EAVType("/rollings/j/harry_potter/chamber_of_secrets","title","The Chamber of Secrets")
    entry30 = EAVType("/rollings/j/harry_potter/prisoner_of_azkaban","date","3/5/2014")
    entry31 = EAVType("/rollings/j/harry_potter/prisoner_of_azkaban","title","The Prisoner of Azkaban")
    entry40 = EAVType("/rollings/j/harry_potter/goblet_of_fire","date","3/5/2014")
    entry41 = EAVType("/rollings/j/harry_potter/goblet_of_fire","title","The Goblet of Fire")
    entry50 = EAVType("/rollings/j/harry_potter/order_of_the_phoenix","date","3/5/2014")
    entry51 = EAVType("/rollings/j/harry_potter/order_of_the_phoenix","title","The Order of the Pheonix")
    entry60 = EAVType("/rollings/j/harry_potter/half_blood_prince","date","3/5/2014")
    entry61 = EAVType("/rollings/j/harry_potter/half_blood_prince","title","The Half Blood Prince")
    entry70 = EAVType("/rollings/j/harry_potter/deathly_hallows","date","3/5/2014")
    entry71 = EAVType("/rollings/j/harry_potter/deathly_hallows","title","The Deathly Hallows")
    DBSession.commit()

    dynamic_book = DynamicType.with_uri("/rollings/j/harry_potter/prisoner_of_azkaban")
    print(dynamic_book)
    print(dynamic_book.title)
    print(dynamic_book.date)
