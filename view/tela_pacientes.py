from view.tela_base import TelaBase

class TelaPacientes(TelaBase):
    def menu_opcoes(self) -> int:
        self.mostrar_titulo("GERENCIAMENTO DE PACIENTES")
        print("1 - Incluir Paciente")
        print("2 - Listar Pacientes")
        print("3 - Buscar Paciente por CPF (Detalhes)")
        print("4 - Excluir Paciente")
        print("0 - Retornar")
        return self.selecionar_opcao([1, 2, 3, 4, 0])

    def pegar_dados_paciente(self) -> dict:
        self.mostrar_titulo("INCLUIR NOVO PACIENTE")
        nome = input("Nome: ")
        cpf = input("CPF: ")
        data_nascimento = input("Data de Nascimento: ")
        celular = input("Celular: ")
        return {"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "celular": celular}

    def pegar_cpf(self) -> str:
        return input("\nDigite o CPF do paciente: ")

    def mostrar_paciente(self, dados: dict):
        print(f"Nome: {dados['nome']} | CPF: {dados['cpf']} | Celular: {dados['celular']}")

    def mostrar_detalhes_completos(self, paciente: dict, atendimentos: list):
        self.mostrar_titulo("DETALHES DO PACIENTE")
        print(f"Nome: {paciente['nome']}")
        print(f"CPF: {paciente['cpf']}")
        print(f"Nascimento: {paciente['data_nascimento']}")
        print(f"Celular: {paciente['celular']}")
        
        print("\n--- Atendimentos Recentes ---")
        if len(atendimentos) == 0:
            print("Nenhum atendimento registrado no sistema.")
        else:
            for at in atendimentos:
                print(f"- {at}") # Mostrará os atendimentos no futuro