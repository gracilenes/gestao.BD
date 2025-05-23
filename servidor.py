#importar a classe Flask
from flask import Flask, render_template, request
import gestaoDB 

#instanciar o servidor Flask
app = Flask(__name__)

#criar banco / tabela
gestaoDB.criarTabela()
usuarios = []

#app.register_blueprint(home_route)

#rota padrão (página principal)
@app.route("/")
def principal():
    return render_template("index.html")

#rota para direcionar para Página de Cadastro
@app.route("/paginaCadastro")
def paginaCadastro():
    return render_template("cadastro.html")

#rota para receber os dados do usuário e cadastrar novo usuário na lista
@app.route("/cadastrarUsuario", methods=['POST'])
def cadastrarUsuario():
    nome = request.form.get('nomeUsuario')
    login = request.form.get('loginUsuario')
    senha = str(request.form.get('senhaUsuario'))
    if(gestaoDB.verificarUsuario(login)==False):
        gestaoDB.inserirUsuario(nome, login, senha)
        mensagem="usuário cadastrado com sucesso"
        return render_template("index.html", mensagem=mensagem)
    else:
        mensagem="usuário já existe"
        return render_template("index.html", mensagem)

#rota para receber login e senha e fazer a autenticação (login)
@app.route("/autenticarUsuario", methods=['POST'])
def autenticar():
    login = request.form.get("loginUsuario")
    senha = str(request.form.get("senhaUsuario"))
    
    logado=gestaoDB.login(login, senha)

    if(logado==True):
        return render_template("logado.html")
    else:    
        mensagem="usuario ou senha incorreto"
        return render_template("home.html", mensagem=mensagem)

@app.route("/listarUsuarios")
def listarUsuarios():
    #return render_template("lista.html", lista=lista_usuarios)
    lista_usuariosDB = gestaoDB.listarUsuarios()
    return render_template("lista.html", lista=lista_usuariosDB)

@app.route("/paginaRecuperarSenha")
def paginaRecuperar():
    return render_template("recuperacao.html")

@app.route("/recuperarSenha", methods=['POST'])
def recuperarSenha():
    nome = request.form.get("nomeUsuario")
    login = request.form.get("loginUsuario")
   
    encontrado=False

    if(gestaoDB.verificarUsuario(login)==True):
        encontrado=True

    if(encontrado==True):
        senha = str(gestaoDB.recuperarSenhaBD(nome, login))
        mensagem="sua senha"+senha
        return render_template("recuperacao.html", mensagem=mensagem)
    else:    
        mensagem="usuario nao encontrado"
        return render_template("recuperacao.html", mensagem=mensagem)
