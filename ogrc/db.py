from mongoengine import Document, StringField, IntField, DictField, connect

from pymongo import MongoClient
from urllib.parse import quote_plus

client = MongoClient("mongodb+srv://jarriq:qwe123@cluster0-xivyu.mongodb.net/test?retryWrites=true&w=majority")

ACCESS_LV = {
    'user': 1,
    'admin': 2
    }

class Usuario(Document):
    user = StringField(required=True)
    passwd = StringField(required=True)
    acesso = IntField(required=True)

    def is_admin(self):
        return self.accesso == ACCESS_LV['admin']

class Sala(Document):
    nome = StringField(required=True, unique=True)
    portas = DictField(required=True)

if __name__ == '__main__':
    banco = client['teste']
    usuarios = banco.usuario
    consulta = {'user':'pedro alvarez cabral',
                'senha':'123',
                'acesso':'admin'}
    res = usuarios.insert_one(consulta)
    if res:
        print('certo')
    else:
        print("errado")
