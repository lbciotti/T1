from view.tela_base import TelaBase

class TelaRelatorios(TelaBase):
    def menu_opcoes(self) -> int:
        self.mostrar_titulo("RELATÓRIOS GERENCIAIS")
        print("1 - Clínicas com maior número de atendimentos")
        print("2 - Atendimentos: Análise de Custos")
        print("3 - Procedimentos mais realizados (populares)")
        print("4 - Procedimentos mais caros e mais baratos")
        print("0 - Retornar ao Menu Principal")
        return self.selecionar_opcao([1, 2, 3, 4, 0])

    def menu_analise_custos(self) -> int:
        self.mostrar_titulo("ANÁLISE DE CUSTOS DE ATENDIMENTO")
        print("1 - Comparar custos por Tipo Específico de atendimento")
        print("2 - Comparar média total de preços entre Clínicas")
        print("0 - Voltar")
        return self.selecionar_opcao([1, 2, 0])

    def selecionar_tipo_atendimento(self, tipos: list) -> str:
        self.mostrar_titulo("TIPOS DE ATENDIMENTO REGISTRADOS")
        for idx, tipo in enumerate(tipos, 1):
            print(f"{idx} - {tipo}")
        print("0 - Cancelar")
        
        while True:
            try:
                escolha = int(input("\nEscolha o número do tipo de atendimento: "))
                if escolha == 0:
                    return None
                if 1 <= escolha <= len(tipos):
                    return tipos[escolha - 1]
                print("Opção inválida.")
            except ValueError:
                print("Digite um número válido.")

    def exibir_ranking_simples(self, titulo: str, ranking: list, texto_complemento: str):
        self.mostrar_titulo(titulo)
        if not ranking:
            print("Sem dados suficientes para gerar este relatório.")
            return
        for pos, (item, valor) in enumerate(ranking, 1):
            print(f"{pos}º Lugar: {item} - {valor} {texto_complemento}")

    def exibir_ranking_valores(self, titulo: str, ranking: list):
        self.mostrar_titulo(titulo)
        if not ranking:
            print("Sem dados suficientes para gerar este relatório.")
            return
        for pos, (item, valor) in enumerate(ranking, 1):
            print(f"{pos}º Lugar: {item} -> R$ {valor:.2f}")

    def exibir_comparacao_tipo_atendimento(self, tipo: str, ranking: list):
        self.mostrar_titulo(f"COMPARAÇÃO DE CUSTO: {tipo.upper()}")
        if not ranking:
            print("Nenhum atendimento deste tipo foi encontrado.")
            return
        print("Do mais barato para o mais caro:\n")
        for pos, item in enumerate(ranking, 1):
            print(f"{pos}º - Clínica: {item['clinica']} | Valor: R$ {item['valor']:.2f} (Atendimento Nº {item['numero']})")