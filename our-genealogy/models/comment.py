from models.base import Base


class Comment(Base):
    def __init__(self, entries=None):
        if entries:
            Base.__init__(self, entries)
            return
        self._id = ''
        self.user_id = ''
        self.article_id = ''
        self.time = ''

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
