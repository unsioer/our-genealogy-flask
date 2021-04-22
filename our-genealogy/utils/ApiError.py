#define custome status_code here
NOT_FOUND=404
WRONG_PASSWORD=800
EMAIL_ALREADY_EXIST=801
DATABASE_ERROR=506
NO_AUTH = 802
REPETITIVE_OPERATION=803
error_MSG={
NOT_FOUND:"NO SUCH ID",
DATABASE_ERROR:"ERROR OCCURRED IN ACCESSING TO DATABASE",
WRONG_PASSWORD:"password wrong",
EMAIL_ALREADY_EXIST:"email already exist",
NO_AUTH:"no authorization",
REPETITIVE_OPERATION:"repetitive operation"
}

class ApiError(Exception):
    status_code = 200
    def __init__(self,return_code=None,status_code=None,payload=None):
        Exception.__init__(self)
        self.return_code = return_code
        if status_code!=None:
            self.status_code =status_code
        self.payload = payload
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['return_code']=self.return_code
        rv['message'] = error_MSG[self.return_code]
        return rv