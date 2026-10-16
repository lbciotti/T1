from datetime import datetime
from models.clinica import Clinica
from view.tela_clinicas import TelaClinicas

class ControladorClinicas:
    def __init__(self, controlador_sistema):
        self.__clinicas = []
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaClinicas()

    def abrir_tela(self):
        opcoes = {
            1: self.incluir, 
            2: self.listar, 
            3: self.buscar_por_nome, 
            4: self.excluir, 
            5: self.vincular_profissional
        }
        while True:
            opcao = self.__tela.menu_opcoes()
            if opcao == 0: break
            opcoes[opcao]()

    def incluir(self):
        dados = self.__tela.pegar_dados_clinica()
        
        # --- VALIDAÇÃO DE NOME ÚNICO ---
        for c in self.__clinicas:
            if c.nome.lower() == dados["nome"].lower():
                self.__tela.mostrar_erro(f"Já existe uma clínica cadastrada com o nome '{dados['nome']}'.")
                return
                
        try:
            hr_abertura = datetime.strptime(dados["horario_abertura"], "%H:%M").time()
            hr_fechamento = datetime.strptime(dados["horario_fechamento"], "%H:%M").time()
            
            nova_clinica = Clinica(
                dados["nome"], 
                dados["localizacao"], 
                dados["descricao"], 
                hr_abertura, 
                hr_fechamento
            )
            self.__clinicas.append(nova_clinica)
            self.__tela.mostrar_mensagem("Clínica cadastrada com sucesso!")
        except ValueError:
            self.__tela.mostrar_erro("Formato de hora inválido. Use HH:MM (ex: 08:00).")

    def listar(self):
        if not self.__clinicas:
            self.__tela.mostrar_erro("Nenhuma clínica cadastrada.")
            return
        print("\n--- LISTA DE CLÍNICAS ---")
        for c in self.__clinicas:
            self.__tela.mostrar_clinica({"nome": c.nome, "localizacao": c.localizacao})

    def buscar_por_nome(self):
        nome = self.__tela.pegar_nome()
        for c in self.__clinicas:
            if c.nome.lower() == nome.lower(): 
                profissionais_vinculados = c.profissionais 
                
                todos_atendimentos = self.__controlador_sistema.controlador_atendimentos.atendimentos
                atendimentos_da_clinica = [at for at in todos_atendimentos if at.clinica == c]
                total_atendimentos = len(atendimentos_da_clinica)
                
                dados = {
                    "nome": c.nome, 
                    "localizacao": c.localizacao, 
                    "descricao": c.descricao,
                    "horario_abertura": c.horario_abertura.strftime("%H:%M"),
                    "horario_fechamento": c.horario_fechamento.strftime("%H:%M")
                }
                
                while True:
                    opcao = self.__tela.mostrar_detalhes(dados, profissionais_vinculados, total_atendimentos)
                    if opcao == 1:
                        # --- DETALHES DE ATENDIMENTOS (Ordem decrescente) ---
                        atendimentos_invertidos = list(reversed(atendimentos_da_clinica))
                        lista_dados_atendimentos = []
                        
                        for at in atendimentos_invertidos:
                            procs = [{"descricao": p.descricao, "custo": p.custo} for p in at.procedimentos]
                            
                            pags = []
                            for pag in at.pagamentos:
                                forma_nome = pag.__class__.__name__.replace("Pagamento", "").upper()
                                pags.append({
                                    "forma": forma_nome,
                                    "data": pag.data.strftime("%d/%m/%Y"),
                                    "valor_pago": pag.valor_pago
                                })

                            dados_at = {
                                "numero": at.numero,
                                "data": at.data.strftime("%d/%m/%Y"),
                                "hora": at.horario_inicio.strftime("%H:%M"),
                                "paciente": at.paciente.nome,
                                "profissional": at.profissional.nome,
                                "tipo": at.tipo_atendimento,
                                "valor": at.valor_total,
                                "procedimentos": procs,
                                "pagamentos": pags
                            }
                            lista_dados_atendimentos.append(dados_at)
                        
                        self.__tela.mostrar_atendimentos_clinica(lista_dados_atendimentos)
                    elif opcao == 0:
                        break
                return
        self.__tela.mostrar_erro("Clínica não encontrada.")

    def excluir(self):
        nome = self.__tela.pegar_nome()
        for c in self.__clinicas:
            if c.nome.lower() == nome.lower():
                self.__clinicas.remove(c)
                self.__tela.mostrar_mensagem("Clínica removida!")
                return
        self.__tela.mostrar_erro("Clínica não encontrada.")

    def vincular_profissional(self):
        # 1. Selecionar Clínica (com listagem)
        if not self.__clinicas:
            self.__tela.mostrar_erro("Não há clínicas cadastradas.")
            return

        opcao_clinica = self.__tela.menu_selecao_entidade("Clínica")
        clinica_encontrada = None
        
        if opcao_clinica == 1:
            print("\nClínicas Cadastradas:")
            for idx, c in enumerate(self.__clinicas, 1):
                print(f"{idx} - {c.nome} ({c.localizacao})")
            escolha = self.__tela.selecionar_da_lista(len(self.__clinicas))
            if escolha == 0: return
            clinica_encontrada = self.__clinicas[escolha - 1]
        elif opcao_clinica == 2:
            nome_clinica = self.__tela.capturar_busca("Nome da Clínica")
            for c in self.__clinicas:
                if c.nome.lower() == nome_clinica.lower():
                    clinica_encontrada = c
                    break
            if not clinica_encontrada:
                self.__tela.mostrar_erro("Clínica não encontrada.")
                return
        else:
            return
            
        # 2. Selecionar Profissional (com listagem)
        ctrl_profissionais = self.__controlador_sistema.controlador_profissionais
        profissionais = ctrl_profissionais._ControladorProfissionais__profissionais
        
        if not profissionais:
            self.__tela.mostrar_erro("Não há profissionais cadastrados no sistema.")
            return

        opcao_prof = self.__tela.menu_selecao_entidade("Profissional")
        profissional_encontrado = None
        
        if opcao_prof == 1:
            print("\nProfissionais Cadastrados:")
            for idx, p in enumerate(profissionais, 1):
                print(f"{idx} - {p.nome} (Registro: {p.registro_profissional})")
            escolha = self.__tela.selecionar_da_lista(len(profissionais))
            if escolha == 0: return
            profissional_encontrado = profissionais[escolha - 1]
        elif opcao_prof == 2:
            registro_prof = self.__tela.capturar_busca("Registro do Profissional")
            for p in profissionais:
                if p.registro_profissional == registro_prof:
                    profissional_encontrado = p
                    break
            if not profissional_encontrado:
                self.__tela.mostrar_erro("Profissional não encontrado.")
                return
        else:
            return
            
        # 3. Vincular e salvar
        clinica_encontrada.adicionar_profissional(profissional_encontrado)
        self.__tela.mostrar_mensagem(f"Profissional '{profissional_encontrado.nome}' vinculado à clínica '{clinica_encontrada.nome}' com sucesso!")