import json
from pymongo import MongoClient

CLIENTE = MongoClient('localhost', 27017)
"""
Coleções no banco
    usuarios:
        username : str
        password : str

    status_portas:
        porta : bool,
        _id : str (nome da sala)

        a acrescentar:
        -ip_switch: 'str' ip do switch da sala
        -comunidade: 'str' comunidade do switch da sala

    escalonamento:
        conectar: bool,
        data: str,
        horario: str,
        porta : str,
        executado: bool
"""

def cadastra_user(usuario):
    """
    Dado um json usuario no formato
    {"username": 'str' nomeusuario, "senha": 'str' senha}
    cadastra o mesmo no banco na colecao usuarios (autorizados)

    Retorna False caso falha na insercao e True caso contrario
    """
    usuario = json.loads(usuario)
    db = CLIENTE['usuarios']

    print(list(db.usuarios.find({"username":usuario})))

    if list(db.usuarios.find({"username":usuario})):
        print("Usuário já cadastrado")
        return False

    db.usuarios.insert_one({"username":usuario['usuario'],
                            "password":usuario['senha']})
    return True

def verifica_cadastro(user, pwd):
    """
    Dado 'str' usuario (user) e  'str' senha (pwd),
    Retorna True caso cadastrado,
    False caso contrario
    """
    db = CLIENTE['usuarios']

    res = db.usuarios.find({"username":user,
                            "password":pwd})

    res = list(res)
    if res:
        return True
    return False

def get_status_portas(sala="F301"):
    """
    Dada uma sala, retorna 'dict',
    com status das portas conforme
    coleção status portas
    """
    db = CLIENTE['status_portas']

    return json.dumps(db.status_portas.find_one({"_id":sala}))

def altera_status_porta(porta, situacao, sala="F301"):
    """
    Altera o status de uma porta em uma sala,
    conforme porta dada e situacao ('conectar' ou 'desconectar')
    """
    db = CLIENTE['status_portas']

    status = db.status_portas.find_one({})
    status[str(porta)] = situacao

    db.status_portas.delete_one({"_id":"F301"})
    db.status_portas.insert_one(status)

def zera_status_portas(sala="F301", comunidade=comunidade, ip_switch=ip_switch):
    """
    Utilitario  para resetar as porta de uma sala

    TODO: incluir IP do switch
    """
    db = CLIENTE['status_portas']
    status_portas = {
        '_id':sala,
        'comunidade': comunidade,
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
    """
    Cadastra agendamento no banco conforme
    formato da coleção agendamentos,
    recebe formato 'dict'
    Retorna True em caso de sucesso,
    e Falso caso contrario
    """
    db = CLIENTE['agendamento']
    try:
        db.agendamento.insert_one({"conectar": agend['conectar'],
                                    "data": agend['data'],
                                    "horario": agend['horario'],
                                    "porta": agend['porta'],
                                    "ip_switch": agend['ip_switch'],
                                    "comunidade": agend['comunidade'],
                                    "executado": agend['executado'],
                                    })
        return True
    except:
        return False


def lista_agendamentos():
    """
    Retorna lista de 'dicts' com agendamentos
    cadastrados no banco
    """
    db = CLIENTE['agendamento']
    return json.dumps(list(db.agendamento.find({}, {'_id':0})))

def altera_status_agendamento(agend):
    """
    Altera status de uma agendamento no banco para "executado",
    utilitario do modulo escalonamento
    Retorna True em caso de sucesso
    e False caso contrario
    """
    db = CLIENTE['agendamento']

    try:
        db.find_one(agend, {'$set': {"executado":True}})
        return True
    except:
        return False

if __name__ == '__main__':
    zera_status_portas()
    user =  json.dumps({'usuario':'admin@admin.com', 'senha':'admin'})
    cadastra_user(user)
