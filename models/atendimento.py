from datetime import date, time
from models.paciente import Paciente
from models.profissional import Profissional
from models.clinica import Clinica
from models.procedimento import Procedimento
from models.pagamento import Pagamento


class Atendimento:
    def __init__(self, paciente: Paciente, profissional: Profissional, clinica: Clinica, 
                 data: date, horario_inicio: time, tipo_atendimento: str):
        self.__paciente = paciente
        self.__profissional = profissional
        self.__clinica = clinica
        self.__data = data
        self.__horario_inicio = horario_inicio
        self.__tipo_atendimento = tipo_atendimento
        
        # Composições: listas que iniciam vazias e recebem os objetos vinculados
        self.__procedimentos = []  # Lista de objetos Procedimento
        self.__pagamentos = []     # Lista de objetos Pagamento (Pix, Cartao, Dinheiro)

    @property
    def paciente(self) -> Paciente:
        return self.__paciente

    @paciente.setter
    def paciente(self, paciente: Paciente):
        self.__paciente = paciente

    @property
    def profissional(self) -> Profissional:
        return self.__profissional

    @profissional.setter
    def profissional(self, profissional: Profissional):
        self.__profissional = profissional

    @property
    def clinica(self) -> Clinica:
        return self.__clinica

    @clinica.setter
    def clinica(self, clinica: Clinica):
        self.__clinica = clinica

    @property
    def data(self) -> date:
        return self.__data

    @data.setter
    def data(self, data: date):
        self.__data = data

    @property
    def horario_inicio(self) -> time:
        return self.__horario_inicio

    @horario_inicio.setter
    def horario_inicio(self, horario_inicio: time):
        self.__horario_inicio = horario_inicio

    @property
    def tipo_atendimento(self) -> str:
        return self.__tipo_atendimento

    @tipo_atendimento.setter
    def tipo_atendimento(self, tipo_atendimento: str):
        self.__tipo_atendimento = tipo_atendimento

    @property
    def procedimentos(self) -> list:
        return self.__procedimentos

    @property
    def pagamentos(self) -> list:
        return self.__pagamentos

    def adicionar_procedimento(self, procedimento: Procedimento):
        if isinstance(procedimento, Procedimento) and procedimento not in self.__procedimentos:
            self.__procedimentos.append(procedimento)

    def remover_procedimento(self, procedimento: Procedimento):
        if procedimento in self.__procedimentos:
            self.__procedimentos.remove(procedimento)

    def adicionar_pagamento(self, pagamento: Pagamento):
        if isinstance(pagamento, Pagamento):
            self.__pagamentos.append(pagamento)

    @property
    def valor_total(self) -> float:
        """Soma dinamicamente os custos de todos os procedimentos realizados no atendimento"""
        return sum(procedimento.custo for procedimento in self.__procedimentos)

    @property
    def total_pago(self) -> float:
        """Soma todos os pagamentos efetuados (totais ou parciais)"""
        return sum(pagamento.valor_pago for pagamento in self.__pagamentos)

    def calcular_valor_restante(self) -> float:
        """Retorna o saldo devedor pendente para quitacao do atendimento"""
        return self.valor_total - self.total_pago