from threading import enumerate

from view.tela_base import TelaBase
from builtins import ValueError, dict, float, int, list, print, str
from fileinput import input



class TelaRelatorios(TelaBase):
    def menu_opcoes(self) -> int:
        self.mostrar_titulo("RELATÓRIOS GERENCIAIS")
        print("1 - Clínicas com maior número de atendimentos")
        print("2 - Atendimentos mais caros e mais baratos")
        print("3 - Procedimentos mais realizados (populares)")
        print("4 - Procedimentos mais caros e mais baratos")
        print("0 - Retornar ao Menu Principal")
        return self.selecionar_opcao([1, 2, 3, 4, 0])

    def exibir_clinicas_mais_atendimentos(self, ranking: list):
        self.mostrar_titulo("RANKING DE CLÍNICAS POR ATENDIMENTOS")
        if not ranking:
            print("Sem dados de atendimentos registrados.")
            return

        for pos, (clinica, qtd) in enumerate(ranking, 1):
            print(f"{pos}º Lugar: {clinica.nome} - Total: {qtd} atendimento(s)")

    def exibir_atendimentos_por_valor(self, dados: dict):
        self.mostrar_titulo("ATENDIMENTOS POR FAIXA DE VALOR")
        caros = dados["mais_caros"]
        baratos = dados["mais_baratos"]

        print("\n--- ATENDIMENTO(S) MAIS CARO(S) ---")
        if not caros:
            print("Sem dados.")
        for at in caros:
            print(f"• Paciente: {at.paciente.nome} | Clínica: {at.clinica.nome} | Valor: R$ {at.valor_total:.2f}")

        print("\n--- ATENDIMENTO(S) MAIS BARATO(S) ---")
        if not baratos:
            print("Sem dados.")
        for at in baratos:
            print(f"• Paciente: {at.paciente.nome} | Clínica: {at.clinica.nome} | Valor: R$ {at.valor_total:.2f}")

    def exibir_procedimentos_mais_realizados(self, ranking: list):
        self.mostrar_titulo("PROCEDIMENTOS MAIS REALIZADOS")
        if not ranking:
            print("Nenhum procedimento foi realizado ainda.")
            return

        for pos, (nome_proc, qtd) in enumerate(ranking, 1):
            print(f"{pos}º - {nome_proc}: Realizado {qtd} vez(es)")

    def exibir_procedimentos_por_custo(self, dados: dict):
        self.mostrar_titulo("PROCEDIMENTOS POR CUSTO")
        caros = dados["mais_caros"]
        baratos = dados["mais_baratos"]

        print("\n--- PROCEDIMENTO(S) DE MAIOR CUSTO ---")
        if not caros:
            print("Sem dados.")
        for p in caros:
            print(f"• {p.descricao} | Custo: R$ {p.custo:.2f}")

        print("\n--- PROCEDIMENTO(S) DE MENOR CUSTO ---")
        if not baratos:
            print("Sem dados.")
        for p in baratos:
            print(f"• {p.descricao} | Custo: R$ {p.custo:.2f}")