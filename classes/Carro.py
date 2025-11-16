from classes.Veiculo import Veiculo

"""
    {Python} class Carro
    Subclasse que representa um carro.

    @propertys
    String Private - tamanho    Porte do veículo (M ou G)
"""

class Carro(Veiculo):    
    def __init__(self, placa, modelo, cor, status, tamanho):
        super().__init__(placa, modelo, cor, "C", status)
        self._tamanho = tamanho

    @property
    def tamanho(self):
        return self._tamanho

    @tamanho.setter
    def tamanho(self, novo_tamanho):
        self._tamanho = novo_tamanho