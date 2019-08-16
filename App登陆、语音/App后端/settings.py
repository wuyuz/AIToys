
AVATAR_PATH = "Avatar"
RECO_PATH = 'Reco'

from pymongo import MongoClient

MC = MongoClient('127.0.0.1',27017)

MongoDB = MC['APP']


 # 返回协议

RET = {
    'code':0,
    'msg':'',
    'data':[]
}