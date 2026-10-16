from abc import ABC, abstractmethod
from datetime import date

class Pessoa(ABC):
    def __init__(self, nome: str, data_nascimento: date, cpf: str, celular: str):
        self.__nome = nome
        # Passa pelo setter para ativar as validações de futuro e de maioridade
        self.data_nascimento = data_nascimento 
        self.__cpf = cpf
        self.__celular = celular
        
    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def data_nascimento(self) -> date:
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: date):
        hoje = date.today()
        
        # 1. Validação do futuro
        if data_nascimento > hoje:
            raise Exception("A data de nascimento não pode estar no futuro!")
            
        # 2. Validação da maioridade (Bloqueia o cadastro na raiz)
        idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
        if idade < 18:
            raise Exception("O sistema não permite o cadastro de pessoas menores de 18 anos.")
            
        self.__data_nascimento = data_nascimento

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str):
        self.__cpf = cpf

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, celular: str):
        self.__celular = celular

    def e_maior_de_idade(self) -> bool:
        """Calcula a idade dinâmica com base na data atual e verifica maioridade (18 anos)"""
        hoje = date.today()
        idade = hoje.year - self.__data_nascimento.year - (
            (hoje.month, hoje.day) < (self.__data_nascimento.month, self.__data_nascimento.day)
        )
        return idade >= 18