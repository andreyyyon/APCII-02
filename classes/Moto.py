from Veiculo import Veiculo

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