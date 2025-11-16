# controller.py
from classes.Carro import Carro
from classes.Moto import Moto
from classes.Estadia import Estadia
from repository.database import conectar, Veiculo as VeiculoDB, Estadia as EstadiaDB, Vaga
from sqlalchemy.exc import IntegrityError

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
def validatePlate(plate: str) -> bool: #função OK
    """
    Valida a existência de uma placa no banco de dados.
    
    Args:
        plate (str): Placa do veículo (será convertida para maiúsculas)
        
    Returns:
        bool: True se existe, False caso contrário
    """
    try:
        sessao = conectar()
        plate_upper = plate.strip().upper()
        veiculo = sessao.query(VeiculoDB).filter(VeiculoDB.placa == plate_upper).first()
        sessao.close()
        if veiculo:
            return True
        else:
            return False
    except Exception as e:
        print(f"Erro ao validar placa: {e}")
        return False

"""
    Função para validar o status de um veiculo no banco de dados.

    status - True: Estacionado False: Não Estacionado
"""
def validateStatus(plate: str) -> bool: #função OK
    """
    Valida o status de um veículo (se está estacionado ou não).
    
    Args:
        plate (str): Placa do veículo
        
    Returns:
        bool: True se estacionado, False caso contrário
    """
    try:
        sessao = conectar()
        plate_upper = plate.strip().upper()
        
        # Busca a estadia aberta (sem data de saída)
        estadia_aberta = (sessao.query(EstadiaDB)
                           .filter(EstadiaDB.placa == plate_upper, EstadiaDB.saida.is_(None)).first())
        sessao.close()
        if estadia_aberta:
            return True # Tem estadia aberta desse veículo, está estacionado
        else:
            return False # Não tem estadia aberta desse veículo, não está estacionado
        
    except Exception as e:
        print(f"Erro ao validar status: {e}")
        return False

"""
    Função para pegar a Estadia em formato de classe
"""
def getStay(plate: str): #função OK
    """
    Recupera a estadia aberta (sem saída) de um veículo.
    
    Args:
        plate (str): Placa do veículo
        
    Returns:
        Estadia: Objeto da estadia, ou None se não houver estadia aberta
    """
    try:
        if validateStatus(plate) == False:
            print("Veículo não está estacionado")
            return None
        
        sessao = conectar()
        plate_upper = plate.strip().upper()
        
        estadia_db = (sessao.query(EstadiaDB)
                      .filter(EstadiaDB.placa == plate_upper, EstadiaDB.saida.is_(None))
                      .order_by(EstadiaDB.id.desc())
                      .first())
        
        # Faz mais uma verificação se realmente há estadia aberta. Se não achou na query, retorna None.
        if not estadia_db:
            sessao.close()
            return None
        
        # Converter de Datetime para String, para ser possível a criação do objeto de Estadia
        entrada_str = estadia_db.entrada.strftime('%d/%m/%Y %H:%M:%S') if estadia_db.entrada is not None else ""
        saida_str = estadia_db.saida.strftime('%d/%m/%Y %H:%M:%S') if estadia_db.saida is not None else ""
        
        estadia = Estadia(
            vaga=estadia_db.vaga,
            placa=estadia_db.placa,
            entrada=entrada_str,
            saida=saida_str
        )
        
        sessao.close()
        return estadia
    except Exception as e:
        print(f"Erro ao recuperar estadia: {e}")
        return None


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


