from builtins import Exception, dict, len, list, property, str, sum

from models.clinica import Clinica


class ControladorClinicas:
    def __init__(self, controlador_sistema):
        self.__clinicas = []
        self.__controlador_sistema = controlador_sistema

    @property
    def clinicas(self) -> list:
        return self.__clinicas

    def buscar_clinica_por_nome(self, nome: str) -> Clinica:
        for clinica in self.__clinicas:
            if clinica.nome.lower() == nome.lower():
                return clinica
        return None

    def incluir_clinica(self, nome: str, localizacao: str, descricao: str, abertura, fechamento) -> Clinica:
        if self.buscar_clinica_por_nome(nome) is not None:
            raise Exception(f"Já existe uma clínica cadastrada com o nome '{nome}'.")

        nova_clinica = Clinica(nome, localizacao, descricao, abertura, fechamento)
        self.__clinicas.append(nova_clinica)
        return nova_clinica

    def vincular_profissional(self, nome_clinica: str, registro_profissional: str):
        clinica = self.buscar_clinica_por_nome(nome_clinica)
        if clinica is None:
            raise Exception("Clínica não encontrada.")

        prof = self.__controlador_sistema.controlador_profissionais.buscar_profissional_por_registro(registro_profissional)
        if prof is None:
            raise Exception("Profissional não encontrado.")

        clinica.adicionar_profissional(prof)

    def obter_detalhes_clinica(self, nome: str) -> dict:
        """Retorna a clínica com o total de profissionais e total de atendimentos realizados"""
        clinica = self.buscar_clinica_por_nome(nome)
        if clinica is None:
            raise Exception("Clínica não encontrada.")

        total_profissionais = len(clinica.profissionais)

        atendimentos = self.__controlador_sistema.controlador_atendimentos.atendimentos
        total_atendimentos = sum(1 for at in atendimentos if at.clinica == clinica)

        return {
            "clinica": clinica,
            "total_profissionais": total_profissionais,
            "total_atendimentos": total_atendimentos
        }