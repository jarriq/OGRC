import json
import os

from flask import Flask, redirect, render_template, request

import flask_login
start()
from ogrc import db
from ogrc.snmp import SNMP
from ogrc.escalonador import Escalonador

app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

esc = Escalonador() 
esc.sched.start()


manager = SNMP()

@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/painel')
#@flask_login.login_required
def painel():
    return render_template('painel.html')


#################### Login ####################

#base de dados que devera ser substituida pelo
#mongodb
users = {'email@email.com': {'password': '1234'}}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user


@app.route("/logar", methods=['POST', 'GET'])
def logar():
	if request.method == 'GET':
		return render_template('index.html', erro_login=True)

	email = request.form['email']
	senha = request.form['senha']

	#aqui a verificao do login
	if db.verifica_cadastro(email, senha):
		user = User()
		user.id = email
		flask_login.login_user(user)
		return redirect("../painel")
	else:
		return redirect("../logar")

@app.route('/sair')
def logout():
    flask_login.logout_user()
    return redirect("../")


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect("../")

#################### Fim Login ####################


#################### Conectar ao Switch ####################

@app.route("/conectar", methods=['POST'])
def conectar():
	dados_conexao = request.form['dados_conexao']
	dados_conexao = json.loads(dados_conexao)
	ip_switch = dados_conexao['ip']
	comunidade = dados_conexao['comunidade']
	manager.ip_switch = ip_switch
	manager.comunidade = comunidade
	print(ip_switch, comunidade)

	print('Testando conexão com switch...')
	if manager.testa_conexao():
		print('Conectado ao switch')
		return "conectado"
	else:
		print('Conexão falhou')
		return "erro"



#################### Fim Conectar ao Switch ####################

#################### Controle de Portas ####################
@app.route("/portas", methods=['POST'])
def portas():
	portas_opcao = request.form['porta_opcao']
	portas_opcao = json.loads(portas_opcao)
	porta = portas_opcao['porta']
	comando = portas_opcao['opcao']

	if comando == 1:
		print("Comando abrir porta:", porta)
	elif comando == 2:
		print("Comando fechar porta:", porta)
	elif comando == 3:
		print("Comando teste porta:", porta)
	else:
		raise ValueError("Comando inválido != (1-3)")

	if manager.altera_porta(porta, comando):
		return "sucesso"
	else:
		return "fracasso"

#################### Fim Controle de Portas ####################

@app.route("/status", methods=['POST'])
def pegar_status_portas():
	return db.get_status_portas()

@app.route("/escalonamento", methods=['POST'])
def pegar_agendamentos():
	return db.lista_agendamentos()

@app.route("/agendar", methods=['POST'])
def cadatra_agendamento():
	agend = request.form['agendamento']
	agend = json.loads(agend)
	agend['ip_switch'] = manager.ip_switch
	agend['comunidade'] = manager.comunidade
	if db.cadastra_agendamento(agend):
		esc.adiciona_agendamento(agend)
		return "ok"
	else:
		return "erro"




############################## instruções ##############
# Fazer autenticação com o banco
# 	- A função logar() já funciona. Só falta ela verificar as credenciais no banco
# 	- A verificação já é feita na linha 69

# Fazer função(método post) que returna o status das portas no banco
# 	- Deve retornar um json como está no arquivo painel.html
# 	- O nome do json lá é status_portas

# Fazer função (método post) que cadastra uma tarefa no banco
# 	- A entrada é uma linha do json chamado escalonamento (olhar painel.html)
# 	- Retorna ok para cadastrado e erro para não cadastrado

# Fazer funcao (método post) que retorna todas as tarefas agendadas 
# 	- O retorno deve ser um json, igual ao json escalonamento do arquivo painel.html

if __name__=="__main__":
    app.run()
