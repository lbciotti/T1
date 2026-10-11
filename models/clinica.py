from datetime import time
from models.profissional import Profissional


class Clinica:
    def __init__(self, nome: str, localizacao: str, descricao: str, 
                 horario_abertura: time, horario_fechamento: time):
        self.__nome = nome
        self.__localizacao = localizacao
        self.__descricao = descricao
        self.__horario_abertura = horario_abertura
        self.__horario_fechamento = horario_fechamento
        self.__profissionais = []  # Agregação: Lista de profissionais cadastrados na clínica

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def localizacao(self) -> str:
        return self.__localizacao

    @localizacao.setter
    def localizacao(self, localizacao: str):
        self.__localizacao = localizacao

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @property
    def horario_abertura(self) -> time:
        return self.__horario_abertura

    @horario_abertura.setter
    def horario_abertura(self, horario_abertura: time):
        self.__horario_abertura = horario_abertura

    @property
    def horario_fechamento(self) -> time:
        return self.__horario_fechamento

    @horario_fechamento.setter
    def horario_fechamento(self, horario_fechamento: time):
        self.__horario_fechamento = horario_fechamento

    @property
    def profissionais(self) -> list:
        return self.__profissionais

    def adicionar_profissional(self, profissional: Profissional):
        # Verifica se a pessoa a ser adicionada é de fato um profissional, e se já está ou não 
        # cadastrada na clinicxa
        if isinstance(profissional, Profissional) and profissional not in self.__profissionais:
            self.__profissionais.append(profissional)

    def remover_profissional(self, profissional: Profissional):
        if profissional in self.__profissionais:
            self.__profissionais.remove(profissional)

    # Verifica se um determinado horario está em horario de funcionamento da clinica
    def esta_em_funcionamento(self, horario) -> bool:
        return self.__horario_abertura <= horario <= self.__horario_fechamento