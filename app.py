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
    mensagem = None
    placa = ''
    if request.method == "POST":
        placa = request.form.get('placa', '').strip().upper()

        if not placa:
            mensagem = "Por favor, informe a placa."
            return render_template("index.html", mensagem=mensagem, alert="dark")

        # Se não cadastrada redireciona para cadastro com a placa
        if not controller.validatePlate(placa):
            return redirect(url_for('cadastro', placa=placa))
        
        # Se estiver estacionado, registrar saída, se não registrar entrada
        if controller.validateStatus(placa):
            resultado = controller.registerOut(placa)
        else:
            resultado = controller.registerEntry(placa)

        mensagem = resultado.get("message", "Operação Realizada.")

        # Se a operação for de entrada, mostra também a vaga em que foi colocado.
        if "spot" in resultado and resultado["spot"]:
            mensagem += f" - Vaga: {resultado['spot']}"

    return render_template("index.html", mensagem=mensagem, alert="success")    

# Rota de cadastro, tela de cadastro de veículo
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    placa = request.args.get('placa', '')
    modelo = ''
    cor = ''
    tipo = 'C'
    tamanho = None
    tipoMoto = None
    mensagem = None
    if request.method == "POST":
        placa = request.form.get('placa', '').strip().upper()
        modelo = request.form.get('modelo', '').strip()
        cor = request.form.get('cor', '').strip()
        tipo = request.form.get('type', 'C')
        tamanho = request.form.get('tamanho')
        tipoMoto = request.form.get('tipoMoto')

        # Validações:

        if not placa:
            mensagem = "Placa é obrigatória."
            return render_template("cadastro.html", placa=placa, modelo=modelo,
                                   cor=cor, tipo=tipo, tamanho=tamanho, tipoMoto=tipoMoto, mensagem=mensagem, alert="warning")

        if not modelo:
            mensagem = "Modelo é obrigatório."
            return render_template("cadastro.html", placa=placa, modelo=modelo,
                                   cor=cor, tipo=tipo, tamanho=tamanho, tipoMoto=tipoMoto, mensagem=mensagem, alert="warning")

        if not cor:
            mensagem = "Cor é obrigatória."
            return render_template("cadastro.html", placa=placa, modelo=modelo,
                                   cor=cor, tipo=tipo, tamanho=tamanho, tipoMoto=tipoMoto, mensagem=mensagem, alert="warning")
        
        # Caso seja carro:
        if tipo == 'C':
            tamanho = request.form.get('tamanho')  # 'M' ou 'G'
            eletric = None
        # Caso seja moto:
        else:
            tipoMoto = request.form.get('tipoMoto')  # 'combustao' ou 'eletrica'
            eletric = True if tipoMoto == 'eletrica' else False
            tamanho = None

        resultado = controller.createVehicle(plate=placa, vehicle_type=tipo, model=modelo, color=cor, size=tamanho, eletric=eletric)

        # Tratamento em caso de insucesso no método
        if resultado.get('sucess', False):
            return redirect(url_for('index'))
        else:
            mensagem = resultado.get('message', 'Erro ao cadastrar veiculo.')
            return render_template("cadastro.html", placa=placa, modelo=modelo, cor=cor, tipo=tipo, tamanho=tamanho, tipoMoto=tipoMoto, mensagem=mensagem, alert="danger")
        
            
    return render_template("cadastro.html", placa=placa, modelo=modelo, cor=cor, tipo=tipo, tamanho=tamanho, tipoMoto=tipoMoto, mensagem=mensagem, alert="success")

