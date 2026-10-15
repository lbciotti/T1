from builtins import dict, int, list, print
from fileinput import input
from threading import enumerate

from view.tela_base import TelaBase


class TelaAtendimentos(TelaBase):
    def menu_opcoes(self) -> int:
        self.mostrar_titulo("GERENCIAMENTO DE ATENDIMENTOS")
        print("1 - Agendar Atendimento")
        print("2 - Adicionar Procedimento a um Atendimento")
        print("3 - Registrar Pagamento")
        print("4 - Listar Todos os Atendimentos")
        print("0 - Retornar ao Menu Principal")
        return self.selecionar_opcao([1, 2, 3, 4, 0])

    def pegar_dados_agendamento(self) -> dict:
        self.mostrar_titulo("AGENDAR ATENDIMENTO")
        cpf_paciente = input("CPF do Paciente: ").strip()
        registro_prof = input("Registro do Profissional: ").strip()
        nome_clinica = input("Nome da Clínica: ").strip()
        data_str = input("Data do Atendimento (DD/MM/AAAA): ").strip()
        horario_str = input("Horário de Início (HH:MM): ").strip()
        tipo_atendimento = input("Tipo do Atendimento (ex: Consulta/Retorno): ").strip()

        return {
            "cpf_paciente": cpf_paciente,
            "registro_profissional": registro_prof,
            "nome_clinica": nome_clinica,
            "data_str": data_str,
            "horario_str": horario_str,
            "tipo_atendimento": tipo_atendimento
        }

    def pegar_dados_procedimento(self) -> dict:
        self.mostrar_titulo("ADICIONAR PROCEDIMENTO")
        idx_atendimento = int(input("Número/Índice do Atendimento (1, 2, ...): ")) - 1
        descricao = input("Descrição do Procedimento: ").strip()
        custo = self.ler_float("Custo do Procedimento (R$): ")
        registro_prof = input("Registro do Profissional Responsável: ").strip()

        return {
            "idx_atendimento": idx_atendimento,
            "descricao": descricao,
            "custo": custo,
            "registro_profissional": registro_prof
        }

    def pegar_dados_pagamento(self) -> dict:
        self.mostrar_titulo("REGISTRAR PAGAMENTO")
        idx_atendimento = int(input("Número/Índice do Atendimento (1, 2, ...): ")) - 1
        print("\nFormas de Pagamento: 1-PIX | 2-CARTAO | 3-DINHEIRO")
        opcao_forma = self.selecionar_opcao([1, 2, 3])

        valor = self.ler_float("Valor Pago (R$): ")
        
        dados_extras = {}
        forma_map = {1: "PIX", 2: "CARTAO", 3: "DINHEIRO"}
        forma_escolhida = forma_map[opcao_forma]

        if forma_escolhida == "PIX":
            dados_extras["cpf_pagador"] = input("CPF do Pagador Pix: ").strip()
        elif forma_escolhida == "CARTAO":
            dados_extras["numero_cartao"] = input("Número do Cartão: ").strip()
            dados_extras["bandeira"] = input("Bandeira do Cartão: ").strip()

        return {
            "idx_atendimento": idx_atendimento,
            "forma_pagamento": forma_escolhida,
            "valor": valor,
            "dados_extras": dados_extras
        }

    def mostrar_lista_atendimentos(self, atendimentos: list):
        self.mostrar_titulo("TODOS OS ATENDIMENTOS REGISTRADOS")
        if not atendimentos:
            print("Nenhum atendimento cadastrado no sistema.")
            return

        for idx, at in enumerate(atendimentos, 1):
            print(f"\n[{idx}] Data: {at.data.strftime('%d/%m/%Y')} {at.horario_inicio.strftime('%H:%M')} | Clínica: {at.clinica.nome}")
            print(f"    Paciente: {at.paciente.nome} | Profissional: {at.profissional.nome}")
            print(f"    Total: R$ {at.valor_total:.2f} | Pago: R$ {at.total_pago:.2f} | Devedor: R$ {at.calcular_valor_restante():.2f}")