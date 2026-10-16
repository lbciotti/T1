from datetime import datetime, date
from models.paciente import Paciente
from view.tela_pacientes import TelaPacientes

class ControladorPacientes:
    def __init__(self, controlador_sistema):
        self.__pacientes = []
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaPacientes()

    def abrir_tela(self):
        opcoes = {1: self.incluir, 2: self.listar, 3: self.buscar_por_cpf, 4: self.excluir}
        while True:
            opcao = self.__tela.menu_opcoes()
            if opcao == 0: break
            opcoes[opcao]()

    def incluir(self):
        dados = self.__tela.pegar_dados_paciente()
        
        # --- VALIDAÇÃO DE CPF ÚNICO ---
        for p in self.__pacientes:
            if p.cpf == dados["cpf"]:
                self.__tela.mostrar_erro(f"Já existe um paciente cadastrado com o CPF '{dados['cpf']}'.")
                return
                
        try:
            data_formatada = datetime.strptime(dados["data_nascimento"], "%d/%m/%Y").date()
            
            # Tenta criar o paciente. Se a data for no futuro, o models/pessoa.py vai gritar um Erro!
            novo_paciente = Paciente(dados["nome"], data_formatada, dados["cpf"], dados["celular"])
            self.__pacientes.append(novo_paciente)
            self.__tela.mostrar_mensagem("Paciente cadastrado com sucesso!")
            
        except ValueError:
            self.__tela.mostrar_erro("Formato de data inválido. Use DD/MM/AAAA.")
        except Exception as e:
            self.__tela.mostrar_erro(str(e))
            
        except ValueError:
            self.__tela.mostrar_erro("Formato de data inválido. Use DD/MM/AAAA.")
        except Exception as e:
            # Captura a nossa Exception da máquina do tempo e mostra na tela
            self.__tela.mostrar_erro(str(e))

    def listar(self):
        if not self.__pacientes:
            self.__tela.mostrar_erro("Nenhum paciente cadastrado.")
            return
        print("\n--- LISTA DE PACIENTES ---")
        for p in self.__pacientes:
            self.__tela.mostrar_paciente({"nome": p.nome, "cpf": p.cpf, "celular": p.celular})

    def buscar_por_cpf(self):
        cpf = self.__tela.pegar_cpf()
        for p in self.__pacientes:
            if p.cpf == cpf:
                atendimentos_vinculados = [] # Será puxado do ControladorAtendimentos no futuro
                dados = {
                    "nome": p.nome, 
                    "cpf": p.cpf, 
                    "data_nascimento": p.data_nascimento.strftime("%d/%m/%Y"), 
                    "celular": p.celular
                }
                self.__tela.mostrar_detalhes_completos(dados, atendimentos_vinculados)
                return
        self.__tela.mostrar_erro("Paciente não encontrado.")

    def excluir(self):
        cpf = self.__tela.pegar_cpf()
        for p in self.__pacientes:
            if p.cpf == cpf:
                self.__pacientes.remove(p)
                self.__tela.mostrar_mensagem("Paciente removido!")
                return
        self.__tela.mostrar_erro("Paciente não encontrado.")