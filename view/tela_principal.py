from builtins import int, print

from view.tela_base import TelaBase


class TelaPrincipal(TelaBase):
    def menu_opcoes(self) -> int:
        self.mostrar_titulo("SISTEMA DE GESTÃO DE CLÍNICAS")
        print("1 - Gerenciar Pacientes")
        print("2 - Gerenciar Profissionais")
        print("3 - Gerenciar Clínicas")
        print("4 - Gerenciar Atendimentos")
        print("5 - Relatórios Gerenciais")
        print("0 - Sair do Sistema")
        return self.selecionar_opcao([1, 2, 3, 4, 5, 0])