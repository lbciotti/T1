from builtins import dict, int, list, print, str
from fileinput import input

from view.tela_base import TelaBase


class TelaClinicas(TelaBase):
    def menu_opcoes(self) -> int:
        self.mostrar_titulo("GERENCIAMENTO DE CLÍNICAS")
        print("1 - Incluir Clínica")
        print("2 - Ver Clínica (com Totais)")
        print("3 - Listar Todas as Clínicas")
        print("4 - Vincular Profissional à Clínica")
        print("0 - Retornar ao Menu Principal")
        return self.selecionar_opcao([1, 2, 3, 4, 0])

    def pegar_dados_clinica(self) -> dict:
        self.mostrar_titulo("CADASTRAR NOVA CLÍNICA")
        nome = input("Nome da Clínica: ").strip()
        localizacao = input("Localização/Endereço: ").strip()
        descricao = input("Descrição dos Serviços: ").strip()
        abertura_str = input("Horário de Abertura (HH:MM): ").strip()
        fechamento_str = input("Horário de Fechamento (HH:MM): ").strip()

        return {
            "nome": nome,
            "localizacao": localizacao,
            "descricao": descricao,
            "abertura_str": abertura_str,
            "fechamento_str": fechamento_str
        }

    def pedir_nome_clinica(self) -> str:
        return input("\nDigite o nome da clínica: ").strip()

    def pedir_dados_vinculo(self) -> dict:
        self.mostrar_titulo("VINCULAR PROFISSIONAL À CLÍNICA")
        nome_clinica = input("Nome da Clínica: ").strip()
        registro_prof = input("Registro do Profissional: ").strip()
        return {"nome_clinica": nome_clinica, "registro_profissional": registro_prof}

    def mostrar_detalhes_clinica(self, dados_detalhados: dict):
        clinica = dados_detalhados["clinica"]
        tot_prof = dados_detalhados["total_profissionais"]
        tot_atend = dados_detalhados["total_atendimentos"]

        self.mostrar_titulo(f"CLÍNICA: {clinica.nome}")
        print(f"Localização: {clinica.localizacao}")
        print(f"Descrição: {clinica.descricao}")
        print(f"Horário de Funcionamento: {clinica.horario_abertura.strftime('%H:%M')} às {clinica.horario_fechamento.strftime('%H:%M')}")
        print("-" * 50)
        print(f" Total de Profissionais Registrados: {tot_prof}")
        print(f" Total de Atendimentos Já Realizados: {tot_atend}")
        
        print("\nProfissionais na unidade:")
        if not clinica.profissionais:
            print(" Ninguém cadastrado nesta unidade.")
        else:
            for p in clinica.profissionais:
                print(f" - {p.nome} ({p.especialidade})")

    def mostrar_lista_clinicas(self, clinicas: list):
        self.mostrar_titulo("LISTA DE CLÍNICAS")
        if not clinicas:
            print("Nenhuma clínica cadastrada.")
            return

        for c in clinicas:
            print(f"• {c.nome} | Local: {c.localizacao} | Expediente: {c.horario_abertura.strftime('%H:%M')}-{c.horario_fechamento.strftime('%H:%M')}")