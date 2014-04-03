from dyneav import EAVType
from dyneav import DBSession

class DynamicType(object):
    '''A type that can dynamically set its attributes based on the values set in a
    EAV table for a given entity.
    '''
    def __init__(self,entity):
        '''Constructor that sets the type of the instance.

        Arguments:
        entity,  The object that indicates the type of the instance.
        '''
        self.entity = entity
        
    def __repr__(self):
        return str(self.entity)

    def __str__(self):
        return str(self.entity)

    def __eq__(self,other):
        try:
            if self.entity == other.entity:
                return True
            else:
                return False
        except AttributeError:
            return False

    @classmethod
    def with_uri(cls,uri):
        '''Creates an object using a URI to retrieve the attribute of the object from the DB.

        Arguments,
        uri,  String URI
        '''
        instance = cls(uri)
        attributes = DBSession.query(EAVType).filter_by(entity=uri).all()
        for attribute in attributes:
            if attribute.is_method:
                setattr(instance,attribute.attribute,types.MethodType(pickle.loads(attribute.value),instance,EAVType))
            else:
                setattr(instance,attribute.attribute,attribute.value)
        return instance


if __name__ == "__main__":
    metadata.create_all()

    def do_something(self):
        return self.title
    
    #Load up the DB
    entry10 = EAVType("/rollings/j/harry_potter/philosophers_stone","date","3/5/2014")
    entry11 = EAVType("/rollings/j/harry_potter/philosophers_stone","title","The Philosopher's Stone")
    entry12 = EAVType("/rollings/j/harry_potter/philosophers_stone","do_something",
                      pickle.dumps(do_something),is_method=True)
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

    dynamic_book01 = DynamicType.with_uri("/rollings/j/harry_potter/prisoner_of_azkaban")
    print(dynamic_book01)
    print(dynamic_book01.title)
    print(dynamic_book01.date)

    dynamic_book02 = DynamicType.with_uri("/rollings/j/harry_potter/philosophers_stone")
    print(dynamic_book02)
    print(dynamic_book02.title)
    print(dynamic_book02.date)
    print(dynamic_book02.do_something())
