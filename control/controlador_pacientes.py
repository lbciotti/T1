from builtins import Exception, dict, list, property, str

from models.paciente import Paciente


class ControladorPacientes:
    def __init__(self, controlador_sistema):
        self.__pacientes = []
        self.__controlador_sistema = controlador_sistema

    @property
    def pacientes(self) -> list:
        return self.__pacientes

    def buscar_paciente_por_cpf(self, cpf: str) -> Paciente:
        for paciente in self.__pacientes:
            if paciente.cpf == cpf:
                return paciente
        return None

    def incluir_paciente(self, nome: str, data_nascimento: str, cpf: str, celular: str):
        if self.buscar_paciente_por_cpf(cpf) is not None:
            raise Exception(f"Já existe um paciente cadastrado com o CPF {cpf}.")

        # Correção: O construtor agora recebe os 4 parâmetros exigidos pelo Model
        novo_paciente = Paciente(nome, data_nascimento, cpf, celular)
        self.__pacientes.append(novo_paciente)
        return novo_paciente

    def excluir_paciente(self, cpf: str):
        paciente = self.buscar_paciente_por_cpf(cpf)
        if paciente is None:
            raise Exception("Paciente não encontrado.")
        self.__pacientes.remove(paciente)

    def obter_detalhes_paciente(self, cpf: str) -> dict:
        """Retorna os dados do paciente com o histórico detalhado de atendimentos"""
        paciente = self.buscar_paciente_por_cpf(cpf)
        if paciente is None:
            raise Exception("Paciente não encontrado.")

        atendimentos_sistema = self.__controlador_sistema.controlador_atendimentos.atendimentos
        historico_atendimentos = [at for at in atendimentos_sistema if at.paciente == paciente]

        return {
            "paciente": paciente,
            "historico_atendimentos": historico_atendimentos
        }