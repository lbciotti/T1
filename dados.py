import random
from datetime import date, time, timedelta
from models.paciente import Paciente
from models.profissional import Profissional
from models.clinica import Clinica
from models.atendimento import Atendimento
from models.procedimento import Procedimento
from models.pagamento_pix import PagamentoPix
from models.pagamento_cartao import PagamentoCartao
from models.pagamento_dinheiro import PagamentoDinheiro
from control.controlador_sistema import ControladorSistema

def popular_e_iniciar():
    print("A preparar a base de dados massiva... Injetando 1000 atendimentos.")
    sistema = ControladorSistema()
    
    # 1. GERAR PACIENTES (150 Pacientes)
    nomes_p = ["Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel", "Helena", "Igor", "Julia", "Lucas", "Mariana", "Nicolas", "Olivia", "Pedro"]
    sobrenomes_p = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira", "Lima", "Gomes"]
    
    pacientes_obj = []
    for i in range(150):
        nome = f"{random.choice(nomes_p)} {random.choice(sobrenomes_p)}"
        cpf = f"{10000000000 + i}"
        celular = f"489{10000000 + i}"
        dias_vida = random.randint(18 * 365, 80 * 365)
        nascimento = date.today() - timedelta(days=dias_vida)
        
        p = Paciente(nome, nascimento, cpf, celular)
        pacientes_obj.append(p)
        sistema.controlador_pacientes._ControladorPacientes__pacientes.append(p)

    # 2. GERAR PROFISSIONAIS (20 Profissionais cômicos)
    nomes_medicos = [
        "Seu Madruga", "Dona Florinda", "Professor Girafales", "Quico", "Chiquinha",
        "Nhonho", "Dona Clotilde (Bruxa do 7)", "Jaiminho o Carteiro", "Senhor Barriga", "Godínez",
        "Chapolin Colorado", "Doutor Chapatin", "Julius Rock", "Walter White", "Meredith Grey",
        "Gregory House Brasileiro", "Agostinho Carrara", "Beiçola", "Lineu Silva", "Bojack Horseman"
    ]
    especialidades = ["Clínico Geral", "Cardiologia", "Dermatologia", "Ortopedia", "Pediatria", "Psiquiatria", "Neurologia", "Oftalmologia", "Medicina de Família", "Cirurgia Geral"]
    
    profissionais_obj = []
    for i, nome_personagem in enumerate(nomes_medicos):
        nome = f"Dr(a). {nome_personagem}"
        cpf = f"{20000000000 + i}"
        celular = f"489{20000000 + i}"
        registro = f"CRM{1000 + i}"
        especialidade = random.choice(especialidades)
        nascimento = date.today() - timedelta(days=random.randint(30 * 365, 70 * 365))
        
        prof = Profissional(nome, nascimento, cpf, celular, especialidade, registro)
        profissionais_obj.append(prof)
        sistema.controlador_profissionais._ControladorProfissionais__profissionais.append(prof)

    # 3. GERAR CLÍNICAS (Hospitais locais)
    dados_clinicas = [
        ("Hospital Universitário (HU - UFSC)", "Trindade, Florianópolis", "Hospital Público de Ensino"),
        ("Hospital Unimed", "Kobrasol, São José", "Hospital Particular de Referência"),
        ("Hospital Baía Sul", "Centro, Florianópolis", "Alta Complexidade e Cirurgias"),
        ("SOS Cárdio", "SC-401, Florianópolis", "Especializado em Cardiologia e Emergências"),
        ("Clínica São Lucas", "Centro, Florianópolis", "Consultas e Exames de Imagem")
    ]
    
    clinicas_obj = []
    for nome_clinica, local, desc in dados_clinicas:
        c = Clinica(nome_clinica, local, desc, time(6, 0), time(22, 0))
        clinicas_obj.append(c)
        sistema.controlador_clinicas._ControladorClinicas__clinicas.append(c)
        
    # Espalhar os vínculos: Garante que cada médico trabalhe em 1 a 3 clínicas aleatórias
    for prof in profissionais_obj:
        clinicas_selecionadas = random.sample(clinicas_obj, random.randint(1, 3))
        for c in clinicas_selecionadas:
            c.adicionar_profissional(prof)

    # 4. GERAR ATENDIMENTOS (1000 Atendimentos com pool equilibrado)
    # Criamos uma lista com múltiplos itens repetidos para simular "pesos".
    # Assim, haverá muito mais consultas de rotina do que cirurgias.
    tipos_atendimento_pool = (
        [("Consulta de Rotina", 150.0)] * 40 +
        [("Retorno", 0.0)] * 30 +
        [("Avaliação Especializada", 250.0)] * 15 +
        [("Sessão de Fisioterapia", 100.0)] * 10 +
        [("Atendimento de Emergência", 400.0)] * 3 +
        [("Cirurgia de Pequeno Porte", 1500.0)] * 2
    )
    
    pool_procedimentos = [
        ("Exame de Sangue", 60.0), ("Raio-X", 120.0), ("Eletrocardiograma", 150.0), 
        ("Ressonância Magnética", 800.0), ("Curativo Simples", 40.0), ("Sutura", 250.0),
        ("Ultrassom", 200.0), ("Aplicação de Injeção", 35.0)
    ]
    
    formas_pagamento = ["PIX", "CARTAO", "DINHEIRO"]

    for i in range(1000):
        # Escolhe a clínica e garante que o profissional escolhido trabalha nela
        clin = random.choice(clinicas_obj)
        prof = random.choice(clin.profissionais) 
        pac = random.choice(pacientes_obj)
        
        dias_atras = random.randint(0, 365)
        data_atend = date.today() - timedelta(days=dias_atras)
        hora_atend = time(random.randint(7, 20), random.choice([0, 15, 30, 45]))
        
        tipo_nome, tipo_custo_base = random.choice(tipos_atendimento_pool)
        
        # --- A MÁGICA DO HU (Sistema Único de Saúde) ---
        eh_hu = "HU" in clin.nome
        if eh_hu:
            tipo_custo_base = 0.0
            
        numero = f"{i + 1:04d}"
        at = Atendimento(numero, pac, prof, clin, data_atend, hora_atend, tipo_nome)
        
        # Adiciona o procedimento inicial do atendimento
        at.adicionar_procedimento(Procedimento(f"Atendimento: {tipo_nome}", tipo_custo_base, prof))
        
        # 50% de probabilidade de ter exames/procedimentos extras
        if random.random() < 0.5:
            extras = random.sample(pool_procedimentos, random.randint(1, 3))
            for desc, custo_proc in extras:
                if eh_hu:
                    custo_proc = 0.0 # Exames também são de graça no HU!
                at.adicionar_procedimento(Procedimento(desc, custo_proc, prof))

        # Pagamento final
        valor_final = at.valor_total
        forma = random.choice(formas_pagamento)
        
        if forma == "PIX":
            pag = PagamentoPix(data_atend, valor_final, pac.cpf)
        elif forma == "CARTAO":
            pag = PagamentoCartao(data_atend, valor_final, f"{random.randint(1000, 9999)}567890123456", random.choice(["Crédito - Visa", "Débito - Mastercard"]))
        else:
            pag = PagamentoDinheiro(data_atend, valor_final)
            
        at.adicionar_pagamento(pag)
        sistema.controlador_atendimentos.atendimentos.append(at)

    print("\n" + "="*55)
    print(" BASE DE DADOS HILARIANTE E MASSIVA CARREGADA!")
    print("="*55)
    print(f" -> 150 Pacientes registrados")
    print(f" -> 20 Profissionais (incluindo a Vila do Chaves)")
    print(f" -> 5 Hospitais Locais de Florianópolis")
    print(f" -> 1000 Atendimentos processados perfeitamente")
    print("    * Nota: Todos os custos no HU foram isentados (SUS).")
    print("="*55 + "\n")
    
    sistema.inicializar_sistema()

if __name__ == "__main__":
    popular_e_iniciar()