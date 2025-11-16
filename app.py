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
    /         - Tela inicial
    /cadastro - Tela de cadastro
    /veiculos - Tela de consulta de veiculos
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

if __name__ == "__main__":
    app.run(debug=True)