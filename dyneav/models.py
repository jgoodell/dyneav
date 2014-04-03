import types
import pickle

from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import create_engine

from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///eav.db")
metadata = MetaData(engine)

Session = sessionmaker(bind=engine)
DBSession = Session()

class EAVType(object):
    def __init__(self, entity, attribute, value, is_method=False):
        '''Stable state constructor, the combination of all members constitutes the unique
        constraint. The addition of the namespace member allows for the duplication of the
        other members.
        
        Arguments:
        entity,     The entity the instance will represent.
        attribute,  The attribute the instance will represent.
        value,      The value the instance will represent.
        is_method,  A boolean indicating if the attribute is a method.
        '''
        self.entity = entity
        self.attribute = attribute
        self.value = value
        self.is_method = is_method
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
    Column('value', String),
    Column('is_method',Boolean),)


mapper(EAVType, eav_type)


