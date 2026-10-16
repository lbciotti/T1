from view.tela_base import TelaBase

class TelaAtendimentos(TelaBase):
    def menu_opcoes(self) -> int:
        self.mostrar_titulo("GERENCIAMENTO DE ATENDIMENTOS")
        print("1 - Agendar Novo Atendimento")
        print("2 - Listar Todos os Atendimentos")
        print("3 - Buscar Atendimento por Número")
        print("0 - Retornar")
        return self.selecionar_opcao([1, 2, 3, 0])

    def menu_selecao_entidade(self, entidade: str) -> int:
        print(f"\n--- SELECIONAR {entidade.upper()} ---")
        print(f"1 - Listar {entidade}s cadastrados para escolher")
        print(f"2 - Buscar {entidade} por identificador (Nome/CPF/Registro)")
        print("0 - Cancelar agendamento")
        return self.selecionar_opcao([1, 2, 0])

    def capturar_busca(self, tipo: str) -> str:
        return input(f"Digite o {tipo} para busca: ")
        
    def capturar_numero_busca(self) -> str:
        return input("\nDigite o número do atendimento (ex: 0001): ").strip()

    def selecionar_da_lista(self, max_opcoes: int) -> int:
        while True:
            try:
                escolha = int(input(f"Digite o número correspondente (1 a {max_opcoes}) ou 0 para cancelar: "))
                if 0 <= escolha <= max_opcoes:
                    return escolha
                print("Número fora do intervalo.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

    def pegar_data_hora(self) -> dict:
        print("\n--- DATA E HORA ---")
        data = input("Data do Atendimento (DD/MM/AAAA): ")
        hora = input("Horário de Início (HH:MM): ")
        return {"data": data, "hora": hora}

    def pegar_dados_atendimento(self) -> dict:
        print("\n--- DADOS DO ATENDIMENTO ---")
        tipo = input("Tipo de atendimento (Ex: Consulta, Retorno, Exame): ")
        while True:
            try:
                custo = float(input("Custo base do atendimento (R$): "))
                break
            except ValueError:
                print("Por favor, digite um valor numérico válido.")
        return {"tipo": tipo, "custo": custo}

    def perguntar_procedimento_extra(self) -> bool:
        while True:
            resp = input("\nHaverá algum procedimento extra neste atendimento? (S/N): ").upper()
            if resp == 'S': return True
            if resp == 'N': return False

    def pegar_dados_procedimento(self) -> dict:
        print("\n--- PROCEDIMENTO EXTRA ---")
        descricao = input("Descrição do procedimento: ")
        while True:
            try:
                custo = float(input("Custo do procedimento (R$): "))
                break
            except ValueError:
                print("Por favor, digite um valor numérico válido.")
        return {"descricao": descricao, "custo": custo}

    def pegar_dados_pagamento(self, total: float, paciente_nome: str, paciente_cpf: str) -> dict:
        print("\n" + "=" * 40)
        print(f"VALOR TOTAL A PAGAR: R$ {total:.2f}")
        print("=" * 40)
        print("--- PAGAMENTO ---")
        print("Formas de Pagamento disponíveis:")
        print("1 - PIX")
        print("2 - CARTÃO")
        print("3 - DINHEIRO")
        
        opcao = self.selecionar_opcao([1, 2, 3])
        formas = {1: "PIX", 2: "CARTAO", 3: "DINHEIRO"}
        forma_escolhida = formas[opcao]
        
        dados_extras = {}
        
        if forma_escolhida == "PIX":
            while True:
                resp = input(f"Deseja utilizar o CPF {paciente_cpf} do cliente {paciente_nome}? (S/N): ").strip().upper()
                if resp == 'S':
                    dados_extras["cpf_pagador"] = paciente_cpf
                    break
                elif resp == 'N':
                    dados_extras["cpf_pagador"] = input("Digite o CPF do pagador PIX: ").strip()
                    break
                print("Opção inválida. Digite S ou N.")
                
        elif forma_escolhida == "CARTAO":
            while True:
                tipo = input("Crédito ou Débito? (C/D): ").strip().upper()
                if tipo in ['C', 'D']:
                    dados_extras["tipo_cartao"] = "Crédito" if tipo == 'C' else "Débito"
                    break
                print("Opção inválida. Digite C ou D.")
            
            dados_extras["numero_cartao"] = input("Número do Cartão: ").strip()
            dados_extras["bandeira"] = input("Bandeira do Cartão (Visa, Mastercard, etc): ").strip()
            
        # Dinheiro vai direto para a data
        data_pagamento = input("Data do Pagamento (DD/MM/AAAA): ")
        
        return {"forma": forma_escolhida, "data": data_pagamento, "extras": dados_extras}

    def mostrar_atendimento(self, dados: dict):
        print(f"\n[ATENDIMENTO Nº {dados['numero']}] Data: {dados['data']} {dados['hora']} | Clínica: {dados['clinica']}")
        print(f"    Paciente: {dados['paciente']} | Profissional: {dados['profissional']}")
        print(f"    Tipo: {dados['tipo']} | Valor Total: R$ {dados['valor']:.2f}")