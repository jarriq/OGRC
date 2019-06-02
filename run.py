from flask import Flask, render_template, request, redirect
import json
import flask_login
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

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

	print(ip_switch, comunidade)
	print('conectando')
	print('conectado')

	#codigos
	#conectado - conectou ao switch
	#erro - não conectou

	return "conectado"

#################### Fim Conectar ao Switch ####################

#################### Controle de Portas ####################
@app.route("/portas", methods=['POST'])
def portas():
	portas_opcao = request.form['porta_opcao']
	portas_opcao = json.loads(portas_opcao)
	porta = portas_opcao['porta']
	opcao = portas_opcao['opcao']

	if opcao == 1:
		print("abrir")
	if opcao == 2:
		print("fechar")
	if opcao == 3:
		print("teste")

	#codigos
	#sucesso - operacao concluida
	#falha - operacao falhou

	return "sucesso"

#################### Fim Controle de Portas ####################



if __name__=="__main__":
    app.run()
