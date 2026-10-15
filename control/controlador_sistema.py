from builtins import print, property

from control.controlador_pacientes import ControladorPacientes
from control.controlador_profissionais import ControladorProfissionais
from control.controlador_clinicas import ControladorClinicas
from control.controlador_atendimentos import ControladorAtendimentos
from control.controlador_relatorios import ControladorRelatorios
from view.tela_principal import TelaPrincipal


class ControladorSistema:
    def __init__(self):
        self.__tela_principal = TelaPrincipal()
        self.__controlador_pacientes = ControladorPacientes(self)
        self.__controlador_profissionais = ControladorProfissionais(self)
        self.__controlador_clinicas = ControladorClinicas(self)
        self.__controlador_atendimentos = ControladorAtendimentos(self)
        self.__controlador_relatorios = ControladorRelatorios(self)

    @property
    def controlador_pacientes(self) -> ControladorPacientes:
        return self.__controlador_pacientes

    @property
    def controlador_profissionais(self) -> ControladorProfissionais:
        return self.__controlador_profissionais

    @property
    def controlador_clinicas(self) -> ControladorClinicas:
        return self.__controlador_clinicas

    @property
    def controlador_atendimentos(self) -> ControladorAtendimentos:
        return self.__controlador_atendimentos

    @property
    def controlador_relatorios(self) -> ControladorRelatorios:
        return self.__controlador_relatorios

    def inicializar_sistema(self):
        """Loop do Menu Principal do Sistema"""
        opcoes = {
            1: self.__controlador_pacientes.abre_tela,
            2: self.__controlador_profissionais.abre_tela,
            3: self.__controlador_clinicas.abre_tela,
            4: self.__controlador_atendimentos.abre_tela,
            5: self.__controlador_relatorios.abre_tela,
        }

        while True:
            opcao_escolhida = self.__tela_principal.menu_opcoes()

            if opcao_escolhida == 0:
                print("\nEncerrando o sistema de gestão de clínicas... Até logo!")
                break

            funcao_controle = opcoes.get(opcao_escolhida)
            if funcao_controle:
                funcao_controle()