from models.base import Base


class Family(Base):
    def __init__(self, entries=None):
        self.members = []
        self.admins = []
        self.relations = []
        if entries:
            Base.__init__(self, entries)
            return
        self._id = 0
        self.created_by = 0
        self.created_on = ''
        self.surname = ''
        self.name = ''
        self.area = ''
        self.tanghao = ''
        self.description = ''
        self.members = []
        self.admins = []
        self.relations = []
        self.read_admins= []
        self.avatar_url = ''
        self.is_public=''

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

