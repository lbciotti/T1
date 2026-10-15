from view.tela_relatorios import TelaRelatorios

class ControladorRelatorios:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_relatorios = TelaRelatorios()

    def abrir_tela(self):
        opcoes = {
            1: self.emitir_relatorio_atendimentos,
            2: self.emitir_relatorio_faturamento,
            0: self.retornar
        }

        while True:
            opcao = self.__tela_relatorios.tela_opcoes()
            funcao_escolhida = opcoes.get(opcao)
            if funcao_escolhida:
                funcao_escolhida()

    def emitir_relatorio_atendimentos(self):
        # Lógica para buscar os atendimentos e enviar para a tela
        pass

    def emitir_relatorio_faturamento(self):
        # Lógica para buscar faturamento e enviar para a tela
        pass

    def retornar(self):
        self.__controlador_sistema.abrir_tela()