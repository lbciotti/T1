from datetime import date, time
from models.atendimento import Atendimento
from models.procedimento import Procedimento
from models.pagamento_pix import PagamentoPix
from models.pagamento_cartao import PagamentoCartao
from models.pagamento_dinheiro import PagamentoDinheiro


class ControladorAtendimentos:
    def __init__(self, controlador_sistema):
        self.__atendimentos = []
        self.__controlador_sistema = controlador_sistema

    @property
    def atendimentos(self) -> list:
        return self.__atendimentos

    def agendar_atendimento(self, paciente, profissional, clinica, data: date, horario_inicio: time, tipo_atendimento: str):
        # Validação de Maioridade do Paciente (Regra do PDF)
        if not paciente.e_maior_de_idade():
            raise Exception("Pacientes menores de 18 anos não podem agendar atendimentos de forma independente.")

        # Validação de Funcionamento da Clínica (Utiliza o método exato de clinica.py)
        if not clinica.esta_em_funcionamento(horario_inicio):
            raise Exception(f"O horário {horario_inicio} está fora do expediente da clínica ({clinica.horario_abertura} às {clinica.horario_fechamento}).")

        novo_atendimento = Atendimento(paciente, profissional, clinica, data, horario_inicio, tipo_atendimento)
        self.__atendimentos.append(novo_atendimento)
        return novo_atendimento

    def adicionar_procedimento_ao_atendimento(self, atendimento: Atendimento, descricao: str, custo: float, profissional):
        """Cria um procedimento e associa diretamente ao atendimento"""
        novo_procedimento = Procedimento(descricao, custo, profissional)
        atendimento.adicionar_procedimento(novo_procedimento)
        return novo_procedimento

    def registrar_pagamento(self, atendimento: Atendimento, forma_pagamento: str, valor: float, **dados_extras):
        hoje = date.today()

        if hoje > atendimento.data:
            raise Exception("Não é possível registrar pagamentos após a data do atendimento.")

        forma = forma_pagamento.upper()
        if forma == "PIX":
            pagamento = PagamentoPix(data=hoje, valor_pago=valor, cpf_pagador=dados_extras.get("cpf_pagador"))
        elif forma == "CARTAO":
            pagamento = PagamentoCartao(data=hoje, valor_pago=valor, numero_cartao=dados_extras.get("numero_cartao"), bandeira=dados_extras.get("bandeira"))
        else:
            pagamento = PagamentoDinheiro(data=hoje, valor_pago=valor)

        atendimento.adicionar_pagamento(pagamento)
        return pagamento