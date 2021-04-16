from models.base import Base


class Article(Base):
    def __init__(self, entries=None):
        if entries:
            Base.__init__(self, entries)
            return
        self._id = 0
        self.title = ''
        self.thumbnail = ''
        self.extra = ''
        self.user_id = ''
        self.access_level = 0
        self.content = ''
        self.imgUrl = ''
        self.families = [] # TODO
        self.comment_ids = [] # TODO
        self.created_time = 0
        self.modified_time = 0
        self.click_num = 0
        self.like_num = 0
        self.favorite_num = 0
        self.share_num = 0

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
