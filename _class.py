import datetime
import _data 
import pytz

"""
    {Python} class Veiculo
    Classe principal para representar um veículo em um estacionamento.

    @propertys
    String Private - placa      Chave primaria do veículo
    String Private - modelo     Modelo  do veículo
    String Private - cor        Cor do veículo
    String Private - vaga       Vaga que o veículo está ocupando
"""

class Veiculo():
    def __init__(self, placa, modelo, cor, vaga):
        self._placa = placa
        self._modelo = modelo
        self._cor = cor
        self._vaga = vaga

    @property
    def placa(self):
        return self._placa

    @placa.setter
    def placa(self, placa):
            self._placa = placa

    @property
    def modelo(self):
        return self._modelo

    @modelo.setter
    def modelo(self, modelo):
            self._modelo = modelo

    @property
    def cor(self):
        return self._cor

    @cor.setter
    def cor(self, cor):
            self._cor = cor

    @property
    def vaga(self):
        return self._vaga

    @vaga.setter
    def vaga(self, vaga):
            self._vaga = vaga

    """
        @staticmethod é um decorator em Python que transforma um método em uma 
        função utilitária que pertence à classe, mas que não tem acesso nem à 
        instância da classe (o 'self').

        Ou seja, ela funciona de maneira indepente, util para buscas do seu 
        escopo global.
    """

    @staticmethod
    def buscar_por_placa(placa: str): # Método estático para buscar um veículo pela placa na lista global
        placa = placa.strip().upper()

        for cliente in _data.clientes:
            if cliente.placa == placa:
                return cliente
        return None

"""
    {Python} class Carro
    Subclasse que representa um carro.

    @propertys
    String Private - tamanho    Porte do veículo (M ou G)
"""

class Carro(Veiculo):    
    def __init__(self, placa, modelo, cor, vaga, tamanho):
        super().__init__(placa, modelo, cor, vaga)
        self._tamanho = tamanho

    @property
    def tamanho(self):
        return self._tamanho

    @tamanho.setter
    def tamanho(self, novo_tamanho):
        self._tamanho = novo_tamanho

"""
    {Python} class Moto
    Subclasse que representa uma moto.

    @propertys
    String Boolean - eletrica   Moto é elétrica? (True - Sim / False - Não)
"""

class Moto(Veiculo):    
    def __init__(self, placa, modelo, cor, vaga, eletrica):
        super().__init__(placa, modelo, cor, vaga)
        
        self._eletrica = eletrica

    @property
    def eletrica(self):
        return self._eletrica

    @eletrica.setter
    def eletrica(self, eletrica):
        self._eletrica = eletrica

"""
    {Python} class Estadia
    Classe principal para representar as estadias em um estacionamento.

    @propertys
    String Private - vaga        Vaga utilizada	
    String Private - placa       Placa do carro que utilizou a vaga		
    String Private - entrada     Data e hora da entrada
    String Private - saida       Data e hora da saida
"""

class Estadia():
    def __init__(self, vaga, placa, entrada, saida):
        self._vaga = vaga
        self._placa = placa
        self._entrada = entrada
        self._saida = saida
    
    # Método para registrar a entrada
    def registrar_entrada(self):
        agora = datetime.datetime.now()
        self._entrada = agora.strftime('%d/%m/%Y %H:%M:%S')

    # Método para registrar a saída
    def registrar_saida(self):
        agora = datetime.datetime.now()
        self._saida = agora.strftime('%d/%m/%Y %H:%M:%S')

    @property
    def vaga(self):
        return self._vaga

    @vaga.setter
    def vaga(self, vaga):
            self._vaga = vaga

    @property
    def placa(self):
        return self._placa

    @placa.setter
    def placa(self, placa):
            self._placa = placa

    @property
    def entrada(self):
        return self._entrada

    @entrada.setter
    def entrada(self, entrada):
            self._entrada = entrada
    
    @property
    def saida(self):
        return self._saida

    @saida.setter
    def saida(self, saida):
            self._saida = saida