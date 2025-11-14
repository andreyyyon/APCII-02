import datetime

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
    def register_entry(self):
        agora = datetime.datetime.now()
        self._entrada = agora.strftime('%d/%m/%Y %H:%M:%S')

    # Método para registrar a saída
    def register_out(self):
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