"""
    {Python} class Veiculo
    Classe principal para representar um veículo em um estacionamento.

    @propertys
    String Private - placa      Chave primaria do veículo
    String Private - modelo     Modelo  do veículo
    String Private - cor        Cor do veículo
    String Private - tipo       Tipo do veículo
"""

class Veiculo():
    def __init__(self, placa, modelo, cor, tipo, status):
        self._placa = placa
        self._modelo = modelo
        self._cor = cor
        self._tipo = tipo
        self._status = status

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
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, tipo):
            self._tipo = tipo
    
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
            self._tipo = status
