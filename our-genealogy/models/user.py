from models.base import Base
from werkzeug.security import generate_password_hash, check_password_hash
class User(Base):
    def __init__(self, entries=None):
        if entries:
            Base.__init__(self, entries)
            return
        self._id = 0
        self.nickname=''
        self.password=''
        self.email=''
        self.phone=''
        self.register_time=''
        self.type=''


    @property
    def id(self):
        return self._id
    @id.setter
    def id(self,value):
        self._id = value

    def passwordHash(self):
        self.password = generate_password_hash(self.password)

    def check_password(self,pwd):
        return check_password_hash(self.password,pwd)