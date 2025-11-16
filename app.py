# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from repository.database import iniciar_banco
from repository.estacionamento_repo import processar_placa
import controller

app = Flask(__name__)
app.secret_key = "troque-esta-chave"
iniciar_banco()

"""
    Planejamento:

    app.py - definir rotas e chamadas de função
    /class/* - definir classes e metodos
    controller.py - definir modulo de funções utilizadas

    Rotas:
    /index    - Tela inicial
    /cadastro - Tela de cadastro
    /clientes - Tela de consulta de veiculos
    /estadias - Tela de consulta de estadias

    - Tela inicial, contem um input que deverá ser inserido a PLACA do veículo:
        * Validar existencia do veículo;
        * Validar status do veículo (Estacionado ou não);
        * Se estiver estacionado, pede se deseja realmente registrar a entrada; (Fazer em JS)
        * Se não estiver estacionado, pede se deseja realmente registrar a saída;
        * Fazer feedback para: Veículo não encontrado, Entrada Registrada, Saída Registrada;

        funções:
        createStay - Chamada ao incluir entrada, cria a estadia
        registerEntry - Grava os valores de entrada no registro da estadia em aberto
        registerOut - Grava os valores de saída no registro de estadia em aberto
        updateStatus - Atualiza o status do veiculo conforme o parametro passado
        validatePlate - Valida existência da placa
        validateStatus - Valida o status da placa passada por parametro

    - Tela de cadastro, contem um formulario com os dados da classe do veículo
        * Validar existencia do veículo;
        * Validar consistencia dos dados preenchidos;
        * Fazer feedback: Veiculo já existente, Veículo incluido com sucesso;
        
        funções:
        validatePlate - Valida existência da placa
        createVehicle - Cria veículo 

    - Tela de Consulta de estadias, contem um input que deverá ser inserido a PLACA do veículo, e caso renderizado com o objeto contendo estadias, 
      deve listar as estadias do veículo em forma da table
        * Validar existencia do veículo;
        * Buscar estadias do veículo e retornar o objeto para o HTML;
        * No HTML listar as estadias;

        funções:
        validatePlate - Valida existência da placa
        getStays - Busca todas as estadias do veículo e retorna o array de objetos (estadias)

    - Tela de Consulta de Veiculos, contém uma table com todos os clientes, com dois botões, de edição e exclusão do veículo
        * Exibe em tela todos os clientes cadastrados;
        * Opção de exclusão remove o veiculo da tabela e recarrega a HTML do component;
        * Opção de edição abre um modal de atualização com os dados pré preenchidos;

        funções:
        getVehicles - Busca todos os veículos e retorna um array de objetos (veículos)
        deleteVehicle - Deleta veículo da tabela e recarrega o component
        updateVehicle - Chamado após o submit do modal, faz a validação da consistencia dos dados e recarrega o component
"""


# Rotas Principais

# Rota index, tela de registro de entrada/saída
@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        placa = request.form.get('placa')

        # Verificar se há o registro da placa
        if not controller.validatePlate(placa):
            return redirect(url_for('cadastro', placa=placa))
        
        # Se estiver estacionado, registrar saída
        if controller.validateStatus:
            return controller.registerOut(placa)
        
        # Se estiver já cadastrado e não tem Estadia aberta, iremos registrar entrada
        else:
            return controller.registerEntry(placa)
    return render_template("index.html")    

# Rota de cadastro, tela de cadastro de veículo
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    placa = request.args.get('placa')  # pode vir None se não vier na URL
    if request.method == "POST":
        pass
    return render_template("cadastro.html", placa=placa)

# Rota de visualização de clientes, tela de veículos cadastrados
@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    if request.method == 'POST':
        vehicles = controller.getVehicles()
        return render_template("clientes.html", vehicles=vehicles)
    return render_template("clientes.html")

# Rota de visualização de estadias, tela dos registros de estadia de determinado veículo
@app.route("/estadias", methods=["GET", "POST"])
def estadias():
    if request.method == 'POST':
    return render_template("estadias.html")

if __name__ == "__main__":
    app.run(debug=True)