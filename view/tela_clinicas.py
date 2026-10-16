from view.tela_base import TelaBase

class TelaClinicas(TelaBase):
    def menu_opcoes(self) -> int:
        self.mostrar_titulo("GERENCIAMENTO DE CLÍNICAS")
        print("1 - Incluir Clínica")
        print("2 - Listar Clínicas")
        print("3 - Buscar Clínica por Nome (Detalhes)")
        print("4 - Excluir Clínica")
        print("5 - Vincular Profissional à Clínica")
        print("0 - Retornar")
        return self.selecionar_opcao([1, 2, 3, 4, 5, 0])

    def pegar_dados_clinica(self) -> dict:
        self.mostrar_titulo("INCLUIR NOVA CLÍNICA")
        print("Digite os dados da clínica:")
        nome = input("Nome da Clínica: ")
        localizacao = input("Localização/Endereço: ")
        descricao = input("Descrição (Ex: Clínica Geral, Fisioterapia): ")
        horario_abertura = input("Horário de Abertura (HH:MM): ")
        horario_fechamento = input("Horário de Fechamento (HH:MM): ")
        
        return {
            "nome": nome, 
            "localizacao": localizacao, 
            "descricao": descricao, 
            "horario_abertura": horario_abertura, 
            "horario_fechamento": horario_fechamento
        }

    def pegar_nome(self) -> str:
        return input("\nDigite o Nome da clínica: ")
        
    def mostrar_clinica(self, dados: dict):
        print(f"Nome: {dados['nome']} | Localização: {dados['localizacao']}")

    def mostrar_detalhes(self, clinica: dict, profissionais: list, total_atendimentos: int) -> int:
        self.mostrar_titulo("DETALHES DA CLÍNICA")
        print(f"Nome: {clinica['nome']}")
        print(f"Localização: {clinica['localizacao']}")
        print(f"Descrição: {clinica['descricao']}")
        print(f"Horário de Funcionamento: {clinica['horario_abertura']} às {clinica['horario_fechamento']}")
        print(f"Total de Atendimentos Realizados: {total_atendimentos}")
        
        print("\n--- Profissionais Vinculados ---")
        if len(profissionais) == 0:
            print("Nenhum profissional vinculado a esta clínica.")
        else:
            for prof in profissionais:
                print(f"- {prof.nome} (Registro: {prof.registro_profissional} | Especialidade: {prof.especialidade})") 
                
        print("\n" + "=" * 40)
        print("1 - Mostrar detalhes dos atendimentos")
        print("0 - Voltar")
        return self.selecionar_opcao([1, 0])
        
    # --- NOVOS MÉTODOS PARA SELEÇÃO E EXIBIÇÃO ---
    
    def menu_selecao_entidade(self, entidade: str) -> int:
        print(f"\n--- SELECIONAR {entidade.upper()} ---")
        print(f"1 - Listar {entidade}s cadastrados para escolher")
        print(f"2 - Buscar {entidade} por identificador (Nome ou Registro)")
        print("0 - Cancelar")
        return self.selecionar_opcao([1, 2, 0])

    def capturar_busca(self, tipo: str) -> str:
        return input(f"Digite o {tipo} para busca: ")

    def selecionar_da_lista(self, max_opcoes: int) -> int:
        while True:
            try:
                escolha = int(input(f"Digite o número correspondente (1 a {max_opcoes}) ou 0 para cancelar: "))
                if 0 <= escolha <= max_opcoes:
                    return escolha
                print("Número fora do intervalo.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

    def mostrar_atendimentos_clinica(self, lista_dados: list):
        self.mostrar_titulo("HISTÓRICO DE ATENDIMENTOS DA CLÍNICA")
        if not lista_dados:
            print("Nenhum atendimento registrado para esta clínica.")
            return
        
        for dados in lista_dados:
            print(f"\n[ATENDIMENTO Nº {dados['numero']}] Data: {dados['data']} às {dados['hora']}")
            print(f"    Paciente: {dados['paciente']} | Profissional: {dados['profissional']}")
            print(f"    Tipo: {dados['tipo']}")
            print("    Procedimentos:")
            for proc in dados['procedimentos']:
                print(f"      - {proc['descricao']}: R$ {proc['custo']:.2f}")
            print(f"    Total do Atendimento: R$ {dados['valor']:.2f}")
            print("    Pagamentos Realizados:")
            for pag in dados['pagamentos']:
                print(f"      - Forma: {pag['forma']} | Data: {pag['data']} | Valor: R$ {pag['valor_pago']:.2f}")
            print("-" * 55)