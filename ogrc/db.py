import json
from pymongo import MongoClient

CLIENTE = MongoClient('localhost', 27017)
"""
collections:

    usuarios:
        username : str
        password : str

    portas:
        porta : bool,
        _id : str sala
  
    escalonamento:
        conectar: bool,
        data: str,
        horario: str,
        porta : str,
        executado: bool
"""
def cadastra_user(usuario):
    usuario = json.loads(usuario)
    db = CLIENTE['usuarios']
    
    db.usuarios.insert_one({"username":usuario['nome'],
                            "password":usuario['senha']})


def get_status_portas():
    db = CLIENTE['status_portas']

    return db.status_portas.find_one({"_id":"F301"})

def zera_status_portas():
    db = CLIENTE['status_portas']
    status_portas = {
        '_id':"F301",
        'comunidade': 'private',
        '1':True,
        '2':True,
        '3':True,
        '4':True,
        '5':True,
        '6':True,
        '7':True,
        '8':True,
        '9':True,
        '10':True,
        '11':True,
        '12':True,
        '13':True,
        '14':True,
        '15':True,
        '16':True,
        '17':True,
        '18':True,
        '19':True,
        '20':True,
        '21':True,
        '22':True,
        '23':True,
        '24':True
    }
    db.status_portas.delete_one({"_id":"F301"})
    db.status_portas.insert_one(status_portas)

def cadastra_agendamento(agend):
    agend = json.loads(agend)

    db = CLIENTE['agendamento']
    
    db.agendamento.insert_one({"conectar": agend.comando,
                                "data": agend.data,
                                "horario": agend.horario,
                                "porta": agend.porta,
                                "executado": agend.executado})


if __name__ == '__main__':
    banco = CLIENTE['teste']
    teste = banco.teste
    consulta = {'user':'pedro alvarez cabral',
                'senha':'123'}
    res = teste.insert_one(consulta)
    if res:
        print('certo')
    else:
        print("errado")

    zera_status_portas()
    print(get_status_portas())
