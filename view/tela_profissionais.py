from view.tela_base import TelaBase

class TelaProfissionais(TelaBase):
    def menu_opcoes(self) -> int:
        self.mostrar_titulo("GERENCIAMENTO DE PROFISSIONAIS")
        print("1 - Incluir Profissional")
        print("2 - Listar Profissionais")
        print("3 - Buscar Profissional por Registro")
        print("4 - Excluir Profissional")
        print("0 - Retornar")
        return self.selecionar_opcao([1, 2, 3, 4, 0])

    def pegar_dados_profissional(self) -> dict:
        self.mostrar_titulo("INCLUIR NOVO PROFISSIONAL")
        print("Digite os dados do profissional passo a passo:")
        nome = input("Nome: ")
        cpf = input("CPF: ")
        data_nascimento = input("Data de Nascimento (DD/MM/AAAA): ")
        celular = input("Celular: ")
        registro = input("Registro Profissional (ex: CRM, CRO): ")
        especialidade = input("Especialidade: ")
        
        return {
            "nome": nome, 
            "cpf": cpf, 
            "data_nascimento": data_nascimento, 
            "celular": celular, 
            "registro": registro, 
            "especialidade": especialidade
        }

    def pegar_registro(self) -> str:
        return input("\nDigite o Registro Profissional: ")

    def mostrar_profissional(self, dados: dict):
        print(f"Nome: {dados['nome']} | Registro: {dados['registro']} | Especialidade: {dados['especialidade']}")

    def mostrar_detalhes(self, prof: dict, clinicas: list, atendimentos: list):
        self.mostrar_titulo("DETALHES DO PROFISSIONAL")
        print(f"Nome: {prof['nome']}")
        print(f"Registro: {prof['registro']}")
        print(f"Especialidade: {prof['especialidade']}")
        
        print("\n--- Hospitais/Clínicas Vinculados ---")
        if len(clinicas) == 0:
            print("Não vinculado a nenhuma clínica.")
        else:
            for c in clinicas: print(f"- {c}")
            
        print("\n--- Atendimentos Recentes ---")
        if len(atendimentos) == 0:
            print("Nenhum atendimento recente.")
        else:
            for a in atendimentos: print(f"- {a}")