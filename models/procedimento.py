from models.profissional import Profissional


class Procedimento:
    def __init__(self, descricao: str, custo: float, profissional_responsavel: Profissional):
        self.__descricao = descricao
        self.__custo = custo
        self.__profissional_responsavel = profissional_responsavel

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @property
    def custo(self) -> float:
        return self.__custo

    @custo.setter
    def custo(self, custo: float):
        self.__custo = custo

    @property
    def profissional_responsavel(self) -> Profissional:
        return self.__profissional_responsavel

    @profissional_responsavel.setter
    def profissional_responsavel(self, profissional: Profissional):
        self.__profissional_responsavel = profissional