from datetime import date
from models.pessoa import Pessoa

class Paciente(Pessoa):
    def __init__(self, nome: str, data_nascimento: date, cpf: str, celular: str):
        super().__init__(nome, data_nascimento, cpf, celular)
