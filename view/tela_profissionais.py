from view.tela_base import TelaBase
from builtins import ValueError, dict, float, int, list, print, str
from fileinput import input



class TelaProfissionais(TelaBase):
    def menu_opcoes(self) -> int:
        self.mostrar_titulo("GERENCIAMENTO DE PROFISSIONAIS")
        print("1 - Incluir Profissional")
        print("2 - Ver Profissional (com Clínicas)")
        print("3 - Listar Todos os Profissionais")
        print("4 - Excluir Profissional")
        print("0 - Retornar ao Menu Principal")
        return self.selecionar_opcao([1, 2, 3, 4, 0])

    def pegar_dados_profissional(self) -> dict:
        self.mostrar_titulo("CADASTRAR NOVO PROFISSIONAL")
        nome = input("Nome: ").strip()
        data_nasc_str = input("Data de Nascimento (DD/MM/AAAA): ").strip()
        cpf = input("CPF: ").strip()
        celular = input("Celular: ").strip()
        especialidade = input("Especialidade: ").strip()
        registro = input("Registro Profissional (ex: CRM/CRO): ").strip()

        return {
            "nome": nome,
            "data_nascimento_str": data_nasc_str,
            "cpf": cpf,
            "celular": celular,
            "especialidade": especialidade,
            "registro_profissional": registro
        }

    def pedir_registro(self) -> str:
        return input("\nDigite o Registro Profissional: ").strip()

    def mostrar_detalhes_profissional(self, dados_detalhados: dict):
        prof = dados_detalhados["profissional"]
        clinicas = dados_detalhados["clinicas"]

        self.mostrar_titulo(f"PROFISSIONAL: {prof.nome}")
        print(f"Registro: {prof.registro_profissional}")
        print(f"Especialidade: {prof.especialidade}")
        print(f"CPF: {prof.cpf} | Fone: {prof.celular}")
        
        print("\n--- CLÍNICAS VINCULADAS ---")
        if not clinicas:
            print("Este profissional não está vinculado a nenhuma clínica no momento.")
        else:
            for c in clinicas:
                print(f"• {c.nome} - Local: {c.localizacao}")

    def mostrar_lista_profissionais(self, lista_com_clinicas: list):
        self.mostrar_titulo("LISTA DE PROFISSIONAIS")
        if not lista_com_clinicas:
            print("Nenhum profissional cadastrado.")
            return

        for item in lista_com_clinicas:
            prof = item["profissional"]
            clinicas = item["clinicas"]
            nomes_clinicas = ", ".join([c.nome for c in clinicas]) if clinicas else "Sem vinculo"
            
            print(f"• {prof.nome} ({prof.especialidade}) | Reg: {prof.registro_profissional}")
            print(f"  Clínicas onde atua: {nomes_clinicas}")