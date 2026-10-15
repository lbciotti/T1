from models.profissional import Profissional


class ControladorProfissionais:
    def __init__(self, controlador_sistema):
        self.__profissionais = []
        self.__controlador_sistema = controlador_sistema

    @property
    def profissionais(self) -> list:
        return self.__profissionais

    def buscar_profissional_por_registro(self, registro_profissional: str) -> Profissional:
        for prof in self.__profissionais:
            if prof.registro_profissional == registro_profissional:
                return prof
        return None

    def incluir_profissional(self, nome: str, data_nascimento, cpf: str, celular: str,
                             especialidade: str, registro_profissional: str) -> Profissional:
        if self.buscar_profissional_por_registro(registro_profissional) is not None:
            raise Exception(f"Já existe um profissional cadastrado com o registro {registro_profissional}.")

        novo_prof = Profissional(nome, data_nascimento, cpf, celular, especialidade, registro_profissional)
        self.__profissionais.append(novo_prof)
        return novo_prof

    def excluir_profissional(self, registro_profissional: str):
        prof = self.buscar_profissional_por_registro(registro_profissional)
        if prof is None:
            raise Exception("Profissional não encontrado.")
        self.__profissionais.remove(prof)

    def obter_clinicas_do_profissional(self, profissional: Profissional) -> list:
        """Retorna as clínicas às quais o profissional está vinculado"""
        clinicas = self.__controlador_sistema.controlador_clinicas.clinicas
        return [c for c in clinicas if profissional in c.profissionais]

    def obter_detalhes_profissional(self, registro_profissional: str) -> dict:
        """Retorna o profissional e suas clínicas vinculadas"""
        prof = self.buscar_profissional_por_registro(registro_profissional)
        if prof is None:
            raise Exception("Profissional não encontrado.")

        clinicas_vinculadas = self.obter_clinicas_do_profissional(prof)

        return {
            "profissional": prof,
            "clinicas": clinicas_vinculadas
        }

    def listar_profissionais_com_clinicas(self) -> list:
        """Retorna a lista estruturada de profissionais com suas clínicas para a View"""
        resultado = []
        for prof in self.__profissionais:
            clinicas = self.obter_clinicas_do_profissional(prof)
            resultado.append({
                "profissional": prof,
                "clinicas": clinicas
            })
        return resultado