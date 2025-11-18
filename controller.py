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
    Função para pegar a Estadia aberta em formato de classe
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
def createStay(plate: str, spot: str): # função OK
    """
    Cria uma nova estadia no banco de dados.
    
    Args:
        plate (str): Placa do veículo
        spot (str): Código da vaga
        
    Returns:
        Estadia: Objeto da estadia criada, ou None em caso de erro
        É criado o registro na tabela Estadias
    """
    try:
        sessao = conectar()
        plate_upper = plate.strip().upper()
        
        # Marcar vaga como ocupada
        vaga = sessao.query(Vaga).filter(Vaga.codigo == spot).first()
        if vaga:
            vaga.ocupada = True 
        
        # Atualizar veiculo com vaga_atual
        veiculo = sessao.query(VeiculoDB).filter(VeiculoDB.placa == plate_upper).first()
        if veiculo:
            veiculo.vaga_atual = spot
        
        # Criar estadia
        nova_estadia = EstadiaDB(
            placa=plate_upper,
            vaga=spot
        )
        sessao.add(nova_estadia)
        sessao.commit()
        
        # Converter para objeto de classe
        estadia = Estadia(
            vaga=spot,
            placa=plate_upper,
            entrada=nova_estadia.entrada.strftime('%d/%m/%Y %H:%M:%S'),
            saida=None
        )
        
        sessao.close()
        return estadia
    except Exception as e:
        print(f"Erro ao criar estadia: {e}")
        return None

"""
    Função para registrar uma nova entrada.
"""
def registerEntry(plate: str) -> dict: # função OK
    """
    Registra a entrada de um veículo no estacionamento.
    
    Args:
        plate (str): Placa do veículo
        
    Returns:
        dict: {'success': bool, 'message': str, 'spot': str}
    """
    try:
        if not validatePlate(plate):
            return {'success': False, 'message': 'Placa não cadastrada!'}
        
        if validateStatus(plate):
            return {'success': False, 'message': 'Veículo já está estacionado!'}
        
        spot = getSpot(plate)
        if not spot:
            return {'success': False, 'message': 'Não há vagas disponíveis para este veículo!'}
        
        estadia = createStay(plate, spot)
        if estadia:
            return {'success': True, 'message': 'Entrada registrada com sucesso!', 'spot': spot}
        else:
            return {'success': False, 'message': 'Erro ao registrar entrada'}
    except Exception as e:
        print(f"Erro ao registrar entrada: {e}")
        return {'success': False, 'message': f'Erro: {str(e)}'}

"""
    Função pra registrar uma nova saída
"""
def registerOut(plate: str) -> dict: # função OK
    """
    Registra a saída de um veículo do estacionamento.
    
    Args:
        plate (str): Placa do veículo
        
    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        if not validatePlate(plate):
            return {'success': False, 'message': 'Placa não cadastrada!'}
        
        if not validateStatus(plate):
            return {'success': False, 'message': 'Veículo não está estacionado!'}
        
        sessao = conectar()
        plate_upper = plate.strip().upper()
        
        # Buscar estadia aberta
        estadia = (sessao.query(EstadiaDB)
                   .filter(EstadiaDB.placa == plate_upper, EstadiaDB.saida.is_(None))
                   .order_by(EstadiaDB.id.desc())
                   .first())
        
        if not estadia:
            sessao.close()
            return {'success': False, 'message': 'Nenhuma estadia aberta encontrada!'}
        
        # Registrar saída
        from datetime import datetime, timezone
        estadia.saida = datetime.now(timezone.utc)  # type: ignore
        
        # Liberar vaga
        veiculo = sessao.query(VeiculoDB).filter(VeiculoDB.placa == plate_upper).first()
        if veiculo is not None and veiculo.vaga_atual is not None:
            vaga = sessao.query(Vaga).filter(Vaga.codigo == veiculo.vaga_atual).first()
            if vaga:
                vaga.ocupada = False  # type: ignore
            veiculo.vaga_atual = None  # type: ignore
        
        sessao.commit()
        sessao.close()
        
        return {'success': True, 'message': 'Saída registrada com sucesso!'}
    except Exception as e:
        print(f"Erro ao registrar saída: {e}")
        return {'success': False, 'message': f'Erro: {str(e)}'}

"""
    Função para pegar uma vaga sugerida
