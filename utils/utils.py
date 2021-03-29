import datetime as dt
import uuid
def currentTime():
    now_time = dt.datetime.now().strftime('%F %T')
    return now_time
def generateID():
    return uuid.uuid1().hex
# def getUpdateDict(dic:dict):
#     ret = dict()
#     for k,v in dic.items():
#