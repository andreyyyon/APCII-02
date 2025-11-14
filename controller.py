# controller.py
from classes.Carro import Carro
from classes.Moto import Moto
from classes.Estadia import Estadia

"""
    Funções a serem criadas:

    getStays - Busca todas as estadias do veículo e retorna o array de objetos (estadias)
    getVehicles - Busca todos os veículos e retorna um array de objetos (veículos)
    deleteVehicle - Deleta veículo da tabela e recarrega o component
    updateVehicle - Chamado após o submit do modal, faz a validação da consistencia dos dados e recarrega o component
"""

"""
    Função para validar a existência de uma placa no banco de dados.
"""
def validatePlate(plate: str):

    # FAZER A VALIDAÇÃO

    return True

"""
    Função para validar o status de um veiculo no banco de dados.

    status - True: Estacionado False: Não Estacionado
"""
def validateStatus(plate: str):

    # FAZER A VALIDAÇÃO

    return True

"""
    Função para pegar a Estadia em formato de classe
"""
def getStay(plate: str):
    try:
        if validateStatus(plate):
            spot = "vaga"
            entry = "entrada"
            out = "saída"

            # FAZER A LOGICA PARA PREENCHER AS VARIAVEIS (BUSCANDO DO DB)

            Stay = Estadia(vaga=spot, placa=plate, entrada=entry, saida=out)

            return Stay
        else:
            print("Veiculo não está em uma vaga")

    except NameError:
        print("Error:", NameError)


"""
    Função para criar uma nova estadia.
"""
def createStay(plate: str, spot: str):
    try:
        Stay = Estadia(vaga=spot, placa=plate, entrada="", saida="")

        return Stay
    except NameError:
        print("Error:", NameError)

"""
    Função para registrar uma nova entrada.
"""
def registerEntry(plate: str):
    try:
        if validatePlate(plate):
            spot = getSpot(plate)
            Stay = createStay(plate, spot)

            Stay.register_entry()
            updateStatus(plate, True)

            # AGORA REGISTRA A NOVA ESTADIA NO DB

        else:
            print("Placa não existe!")
    except NameError:
        print("Error:", NameError)

"""
    Função pra registrar uma nova saída
"""
def registerOut(plate: str):
    try:
        Stay = getStay(plate)

        Stay.register_out()
        updateStatus(plate, False)

        # AGORA ATUALIZA A ESTADIA NO DB

    except NameError:
        print("Error:", NameError)

"""
    Função para pegar uma vaga sugerida
"""
def getSpot(plate: str):
    try:
        if validatePlate(plate):
            Vehicle = getVehicle(plate)

            # FAZER A LOGICA PARA A VAGA SUGERIDA

            spot = "vaga sugerida"

        else:
            print("Veiculo não existe")

        return spot
    except NameError:
        print("Error:", NameError)

"""
    Função para pegar os dados do veículo pela placa
"""
def getVehicle(plate: str):
    try:
        type = "C"
        size = "M"
        eletric = False
        status = False
        model = ""
        color = ""

        # FAZER A LOGICA PARA BUSCAR NO DB E PREENCHER AS VARIAVEIS

        if type == "C":
            Vehicle = Carro(placa=plate, modelo=model, cor=color, status=status, tamanho=size)
        elif type == "M":
            Vehicle = Moto(placa=plate, modelo=model, cor=color, eletrica=eletric)

    except NameError:
        print("Error:", NameError)

    return Vehicle

"""
    Função para criar um novo veículo
"""
def createVehicle(plate: str, type: str, model: str, color: str, size: str, eletric: bool):
    try:
        if not validatePlate(plate):
            if type == "C":
                Vehicle = Carro(placa=plate, modelo=model, cor=color, status=False, tamanho=size)
            elif type == "M":
                Vehicle = Moto(placa=plate, modelo=model, cor=color, status=False, eletrica=eletric)

            # REGISTRA O NOVO VEICULO NO DB

        else:
            print("Veiculo já existe!")

    except NameError:
        print("Error:", NameError)

"""
    Função para atualizar o status de um veículo

    status - True: Estacionado False: Não Estacionado
"""
def updateStatus(plate: str, status: bool):
    try:
        if validatePlate(plate):
            Vehicle = getVehicle(plate)
            Vehicle.status(status)

            # ATUALIZAR O STATUS NO DB
            
        else:
            print("Veiculo não existe!")

    except NameError:
        print("Error:", NameError)