"""
def getSpot(plate: str) -> str | None: # função OK
    """
    Encontra uma vaga disponível compatível com o tipo de veículo.
    
    Args:
        plate (str): Placa do veículo
        
    Returns:
        str: Código da vaga, ou None se não houver vagas disponíveis
    """
    try:
        if not validatePlate(plate):
            print("Veículo não existe")
            return None
        
        veiculo = getVehicle(plate)
        if not veiculo:
            return None
        
        sessao = conectar()
        
        # Determinar tipo de vaga conforme o tipo de veículo
        tipo_vaga = None
        if isinstance(veiculo, Carro):
            tipo_vaga = veiculo.tamanho  # M ou G
        elif isinstance(veiculo, Moto):
            is_eletrica = bool(veiculo.eletrica)
            tipo_vaga = "E" if is_eletrica else "C"
        
        if tipo_vaga is None:
            sessao.close()
            return None
        
        # Buscar vaga disponível
        vaga = (sessao.query(Vaga)
                .filter(Vaga.tipo == tipo_vaga, Vaga.ocupada == False)
                .order_by(Vaga.codigo.asc())
                .first())
        
        sessao.close()
        
        return str(vaga.codigo) if vaga is not None else None
    except Exception as e:
        print(f"Erro ao obter vaga: {e}")
        return None

"""
    Função para pegar os dados do veículo pela placa
"""
def getVehicle(plate: str): #f unção OK
    """
    Recupera os dados de um veículo e retorna como objeto de classe (Carro ou Moto).
    
    Args:
        plate (str): Placa do veículo
        
    Returns:
        Carro ou Moto: Objeto do veículo, ou None se não encontrado
    """
    try:
        sessao = conectar()
        plate_upper = plate.strip().upper()
        veiculo_db = sessao.query(VeiculoDB).filter(VeiculoDB.placa == plate_upper).first()
        
        if not veiculo_db:
            sessao.close()
            print(f"Veículo com placa {plate_upper} não encontrado.")
            return None
        
        # Converter de modelo ORM para objeto de classe
        tipo_veiculo = str(veiculo_db.tipo)
        if tipo_veiculo == "C":
            veiculo = Carro(
                placa=veiculo_db.placa,
                modelo=veiculo_db.modelo,
                cor=veiculo_db.cor,
                status=veiculo_db.vaga_atual is not None,  # True se tem vaga atual
                tamanho=veiculo_db.tamanho
            )
        elif tipo_veiculo == "M":
            veiculo = Moto(
                placa=veiculo_db.placa,
                modelo=veiculo_db.modelo,
                cor=veiculo_db.cor,
                status=veiculo_db.vaga_atual is not None,  # True se tem vaga atual
                eletrica=veiculo_db.eletrica
            )
        else:
            veiculo = None
        
        sessao.close()
        return veiculo
    except Exception as e:
        print(f"Erro ao recuperar veículo: {e}")
        return None

"""
    Função para criar um novo veículo
"""
def createVehicle(plate: str, vehicle_type: str, model: str, color: str, size: str | None = None, eletric: bool | None = None) -> dict: # função OK
    """
    Cria um novo veículo no banco de dados.
    
    Args:
        plate (str): Placa do veículo
        vehicle_type (str): Tipo ('C' para Carro, 'M' para Moto)
        model (str): Modelo do veículo
        color (str): Cor do veículo
        size (str): Tamanho ('M' ou 'G') - obrigatório para Carro
        eletric (bool): Se é elétrica - obrigatório para Moto
        
    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        if validatePlate(plate):
            return {'success': False, 'message': 'Veículo já existe!'}
        
        sessao = conectar()
        plate_upper = plate.strip().upper()
        
        # Criar novo veículo
        novo_veiculo = VeiculoDB(
            placa=plate_upper,
            modelo=model,
            cor=color,
            tipo=vehicle_type,
            tamanho=size if vehicle_type == "C" else None,
            eletrica=eletric if vehicle_type == "M" else None,
            vaga_atual=None
        )
        
        sessao.add(novo_veiculo)
        sessao.commit()
        sessao.close()
        
        return {'success': True, 'message': 'Veículo incluído com sucesso!'}
    except IntegrityError as e:
        return {'success': False, 'message': 'Erro de integridade nos dados'}
    except Exception as e:
        print(f"Erro ao criar veículo: {e}")
        return {'success': False, 'message': f'Erro ao criar veículo: {str(e)}'}

"""
    Função para buscar todas as estadias de um determinado veículo
"""
def getStays(plate: str) -> list: # função OK
    """
    Busca todas as estadias de um veículo.
    
    Args:
        plate (str): Placa do veículo
        
    Returns:
        list: Lista de objetos Estadia
    """
    try:
        if not validatePlate(plate):
            print("Placa não existe!")
            return []
        
        sessao = conectar()
        plate_upper = plate.strip().upper()
        
        estadias_db = (sessao.query(EstadiaDB)
                       .filter(EstadiaDB.placa == plate_upper)
                       .order_by(EstadiaDB.entrada.desc())
                       .all()) # Capta todos os registros para a placa
        
        estadias = []
        for estadia_db in estadias_db:
            # Transformar os atributos datetime em strings
            entrada_str = estadia_db.entrada.strftime('%d/%m/%Y %H:%M:%S') if estadia_db.entrada is not None else ""
            saida_str = estadia_db.saida.strftime('%d/%m/%Y %H:%M:%S') if estadia_db.saida is not None else ""
            
            estadia = Estadia(
                vaga=estadia_db.vaga,
                placa=estadia_db.placa,
                entrada=entrada_str,
                saida=saida_str
            )
            estadias.append(estadia)
        
        sessao.close()
        return estadias
    except Exception as e:
        print(f"Erro ao buscar estadias: {e}")
        return []
    
