from models.base import Base


class Relation(Base):
    '''
    Relation
    '''
    def __init__(self, entries=None):
        if entries:
            Base.__init__(self, entries)
            return
        self.id = 0
        self.created_by = 0
        self.created_on = ''
        self.from_person = 0
        self.to_person = 0
        self.family_id = 0
        self.type = 0
        self.special = 0
