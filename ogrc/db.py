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

    print(list(db.usuarios.find({"username":usuario})))

    if not list(db.usuarios.find({"username":usuario})):
        print("Usuário já cadastrado")
        return False

    db.usuarios.insert_one({"username":usuario['usuario'],
                            "password":usuario['senha']})
    return True

def verifica_cadastro(user, pwd):
    db = CLIENTE['usuarios']

    res = db.usuarios.find({"username":user,
                            "password":pwd})

    res = list(res)
    if res:
        return True
    return False




def get_status_portas(sala="F301"):
    db = CLIENTE['status_portas']

    return json.dumps(db.status_portas.find_one({"_id":sala}))

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
    try:
        db.agendamento.insert_one({"conectar": agend['conectar'],
                                    "data": agend['data'],
                                    "horario": agend['horario'],
                                    "porta": agend['porta'],
                                    "executado": agend['executado']})
        return True
    except:
        return False


def lista_agendamentos():
    db = CLIENTE['agendamento']
    return json.dumps(list(db.agendamento.find({}, {'_id':0})))


if __name__ == '__main__':
    agend = {
          'conectar': True,
          'data': '14/06/2019',
          'horario': '15:55',
          'porta' : '21',
          'executado': False
          }
    agend = json.dumps(agend)

    banco = CLIENTE['teste']
    teste = banco.teste

    zera_status_portas()
    print(get_status_portas())
    cadastra_agendamento(agend)
    user =  json.dumps({'usuario':'admin', 'senha':'admin'})
    cadastra_user(user)
    print(lista_agendamentos())
    print(verifica_cadastro('admin','admin'))
    print(verifica_cadastro('admin','admin2'))