'''
    Função para listar todos os veículos/clientes
'''
def getVehicles() -> list: # função OK
    """
    Busca todos os veículos cadastrados.
    
    Returns:
        list: Lista de objetos Carro ou Moto
    """
    try:
        sessao = conectar()
        veiculos_db = sessao.query(VeiculoDB).all()
        
        veiculos = []
        for veiculo_db in veiculos_db:
            tipo_veiculo = str(veiculo_db.tipo)
            if tipo_veiculo == "C":
                veiculo = Carro(
                    placa=veiculo_db.placa,
                    modelo=veiculo_db.modelo,
                    cor=veiculo_db.cor,
                    status=veiculo_db.vaga_atual is not None,
                    tamanho=veiculo_db.tamanho
                )
            elif tipo_veiculo == "M":
                veiculo = Moto(
                    placa=veiculo_db.placa,
                    modelo=veiculo_db.modelo,
                    cor=veiculo_db.cor,
                    status=veiculo_db.vaga_atual is not None,
                    eletrica=veiculo_db.eletrica
                )
            else:
                continue
            
            veiculo.vaga = veiculo_db.vaga_atual
            veiculos.append(veiculo)
        
        sessao.close()
        return veiculos
    except Exception as e:
        print(f"Erro ao buscar veículos: {e}")
        return []

"""
    Função para atualizar o veículo
"""
def updateVehicle(plate: str, model: str | None = None, color: str | None = None, size: str | None = None, eletric: bool | None = None) -> dict:
    """
    Atualiza os dados de um veículo existente.
    
    Args:
        plate (str): Placa do veículo
        model (str): Novo modelo
        color (str): Nova cor
        size (str): Novo tamanho (para Carro)
        eletric (bool): Novo status elétrico (para Moto)
        
    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        if not validatePlate(plate):
            return {'success': False, 'message': 'Veículo não encontrado!'}
        
        sessao = conectar()
        plate_upper = plate.strip().upper()
        veiculo = sessao.query(VeiculoDB).filter(VeiculoDB.placa == plate_upper).first()
        
        if not veiculo:
            sessao.close()
            return {'success': False, 'message': 'Veículo não encontrado!'}
        
        # Atualizar campos
        if model:
            veiculo.modelo = model
        if color:
            veiculo.cor = color
        if size is not None and str(veiculo.tipo) == "C":
            veiculo.tamanho = size
        if eletric is not None and str(veiculo.tipo) == "M":
            veiculo.eletrica = eletric
        
        sessao.commit()
        sessao.close()
        
        return {'success': True, 'message': 'Veículo atualizado com sucesso!'}
    except Exception as e:
        print(f"Erro ao atualizar veículo: {e}")
        return {'success': False, 'message': f'Erro ao atualizar: {str(e)}'}
    
'''
    Função para deletar veículo
'''
def deleteVehicle(plate: str) -> dict:
    """
    Deleta um veículo do banco de dados (junto com suas estadias).
    
    Args:
        plate (str): Placa do veículo
        
    Returns:
        dict: {'success': bool, 'message': str}
    """
    try:
        if not validatePlate(plate):
            return {'success': False, 'message': 'Veículo não encontrado!'}
        
        sessao = conectar()
        plate_upper = plate.strip().upper()
        
        # Deletar estadias associadas
        sessao.query(EstadiaDB).filter(EstadiaDB.placa == plate_upper).delete()
        
        # Liberar vaga se estiver ocupada
        veiculo = sessao.query(VeiculoDB).filter(VeiculoDB.placa == plate_upper).first()
        if veiculo is not None and veiculo.vaga_atual is not None:
            vaga = sessao.query(Vaga).filter(Vaga.codigo == veiculo.vaga_atual).first()
            if vaga:
                vaga.ocupada = False
        
        # Deletar veículo
        sessao.query(VeiculoDB).filter(VeiculoDB.placa == plate_upper).delete()
        sessao.commit()
        sessao.close()
        
        return {'success': True, 'message': 'Veículo deletado com sucesso!'}
    except Exception as e:
        print(f"Erro ao deletar veículo: {e}")
        return {'success': False, 'message': f'Erro ao deletar: {str(e)}'}