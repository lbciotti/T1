from datetime import datetime
from models.profissional import Profissional
from view.tela_profissionais import TelaProfissionais

class ControladorProfissionais:
    def __init__(self, controlador_sistema):
        self.__profissionais = []
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaProfissionais()

    def abrir_tela(self):
        opcoes = {1: self.incluir, 2: self.listar, 3: self.buscar_por_registro, 4: self.excluir}
        while True:
            opcao = self.__tela.menu_opcoes()
            if opcao == 0: break
            opcoes[opcao]()

    def incluir(self):
        dados = self.__tela.pegar_dados_profissional()
        
        # --- VALIDAÇÃO DE CPF E REGISTRO ÚNICOS ---
        for p in self.__profissionais:
            if p.cpf == dados["cpf"]:
                self.__tela.mostrar_erro(f"Já existe um profissional cadastrado com o CPF '{dados['cpf']}'.")
                return
            if p.registro_profissional == dados["registro"]:
                self.__tela.mostrar_erro(f"Já existe um profissional cadastrado com o Registro '{dados['registro']}'.")
                return
                
        try:
            data_formatada = datetime.strptime(dados["data_nascimento"], "%d/%m/%Y").date()
            
            novo_profissional = Profissional(
                dados["nome"], 
                data_formatada, 
                dados["cpf"], 
                dados["celular"], 
                dados["especialidade"], 
                dados["registro"]
            )
            self.__profissionais.append(novo_profissional)
            self.__tela.mostrar_mensagem("Profissional cadastrado com sucesso!")
            
        except ValueError:
            self.__tela.mostrar_erro("Formato de data inválido. Use DD/MM/AAAA.")
        except Exception as e:
            self.__tela.mostrar_erro(str(e))
            
        
    def listar(self):
        if not self.__profissionais:
            self.__tela.mostrar_erro("Nenhum profissional cadastrado.")
            return
        print("\n--- LISTA DE PROFISSIONAIS ---")
        for p in self.__profissionais:
            # Corrigido para acessar a propriedade exata do Model: p.registro_profissional
            self.__tela.mostrar_profissional({
                "nome": p.nome, 
                "registro": p.registro_profissional, 
                "especialidade": p.especialidade
            })

    def buscar_por_registro(self):
        registro = self.__tela.pegar_registro()
        for p in self.__profissionais:
            # Corrigido para p.registro_profissional
            if p.registro_profissional == registro:
                clinicas_vinculadas = [] 
                atendimentos_recentes = [] 
                
                dados = {
                    "nome": p.nome, 
                    "registro": p.registro_profissional, 
                    "especialidade": p.especialidade
                }
                self.__tela.mostrar_detalhes(dados, clinicas_vinculadas, atendimentos_recentes)
                return
        self.__tela.mostrar_erro("Profissional não encontrado.")

    def excluir(self):
        registro = self.__tela.pegar_registro()
        for p in self.__profissionais:
            # Corrigido para p.registro_profissional
            if p.registro_profissional == registro:
                self.__profissionais.remove(p)
                self.__tela.mostrar_mensagem("Profissional removido!")
                return
        self.__tela.mostrar_erro("Profissional não encontrado.")