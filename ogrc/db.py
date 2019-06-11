from pymongo import MongoClient
import urllib.parse as parse
from urllib.parse import quote_plus

print(parse.quote_plus('qwerty@123'))
qwerty%40123
client = MongoClient("mongodb+srv://jarriq:qwerty%40123@cluster0-xivyu.mongodb.net/test?retryWrites=true&w=majority")
print(client)

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