# Rota de visualização de clientes, tela de veículos cadastrados
@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    mensagem = None
    alert = "info"

    # POST -> ações (editar / excluir)
    if request.method == "POST":
        action = request.form.get('action', '').strip().lower()
        placa = request.form.get('placa', '').strip().upper()  # garantimos maiúsculas

        if not placa:
            mensagem = "Placa não informada."
            alert = "danger"
            # Recarregar lista e devolver template com mensagem
            lista_clientes = controller.getVehicles()
            return render_template("clientes.html", clientes=lista_clientes, mensagem=mensagem, alert=alert)

        # --- AÇÃO: editar ---
        if action == 'editar':
            modelo = request.form.get('modelo', '').strip()
            cor = request.form.get('cor', '').strip()
            vaga = request.form.get('vaga', '').strip() or None
            tipo = request.form.get('tipo', '').strip()  # 'carro' | 'moto' | ''
            tamanho = request.form.get('tamanho', '').strip() or None
            eletrica_raw = request.form.get('eletrica', '0')  # 0 ou 1
            eletrica_bool = True if eletrica_raw == '1' else False

            # Determinar params para controller.updateVehicle
            size_param = tamanho if tipo == 'carro' else None
            eletric_param = eletrica_bool if tipo == 'moto' else None

            try:
                resultado = controller.updateVehicle(
                    plate=placa,
                    model=modelo if modelo != '' else None,
                    color=cor if cor != '' else None,
                    size=size_param,
                    eletric=eletric_param,
                    vaga=vaga
                )
                # tratar retorno do controller
                if isinstance(resultado, dict):
                    if resultado.get('success', resultado.get('sucess', True)) is True:
                        mensagem = resultado.get('message', 'Veículo atualizado com sucesso!')
                        alert = 'success'
                    else:
                        mensagem = resultado.get('message', 'Erro ao atualizar veículo.')
                        alert = 'danger'
                else:
                    mensagem = 'Veículo atualizado (retorno inesperado do controller).'
                    alert = 'success'
            except Exception as e:
                print(f"Erro em editar cliente (controller.updateVehicle): {e}")
                mensagem = 'Erro ao atualizar veículo (ver logs).'
                alert = 'danger'

            lista_clientes = controller.getVehicles()
            return render_template("clientes.html", clientes=lista_clientes, mensagem=mensagem, alert=alert)

        # --- AÇÃO: excluir ---
        elif action == 'excluir':
            try:
                resultado = controller.deleteVehicle(plate=placa)
                if isinstance(resultado, dict):
                    if resultado.get('success', True) is True:
                        mensagem = resultado.get('message', 'Veículo excluído com sucesso!')
                        alert = 'success'
                    else:
                        mensagem = resultado.get('message', 'Erro ao excluir veículo.')
                        alert = 'danger'
                else:
                    mensagem = 'Veículo excluído (retorno inesperado do controller).'
                    alert = 'success'
            except Exception as e:
                print(f"Erro em excluir cliente (controller.deleteVehicle): {e}")
                mensagem = 'Erro ao excluir veículo (ver logs).'
                alert = 'danger'

            lista_clientes = controller.getVehicles()
            return render_template("clientes.html", clientes=lista_clientes, mensagem=mensagem, alert=alert)

        else:
            mensagem = 'Ação inválida.'
            alert = 'warning'
            lista_clientes = controller.getVehicles()
            return render_template("clientes.html", clientes=lista_clientes, mensagem=mensagem, alert=alert)

    # GET -> apenas renderiza a lista
    lista_clientes = controller.getVehicles()
    return render_template("clientes.html", clientes=lista_clientes)

# Rota de visualização de estadias, tela dos registros de estadia de determinado veículo
@app.route("/estadias", methods=["GET", "POST"])
def estadias():
    placa_buscada = ''
    estadias = []

    if request.method == "POST":
        placa_buscada = request.form.get('placa', '').strip().upper()
        if placa_buscada:
            try:
                estadias = controller.getStays(placa_buscada)
            except Exception as e:
                print(f"Erro ao buscar estadias: {e}")
                estadias = []
    return render_template("estadias.html", placa_buscada=placa_buscada, estadias=estadias)
if __name__ == "__main__":
    app.run(debug=True)

# Rotas Principais

# Rota index, tela de registro de entrada/saída
@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pass
    return render_template("index.html")    

# Rota de cadastro, tela de cadastro de veículo
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        pass
    return render_template("cadastro.html")

# Rota de visualização de clientes, tela de veículos cadastrados
@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    return render_template("clientes.html")

# Rota de visualização de estadias, tela dos registros de estadia de determinado veículo
@app.route("/estadias", methods=["GET", "POST"])
def estadias():
    return render_template("estadias.html")
