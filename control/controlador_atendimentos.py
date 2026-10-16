from datetime import datetime
from models.atendimento import Atendimento
from models.procedimento import Procedimento
from models.pagamento_pix import PagamentoPix
from models.pagamento_cartao import PagamentoCartao
from models.pagamento_dinheiro import PagamentoDinheiro
from view.tela_atendimentos import TelaAtendimentos

class ControladorAtendimentos:
    def __init__(self, controlador_sistema):
        self.__atendimentos = []
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaAtendimentos()

    @property
    def atendimentos(self) -> list:
        return self.__atendimentos

    def abrir_tela(self):
        opcoes = {1: self.agendar_atendimento, 2: self.listar, 3: self.buscar_por_numero}
        while True:
            opcao = self.__tela.menu_opcoes()
            if opcao == 0: break
            opcoes[opcao]()

    def agendar_atendimento(self):
        try:
            self.__tela.mostrar_titulo("NOVO AGENDAMENTO")
            
            # --- PASSO 1: CLÍNICA ---
            clinica_selecionada = self.__selecionar_clinica()
            if not clinica_selecionada: return

            # --- PASSO 2: DATA E HORA ---
            dados_dh = self.__tela.pegar_data_hora()
            data_atend = datetime.strptime(dados_dh["data"], "%d/%m/%Y").date()
            hora_atend = datetime.strptime(dados_dh["hora"], "%H:%M").time()

            # --- PASSO 3: PACIENTE ---
            paciente_selecionado = self.__selecionar_paciente()
            if not paciente_selecionado: return

            # --- PASSO 4: PROFISSIONAL ---
            profissional_selecionado = self.__selecionar_profissional(clinica_selecionada)
            if not profissional_selecionado: return

            # --- PASSO 5: TIPO E CUSTO DO ATENDIMENTO ---
            dados_atend = self.__tela.pegar_dados_atendimento()

            # GERAÇÃO DO NÚMERO SEQUENCIAL (Ex: 0001, 0002)
            novo_numero = f"{len(self.__atendimentos) + 1:04d}"

            # CRIAÇÃO DO ATENDIMENTO
            novo_atendimento = Atendimento(
                novo_numero, paciente_selecionado, profissional_selecionado, clinica_selecionada, 
                data_atend, hora_atend, dados_atend["tipo"]
            )
            
            proc_base = Procedimento(f"Atendimento: {dados_atend['tipo']}", dados_atend["custo"], profissional_selecionado)
            novo_atendimento.adicionar_procedimento(proc_base)

            # --- PASSO 6: PROCEDIMENTOS EXTRAS ---
            while self.__tela.perguntar_procedimento_extra():
                dados_proc = self.__tela.pegar_dados_procedimento()
                novo_proc = Procedimento(dados_proc["descricao"], dados_proc["custo"], profissional_selecionado)
                novo_atendimento.adicionar_procedimento(novo_proc)

            # --- PASSO 7: PAGAMENTO ---
            # Loop de validação para garantir que a data do pagamento seja igual ou anterior à consulta
            while True:
                dados_pag = self.__tela.pegar_dados_pagamento(
                    novo_atendimento.valor_total, 
                    paciente_selecionado.nome, 
                    paciente_selecionado.cpf
                )
                try:
                    data_pag = datetime.strptime(dados_pag["data"], "%d/%m/%Y").date()
                    
                    if data_pag > data_atend:
                        self.__tela.mostrar_erro(f"Regra de Negócio: O pagamento não pode ser registrado numa data posterior ao dia da consulta ({data_atend.strftime('%d/%m/%Y')}).")
                        continue # Volta a pedir os dados de pagamento
                        
                    break # Se chegou aqui, a data é válida
                except ValueError:
                    self.__tela.mostrar_erro("Formato de data inválido. Use DD/MM/AAAA.")
            
            # Construção do objeto de Pagamento consoante a escolha
            if dados_pag["forma"] == "PIX":
                pagamento = PagamentoPix(data_pag, novo_atendimento.valor_total, dados_pag["extras"]["cpf_pagador"])
            elif dados_pag["forma"] == "CARTAO":
                # Concatena o Crédito/Débito com a Bandeira para o modelo
                bandeira_completa = f"{dados_pag['extras']['tipo_cartao']} - {dados_pag['extras']['bandeira']}"
                pagamento = PagamentoCartao(
                    data_pag, 
                    novo_atendimento.valor_total, 
                    dados_pag["extras"]["numero_cartao"], 
                    bandeira_completa
                )
            else:
                pagamento = PagamentoDinheiro(data_pag, novo_atendimento.valor_total)
                
            novo_atendimento.adicionar_pagamento(pagamento)

            self.__atendimentos.append(novo_atendimento)
            self.__tela.mostrar_mensagem(f"Atendimento agendado com sucesso!\nO número deste atendimento é: {novo_numero}")

        except ValueError:
            self.__tela.mostrar_erro("Erro de formatação (data ou número inválido). Agendamento cancelado.")
        except Exception as e:
            self.__tela.mostrar_erro(f"Erro ao agendar: {str(e)}")

    def listar(self):
        if not self.__atendimentos:
            self.__tela.mostrar_erro("Nenhum atendimento registrado.")
            return
        
        self.__tela.mostrar_titulo("LISTA DE ATENDIMENTOS")
        for at in self.__atendimentos:
            dados = {
                "numero": at.numero,
                "data": at.data.strftime("%d/%m/%Y"),
                "hora": at.horario_inicio.strftime("%H:%M"),
                "clinica": at.clinica.nome,
                "paciente": at.paciente.nome,
                "profissional": at.profissional.nome,
                "tipo": at.tipo_atendimento,
                "valor": at.valor_total
            }
            self.__tela.mostrar_atendimento(dados)

    def buscar_por_numero(self):
        numero = self.__tela.capturar_numero_busca()
        for at in self.__atendimentos:
            if at.numero == numero:
                dados = {
                    "numero": at.numero,
                    "data": at.data.strftime("%d/%m/%Y"),
                    "hora": at.horario_inicio.strftime("%H:%M"),
                    "clinica": at.clinica.nome,
                    "paciente": at.paciente.nome,
                    "profissional": at.profissional.nome,
                    "tipo": at.tipo_atendimento,
                    "valor": at.valor_total
                }
                self.__tela.mostrar_titulo("DETALHES DO ATENDIMENTO")
                self.__tela.mostrar_atendimento(dados)
                return
        self.__tela.mostrar_erro("Atendimento não encontrado.")

    # ================= MÉTODOS AUXILIARES DE SELEÇÃO =================
    
    def __selecionar_clinica(self):
        ctrl_clinicas = self.__controlador_sistema.controlador_clinicas
        if not ctrl_clinicas._ControladorClinicas__clinicas:
            self.__tela.mostrar_erro("Não há clínicas cadastradas no sistema.")
            return None
            
        opcao = self.__tela.menu_selecao_entidade("Clínica")
        if opcao == 1:
            clinicas = ctrl_clinicas._ControladorClinicas__clinicas
            for idx, c in enumerate(clinicas, 1):
                print(f"{idx} - {c.nome} ({c.localizacao})")
            escolha = self.__tela.selecionar_da_lista(len(clinicas))
            return clinicas[escolha - 1] if escolha > 0 else None
        elif opcao == 2:
            nome = self.__tela.capturar_busca("Nome da Clínica")
            for c in ctrl_clinicas._ControladorClinicas__clinicas:
                if c.nome.lower() == nome.lower(): return c
            self.__tela.mostrar_erro("Clínica não encontrada.")
        return None

    def __selecionar_paciente(self):
        ctrl_pacientes = self.__controlador_sistema.controlador_pacientes
        if not ctrl_pacientes._ControladorPacientes__pacientes:
            self.__tela.mostrar_erro("Não há pacientes cadastrados no sistema.")
            return None
            
        opcao = self.__tela.menu_selecao_entidade("Paciente")
        if opcao == 1:
            pacientes = ctrl_pacientes._ControladorPacientes__pacientes
            for idx, p in enumerate(pacientes, 1):
                print(f"{idx} - {p.nome} (CPF: {p.cpf})")
            escolha = self.__tela.selecionar_da_lista(len(pacientes))
            return pacientes[escolha - 1] if escolha > 0 else None
        elif opcao == 2:
            cpf = self.__tela.capturar_busca("CPF do Paciente")
            for p in ctrl_pacientes._ControladorPacientes__pacientes:
                if p.cpf == cpf: return p
            self.__tela.mostrar_erro("Paciente não encontrado.")
        return None

    def __selecionar_profissional(self, clinica):
        if not clinica.profissionais:
            self.__tela.mostrar_erro(f"Não há profissionais vinculados à clínica {clinica.nome}.")
            return None
            
        opcao = self.__tela.menu_selecao_entidade("Profissional")
        if opcao == 1:
            profissionais = clinica.profissionais
            print(f"\nProfissionais da Clínica {clinica.nome}:")
            for idx, p in enumerate(profissionais, 1):
                print(f"{idx} - {p.nome} (Registro: {p.registro_profissional})")
            escolha = self.__tela.selecionar_da_lista(len(profissionais))
            return profissionais[escolha - 1] if escolha > 0 else None
        elif opcao == 2:
            registro = self.__tela.capturar_busca("Registro do Profissional")
            for p in clinica.profissionais:
                if p.registro_profissional == registro: return p
            self.__tela.mostrar_erro("Profissional não encontrado nesta clínica.")
        return None
    
    