from view.tela_relatorios import TelaRelatorios

class ControladorRelatorios:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela = TelaRelatorios()

    def abrir_tela(self):
        opcoes = {
            1: self.relatorio_clinicas_mais_atendimentos,
            2: self.relatorio_analise_custos,
            3: self.relatorio_procedimentos_populares,
            4: self.relatorio_procedimentos_custos
        }
        
        while True:
            opcao = self.__tela.menu_opcoes()
            if opcao == 0:
                break
            opcoes[opcao]()

    def obter_atendimentos(self):
        return self.__controlador_sistema.controlador_atendimentos.atendimentos

    def relatorio_clinicas_mais_atendimentos(self):
        atendimentos = self.obter_atendimentos()
        if not atendimentos:
            self.__tela.mostrar_erro("Não há atendimentos registrados para gerar o relatório.")
            return

        contagem_clinicas = {}
        for at in atendimentos:
            nome_clinica = at.clinica.nome
            contagem_clinicas[nome_clinica] = contagem_clinicas.get(nome_clinica, 0) + 1

        # Ordena do maior para o menor número de atendimentos
        ranking = sorted(contagem_clinicas.items(), key=lambda x: x[1], reverse=True)
        self.__tela.exibir_ranking_simples("CLÍNICAS COM MAIS ATENDIMENTOS", ranking, "atendimento(s)")

    def relatorio_analise_custos(self):
        atendimentos = self.obter_atendimentos()
        if not atendimentos:
            self.__tela.mostrar_erro("Não há atendimentos registrados para gerar o relatório.")
            return

        while True:
            opcao = self.__tela.menu_analise_custos()
            if opcao == 0:
                break
                
            elif opcao == 1: # Comparar por Tipo
                tipos_unicos = list(set([at.tipo_atendimento for at in atendimentos]))
                tipo_escolhido = self.__tela.selecionar_tipo_atendimento(tipos_unicos)
                
                if tipo_escolhido:
                    # Filtra apenas os atendimentos desse tipo
                    filtrados = [at for at in atendimentos if at.tipo_atendimento == tipo_escolhido]
                    
                    dados_comparacao = []
                    for at in filtrados:
                        dados_comparacao.append({
                            "clinica": at.clinica.nome,
                            "valor": at.valor_total,
                            "numero": at.numero
                        })
                    
                    # Ordena do mais barato para o mais caro
                    ranking = sorted(dados_comparacao, key=lambda x: x['valor'])
                    self.__tela.exibir_comparacao_tipo_atendimento(tipo_escolhido, ranking)
                    
            elif opcao == 2: # Média por Clínica
                soma_clinicas = {}
                contagem_clinicas = {}
                
                for at in atendimentos:
                    nome = at.clinica.nome
                    soma_clinicas[nome] = soma_clinicas.get(nome, 0.0) + at.valor_total
                    contagem_clinicas[nome] = contagem_clinicas.get(nome, 0) + 1
                
                medias = []
                for nome in soma_clinicas:
                    media = soma_clinicas[nome] / contagem_clinicas[nome]
                    medias.append((nome, media))
                
                # Ordena da média mais barata para a mais cara
                ranking = sorted(medias, key=lambda x: x[1])
                self.__tela.exibir_ranking_valores("MÉDIA DE PREÇOS POR CLÍNICA", ranking)

    def relatorio_procedimentos_populares(self):
        atendimentos = self.obter_atendimentos()
        if not atendimentos:
            self.__tela.mostrar_erro("Não há atendimentos registrados para gerar o relatório.")
            return

        contagem_procedimentos = {}
        for at in atendimentos:
            for proc in at.procedimentos:
                desc = proc.descricao
                contagem_procedimentos[desc] = contagem_procedimentos.get(desc, 0) + 1

        # Ordena do mais realizado para o menos realizado
        ranking = sorted(contagem_procedimentos.items(), key=lambda x: x[1], reverse=True)
        self.__tela.exibir_ranking_simples("PROCEDIMENTOS MAIS REALIZADOS", ranking, "vez(es)")

    def relatorio_procedimentos_custos(self):
        atendimentos = self.obter_atendimentos()
        if not atendimentos:
            self.__tela.mostrar_erro("Não há atendimentos registrados para gerar o relatório.")
            return

        custos_procedimentos = {}
        for at in atendimentos:
            for proc in at.procedimentos:
                # Mantém o custo associado à descrição. 
                # (Se houver variação de preço para o mesmo nome, guarda o valor mais recente ou mantém como registro único)
                custos_procedimentos[proc.descricao] = proc.custo

        # Ordena do mais caro para o mais barato
        ranking_caros = sorted(custos_procedimentos.items(), key=lambda x: x[1], reverse=True)
        self.__tela.exibir_ranking_valores("RANKING DE PROCEDIMENTOS (MAIS CAROS)", ranking_caros)
        
        # Pode imprimir também os mais baratos invertendo a lista na tela, mas o ranking_caros já mostra tudo.