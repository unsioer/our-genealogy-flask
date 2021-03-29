from models.base import Base


class Person(Base):
    def __init__(self, entries=None):
        if entries:
            Base.__init__(self, entries)
            return
        self._id = 0
        self.user_id = 0
        self.name = ''
        self.gender = 'M'
        self.families = []
        self.living = True
        self.born = ''
        self.death = ''
        self.description=''

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self,value):
        self._id = value
