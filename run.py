from flask import Flask, render_template, request, redirect
import json
import flask_login
import os
from ogrc.snmp import SNMP
from ogrc import db

app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

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
	if email in users and senha == users[email]['password']:
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
		return "deu ruim"



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



if __name__=="__main__":
    app.run()
