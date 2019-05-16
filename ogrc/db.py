from pymongo import MongoClient
from mongoengine import Document
from urllib.parse import quote_plus


def conecta_banco(self):
    client = MongoClient("mongodb+srv://jarriq:"+quote_plus("qwe@123")+"@jarriq-as8oa.mongodb.net/test?retryWrites=true")
    return client


        
