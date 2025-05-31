from flask import Flask, render_template, request, send_file, redirect, url_for
import sqlite3
import pdfkit
import os
from datetime import datetime
import random
import string

# Função para gerar um número de controle único
def gerar_numero_controle():
    # Formato: ANO + MÊS + 4 caracteres aleatórios (letras e números)
    agora = datetime.now()
    ano_mes = agora.strftime('%y%m')
    
    # Gerar 4 caracteres alfanuméricos aleatórios
    caracteres = string.ascii_uppercase + string.digits
    aleatorio = ''.join(random.choice(caracteres) for _ in range(4))
    
    # Juntar tudo para formar o número de controle
    numero_controle = ano_mes + aleatorio
    
    return numero_controle

def processar_ambiente(prefixo):
    """Processa os dados de um ambiente específico"""
    dados = {
        'convencional': request.form.get(f'{prefixo}_tipo') == 'Convencional' and 'Sim' or 'Não',
        'nao_tem': request.form.get(f'{prefixo}_tipo') == 'Não tem' and 'Sim' or 'Não',
        'iluminacao_qtde': request.form.get(f'{prefixo}_iluminacao_qtde'),
        'iluminacao_modo': request.form.get(f'{prefixo}_iluminacao_modo'),
        'tomadas_qtde': request.form.get(f'{prefixo}_tomadas_qtde'),
        'tomadas_modo': request.form.get(f'{prefixo}_tomadas_modo'),
        'assistente_voz': request.form.get(f'{prefixo}_assistente_voz'),
        'assistente_voz_modelo': request.form.get(f'{prefixo}_assistente_voz_modelo'),
        'ar_condicionado': request.form.get(f'{prefixo}_ar_condicionado'),
        'ar_condicionado_obs': request.form.get(f'{prefixo}_ar_condicionado_obs'),
        'tv': request.form.get(f'{prefixo}_tv'),
        'tv_obs': request.form.get(f'{prefixo}_tv_obs'),
        'sonorizacao': request.form.get(f'{prefixo}_sonorizacao'),
        'sonorizacao_obs': request.form.get(f'{prefixo}_sonorizacao_obs'),
        'janela_motorizada': request.form.get(f'{prefixo}_janela_motorizada'),
        'janela_motorizada_obs': request.form.get(f'{prefixo}_janela_motorizada_obs'),
        'cortina_motorizada': request.form.get(f'{prefixo}_cortina_motorizada'),
        'cortina_motorizada_obs': request.form.get(f'{prefixo}_cortina_motorizada_obs'),
        'outros_sistemas': request.form.get(f'{prefixo}_outros_sistemas'),
        'outros_sistemas_obs': request.form.get(f'{prefixo}_outros_sistemas_obs'),
        'notas': request.form.get(f'{prefixo}_notas')
    }
    
    # Adiciona campos específicos para áreas que têm componentes especiais
    if prefixo == 'sala_estar_hall':
        dados['biometria'] = request.form.get(f'{prefixo}_biometria')
        dados['biometria_obs'] = request.form.get(f'{prefixo}_biometria_obs')
    elif prefixo == 'area_externa_fachada':
        dados['irrigacao'] = request.form.get(f'{prefixo}_irrigacao')
        dados['irrigacao_obs'] = request.form.get(f'{prefixo}_irrigacao_obs')
    elif prefixo == 'garagem':
        dados['portao'] = request.form.get(f'{prefixo}_portao')
        dados['portao_obs'] = request.form.get(f'{prefixo}_portao_obs')
        
    return dados

app = Flask(__name__)

# Configuração do pdfkit - atualize este caminho após instalar o wkhtmltopdf
WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

# Verifica se o arquivo wkhtmltopdf existe no caminho especificado
if not os.path.exists(WKHTMLTOPDF_PATH):
    alternative_path = 'wkhtmltopdf'  # Nome simples, caso esteja no PATH
    print(f"AVISO: {WKHTMLTOPDF_PATH} não encontrado. Tentando usar '{alternative_path}' do PATH do sistema.")
    WKHTMLTOPDF_PATH = alternative_path

try:
    pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
except Exception as e:
    print(f"ERRO: Não foi possível configurar o pdfkit: {e}")
    print("Por favor, instale o wkhtmltopdf de https://wkhtmltopdf.org/downloads.html")
    pdfkit_config = None

# Rota para exibir o formulário
@app.route('/')
def form():
    return render_template('form.html', modo="novo")

# Rota para processar o formulário
@app.route('/submit', methods=['POST'])
def submit():
    action = request.form.get('action')
    
    # Dados do cliente (capa)
    cliente = request.form.get('cliente', '')
    endereco = request.form.get('endereco', '')
    telefone = request.form.get('telefone', '')
    email = request.form.get('email', '')
    
    # Perfil do cliente
    familia = request.form.get('familia', '')
    expectativas = request.form.get('expectativas', '')
    preocupacoes = request.form.get('preocupacoes', '')
    
    # Informações iniciais
    situacao = request.form.get('situacao', '')
    area = request.form.get('area', '')
      # Processamento dos ambientes
    ambientes = {
        'escritorio': processar_ambiente('escritorio'),
        'estar_intimo': processar_ambiente('estar_intimo'),
        'area_externa_lazer': processar_ambiente('area_externa_lazer'),
        'area_gourmet': processar_ambiente('area_gourmet'),
        'sala_jantar': processar_ambiente('sala_jantar'),
        'cozinha': processar_ambiente('cozinha'),
        'sala_estar_hall': processar_ambiente('sala_estar_hall'),
        'area_externa_fachada': processar_ambiente('area_externa_fachada'),
        'garagem': processar_ambiente('garagem'),
        'home_theater': processar_ambiente('home_theater'),
        'quarto01': processar_ambiente('quarto01'),
        'quarto02': processar_ambiente('quarto02'),
        'quarto03': processar_ambiente('quarto03'),
        'suite_quarto01': processar_ambiente('suite_quarto01'),
        'suite_quarto02': processar_ambiente('suite_quarto02'),
        'suite_quarto03': processar_ambiente('suite_quarto03'),
        'banheiro_social_lavabo': processar_ambiente('banheiro_social_lavabo'),
        'area_servico': processar_ambiente('area_servico'),
        'areas_circulacao': processar_ambiente('areas_circulacao')
    }
    
    # Informações sobre projetos relacionados
    projetos = {
        'arquitetonico': {
            'status': request.form.get('projeto_arquitetonico', ''),
            'contato': request.form.get('arquiteto_contato', '')
        },
        'lumiotecnico': {
            'status': request.form.get('projeto_lumiotecnico', ''),
            'contato': request.form.get('lumiotecnico_contato', '')
        },
        'eletrico': {
            'status': request.form.get('projeto_eletrico', ''),
            'contato': request.form.get('eletrico_contato', '')
        },
        'automacao_pre_existente': {
            'status': request.form.get('automacao_pre_existente', ''),
            'empresa': request.form.get('automacao_empresa_anterior', '')
        }
    }
    
    # Resumo
    resumo = {
        'circ_auto': request.form.get('total_circ_auto', ''),
        'circ_pre_auto': request.form.get('total_circ_pre_auto', '')
    }
    if action == 'salvar':     # Salvar no banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS briefing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_controle TEXT UNIQUE,
                cliente TEXT,
                endereco TEXT,
                telefone TEXT,
                email TEXT,
                familia TEXT,
                expectativas TEXT,
                preocupacoes TEXT,
                situacao TEXT,
                area TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
          # Gerar número de controle único
        numero_controle = gerar_numero_controle()
        
        # Verificar se o número já existe e gerar outro se necessário
        while True:
            cursor.execute("SELECT COUNT(*) FROM briefing WHERE numero_controle = ?", (numero_controle,))
            if cursor.fetchone()[0] == 0:
                break
            numero_controle = gerar_numero_controle()
        
        cursor.execute('''
            INSERT INTO briefing (numero_controle, cliente, endereco, telefone, email, familia, expectativas, preocupacoes, situacao, area)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (numero_controle, cliente, endereco, telefone, email, familia, expectativas, preocupacoes, situacao, area))
        
        # Obter o ID do último registro inserido
        briefing_id = cursor.lastrowid
        
        # Criar tabelas para ambientes e outros dados se ainda não existirem
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ambientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                briefing_id INTEGER,
                nome TEXT,
                tipo TEXT,
                iluminacao_qtde TEXT,
                iluminacao_modo TEXT,
                tomadas_qtde TEXT,
                tomadas_modo TEXT,
                assistente_voz TEXT,
                assistente_voz_modelo TEXT,
                ar_condicionado TEXT,
                ar_condicionado_obs TEXT,
                tv TEXT,
                tv_obs TEXT,
                sonorizacao TEXT,
                sonorizacao_obs TEXT,
                janela_motorizada TEXT,
                janela_motorizada_obs TEXT,
                cortina_motorizada TEXT,
                cortina_motorizada_obs TEXT,
                outros_sistemas TEXT,
                outros_sistemas_obs TEXT,
                notas TEXT,
                FOREIGN KEY (briefing_id) REFERENCES briefing(id)
            )
        ''')
        
        # Criar tabela para campos específicos de certos ambientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campos_especiais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ambiente_id INTEGER,
                tipo_campo TEXT,
                valor TEXT,
                observacao TEXT,
                FOREIGN KEY (ambiente_id) REFERENCES ambientes(id)
            )
        ''')
        
        # Criar tabela para informações de projetos relacionados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projetos_relacionados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                briefing_id INTEGER,
                tipo TEXT,
                status TEXT,
                contato TEXT,
                FOREIGN KEY (briefing_id) REFERENCES briefing(id)
            )
        ''')
        
        # Criar tabela para resumo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                briefing_id INTEGER,
                circ_auto TEXT,
                circ_pre_auto TEXT,
                FOREIGN KEY (briefing_id) REFERENCES briefing(id)
            )
        ''')
        
        # Salvar dados dos ambientes
        for nome, dados in ambientes.items():
            cursor.execute('''
                INSERT INTO ambientes (briefing_id, nome, tipo, iluminacao_qtde, iluminacao_modo, 
                                      tomadas_qtde, tomadas_modo, assistente_voz, assistente_voz_modelo,
                                      ar_condicionado, ar_condicionado_obs, tv, tv_obs,
                                      sonorizacao, sonorizacao_obs, janela_motorizada, janela_motorizada_obs,
                                      cortina_motorizada, cortina_motorizada_obs, outros_sistemas, 
                                      outros_sistemas_obs, notas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                briefing_id, nome,
                'Convencional' if dados.get('convencional') == 'Sim' else 'Não tem',
                dados.get('iluminacao_qtde', ''),
                dados.get('iluminacao_modo', ''),
                dados.get('tomadas_qtde', ''),
                dados.get('tomadas_modo', ''),
                dados.get('assistente_voz', ''),
                dados.get('assistente_voz_modelo', ''),
                dados.get('ar_condicionado', ''),
                dados.get('ar_condicionado_obs', ''),
                dados.get('tv', ''),
                dados.get('tv_obs', ''),
                dados.get('sonorizacao', ''),
                dados.get('sonorizacao_obs', ''),
                dados.get('janela_motorizada', ''),
                dados.get('janela_motorizada_obs', ''),
                dados.get('cortina_motorizada', ''),
                dados.get('cortina_motorizada_obs', ''),
                dados.get('outros_sistemas', ''),
                dados.get('outros_sistemas_obs', ''),
                dados.get('notas', '')
            ))
            
            ambiente_id = cursor.lastrowid
            
            # Inserir campos especiais se existirem
            if nome == 'sala_estar_hall' and 'biometria' in dados:
                cursor.execute('''
                    INSERT INTO campos_especiais (ambiente_id, tipo_campo, valor, observacao)
                    VALUES (?, ?, ?, ?)
                ''', (ambiente_id, 'biometria', dados.get('biometria', ''), dados.get('biometria_obs', '')))
            elif nome == 'area_externa_fachada' and 'irrigacao' in dados:
                cursor.execute('''
                    INSERT INTO campos_especiais (ambiente_id, tipo_campo, valor, observacao)
                    VALUES (?, ?, ?, ?)
                ''', (ambiente_id, 'irrigacao', dados.get('irrigacao', ''), dados.get('irrigacao_obs', '')))
            elif nome == 'garagem' and 'portao' in dados:
                cursor.execute('''
                    INSERT INTO campos_especiais (ambiente_id, tipo_campo, valor, observacao)
                    VALUES (?, ?, ?, ?)
                ''', (ambiente_id, 'portao', dados.get('portao', ''), dados.get('portao_obs', '')))
                
        # Salvar dados dos projetos relacionados
        for tipo, dados in projetos.items():
            cursor.execute('''
                INSERT INTO projetos_relacionados (briefing_id, tipo, status, contato)
                VALUES (?, ?, ?, ?)
            ''', (briefing_id, tipo, dados.get('status', ''), dados.get('contato', '')))
            
        # Salvar resumo
        cursor.execute('''
            INSERT INTO resumo (briefing_id, circ_auto, circ_pre_auto)
            VALUES (?, ?, ?)
        ''', (briefing_id, resumo.get('circ_auto', ''), resumo.get('circ_pre_auto', '')))
        
        conn.commit()
        conn.close()
        return 'Dados salvos com sucesso!'
    
    elif action == 'imprimir':
        # Gerar PDF usando pdfkit
        if pdfkit_config is None:
            return 'Erro: wkhtmltopdf não está configurado corretamente. Verifique o console para mais informações.'
            
        try:
            # Preparar dados para renderização do template
            dados_completos = {
                'cliente': cliente,
                'endereco': endereco,
                'telefone': telefone,
                'email': email,
                'perfil': {
                    'familia': familia,
                    'expectativas': expectativas,
                    'preocupacoes': preocupacoes
                },
                'informacoes_iniciais': {
                    'situacao': situacao,
                    'area': area
                },
                'ambientes': ambientes,
                'projetos': projetos,
                'resumo': resumo
            }            # Renderizar o template com os dados
            rendered = render_template('pdf_template.html', 
                                       dados=dados_completos, 
                                       now=datetime.now())
            
            # Gerar o PDF
            pdf_filename = f"briefing_{cliente.replace(' ', '_')}_{situacao}.pdf"
            pdfkit.from_string(rendered, pdf_filename, configuration=pdfkit_config)
            return send_file(pdf_filename, as_attachment=True)
        except Exception as e:
            return f'Erro ao gerar PDF: {e}'
    else:
        return 'Ação inválida.'

# Rota para listar registros
@app.route('/registros')
def registros():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM briefing')
    registros = cursor.fetchall()
    
    conn.close()
    
    return render_template('registros.html', registros=registros)

# Rota para visualizar detalhes de um registro
@app.route('/detalhes/<int:registro_id>')
def detalhes(registro_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM briefing WHERE id = ?', (registro_id,))
    registro = cursor.fetchone()
    
    conn.close()
    
    if registro:
        return render_template('detalhes.html', registro=registro)
    else:
        return 'Registro não encontrado.'

# Rota para listar todos os briefings
@app.route('/listar')
def listar():
    page = request.args.get('page', 1, type=int)
    items_per_page = 10
    offset = (page - 1) * items_per_page
    
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Para retornar dicionários em vez de tuplas
    cursor = conn.cursor()
    
    # Contagem total de registros
    cursor.execute("SELECT COUNT(*) FROM briefing")
    total_items = cursor.fetchone()[0]
    
    # Cálculo das páginas
    total_pages = (total_items + items_per_page - 1) // items_per_page  # Teto da divisão
    
    # Buscar registros com paginação
    cursor.execute('''
        SELECT id, numero_controle, cliente, endereco, telefone, email,
               situacao, area, data_criacao
        FROM briefing
        ORDER BY data_criacao DESC
        LIMIT ? OFFSET ?
    ''', (items_per_page, offset))
    
    briefings = []
    for row in cursor.fetchall():
        briefing = dict(row)
        briefing['data_criacao'] = datetime.strptime(briefing['data_criacao'], '%Y-%m-%d %H:%M:%S')
        briefings.append(briefing)
    
    conn.close()
    
    return render_template('listar_briefings.html', 
                          briefings=briefings, 
                          page=page, 
                          total_pages=total_pages)

# Rota para buscar briefing por número de controle
@app.route('/buscar')
def buscar():
    numero_controle = request.args.get('numero_controle', '')
    
    if not numero_controle:
        return redirect(url_for('listar'))
    
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Buscar o briefing pelo número de controle
    cursor.execute("SELECT id FROM briefing WHERE numero_controle = ?", (numero_controle,))
    resultado = cursor.fetchone()
    
    conn.close()
    
    if resultado:
        # Se encontrado, redirecionar para a visualização
        return redirect(url_for('visualizar', numero_controle=numero_controle))
    else:
        # Se não encontrado, mostrar mensagem
        return render_template('listar_briefings.html', 
                              briefings=[],
                              page=1, 
                              total_pages=0, 
                              mensagem=f"Briefing com número de controle {numero_controle} não encontrado.")

# Rota para visualizar um briefing específico
@app.route('/visualizar/<numero_controle>')
def visualizar(numero_controle):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Buscar dados do briefing
    cursor.execute('''
        SELECT * FROM briefing WHERE numero_controle = ?
    ''', (numero_controle,))
    briefing = dict(cursor.fetchone() or {})
    
    if not briefing:
        conn.close()
        return redirect(url_for('listar'))
    
    # Buscar ambientes associados a este briefing
    cursor.execute('''
        SELECT * FROM ambientes WHERE briefing_id = ?
    ''', (briefing['id'],))
    
    ambientes = {}
    for row in cursor.fetchall():
        ambiente = dict(row)
        nome = ambiente['nome']
        ambientes[nome] = ambiente
        
        # Buscar campos especiais para ambientes específicos
        if nome in ['sala_estar_hall', 'area_externa_fachada', 'garagem']:
            cursor.execute('''
                SELECT tipo_campo, valor, observacao FROM campos_especiais WHERE ambiente_id = ?
            ''', (ambiente['id'],))
            
            for campo in cursor.fetchall():
                campo_info = dict(campo)
                ambientes[nome][campo_info['tipo_campo']] = campo_info['valor']
                ambientes[nome][campo_info['tipo_campo'] + '_obs'] = campo_info['observacao']
    
    # Buscar projetos relacionados
    cursor.execute('''
        SELECT * FROM projetos_relacionados WHERE briefing_id = ?
    ''', (briefing['id'],))
    
    projetos = {}
    for row in cursor.fetchall():
        projeto = dict(row)
        projetos[projeto['tipo']] = {
            'status': projeto['status'],
            'contato': projeto['contato']
        }
    
    # Buscar resumo
    cursor.execute('''
        SELECT * FROM resumo WHERE briefing_id = ?
    ''', (briefing['id'],))
    
    resumo = dict(cursor.fetchone() or {'circ_auto': '', 'circ_pre_auto': ''})
    
    conn.close()
    
    # Renderizar o formulário preenchido com os dados
    return render_template('form.html',
                          modo="visualizar",
                          numero_controle=numero_controle,
                          cliente=briefing.get('cliente', ''),
                          endereco=briefing.get('endereco', ''),
                          telefone=briefing.get('telefone', ''),
                          email=briefing.get('email', ''),
                          familia=briefing.get('familia', ''),
                          expectativas=briefing.get('expectativas', ''),
                          preocupacoes=briefing.get('preocupacoes', ''),
                          situacao=briefing.get('situacao', ''),
                          area=briefing.get('area', ''),
                          ambientes=ambientes,
                          projetos=projetos,
                          resumo=resumo)

# Rota para editar um briefing
@app.route('/editar/<numero_controle>')
def editar(numero_controle):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Buscar dados do briefing
    cursor.execute('''
        SELECT * FROM briefing WHERE numero_controle = ?
    ''', (numero_controle,))
    briefing = dict(cursor.fetchone() or {})
    
    if not briefing:
        conn.close()
        return redirect(url_for('listar'))
    
    # Buscar ambientes associados a este briefing
    cursor.execute('''
        SELECT * FROM ambientes WHERE briefing_id = ?
    ''', (briefing['id'],))
    
    ambientes = {}
    for row in cursor.fetchall():
        ambiente = dict(row)
        nome = ambiente['nome']
        ambientes[nome] = ambiente
        
        # Buscar campos especiais para ambientes específicos
        if nome in ['sala_estar_hall', 'area_externa_fachada', 'garagem']:
            cursor.execute('''
                SELECT tipo_campo, valor, observacao FROM campos_especiais WHERE ambiente_id = ?
            ''', (ambiente['id'],))
            
            for campo in cursor.fetchall():
                campo_info = dict(campo)
                ambientes[nome][campo_info['tipo_campo']] = campo_info['valor']
                ambientes[nome][campo_info['tipo_campo'] + '_obs'] = campo_info['observacao']
    
    # Buscar projetos relacionados
    cursor.execute('''
        SELECT * FROM projetos_relacionados WHERE briefing_id = ?
    ''', (briefing['id'],))
    
    projetos = {}
    for row in cursor.fetchall():
        projeto = dict(row)
        projetos[projeto['tipo']] = {
            'status': projeto['status'],
            'contato': projeto['contato']
        }
    
    # Buscar resumo
    cursor.execute('''
        SELECT * FROM resumo WHERE briefing_id = ?
    ''', (briefing['id'],))
    
    resumo = dict(cursor.fetchone() or {'circ_auto': '', 'circ_pre_auto': ''})
    
    conn.close()
    
    # URL de ação - redirecionar para a rota de atualização quando em modo de edição
    action_url = f"/atualizar/{numero_controle}"
    
    # Renderizar o formulário para edição
    return render_template('form.html',
                          modo="editar",
                          action_url=action_url,
                          numero_controle=numero_controle,
                          cliente=briefing.get('cliente', ''),
                          endereco=briefing.get('endereco', ''),
                          telefone=briefing.get('telefone', ''),
                          email=briefing.get('email', ''),
                          familia=briefing.get('familia', ''),
                          expectativas=briefing.get('expectativas', ''),
                          preocupacoes=briefing.get('preocupacoes', ''),
                          situacao=briefing.get('situacao', ''),
                          area=briefing.get('area', ''),
                          ambientes=ambientes,
                          projetos=projetos,
                          resumo=resumo)

# Rota para excluir um briefing
@app.route('/excluir/<numero_controle>')
def excluir(numero_controle):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Primeiro obtém o ID do briefing
    cursor.execute("SELECT id FROM briefing WHERE numero_controle = ?", (numero_controle,))
    resultado = cursor.fetchone()
    
    if resultado:
        briefing_id = resultado[0]
        
        # Exclui registros relacionados em todas as tabelas
        cursor.execute("DELETE FROM campos_especiais WHERE ambiente_id IN (SELECT id FROM ambientes WHERE briefing_id = ?)", (briefing_id,))
        cursor.execute("DELETE FROM ambientes WHERE briefing_id = ?", (briefing_id,))
        cursor.execute("DELETE FROM projetos_relacionados WHERE briefing_id = ?", (briefing_id,))
        cursor.execute("DELETE FROM resumo WHERE briefing_id = ?", (briefing_id,))
        cursor.execute("DELETE FROM briefing WHERE id = ?", (briefing_id,))
        
        conn.commit()
    
    conn.close()
    
    return redirect(url_for('listar'))

# Rota para atualizar um briefing existente
@app.route('/atualizar/<numero_controle>', methods=['POST'])
def atualizar(numero_controle):
    # Buscar o briefing_id a partir do numero_controle
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM briefing WHERE numero_controle = ?", (numero_controle,))
    resultado = cursor.fetchone()
    
    if not resultado:
        conn.close()
        return 'Briefing não encontrado.'
    
    briefing_id = resultado[0]
    
    # Obter dados do formulário - similar à rota /submit
    cliente = request.form.get('cliente', '')
    endereco = request.form.get('endereco', '')
    telefone = request.form.get('telefone', '')
    email = request.form.get('email', '')
    
    familia = request.form.get('familia', '')
    expectativas = request.form.get('expectativas', '')
    preocupacoes = request.form.get('preocupacoes', '')
    
    situacao = request.form.get('situacao', '')
    area = request.form.get('area', '')
    
    # Processar ambientes
    ambientes = {
        'escritorio': processar_ambiente('escritorio'),
        'estar_intimo': processar_ambiente('estar_intimo'),
        'area_externa_lazer': processar_ambiente('area_externa_lazer'),
        'area_gourmet': processar_ambiente('area_gourmet'),
        'sala_jantar': processar_ambiente('sala_jantar'),
        'cozinha': processar_ambiente('cozinha'),
        'sala_estar_hall': processar_ambiente('sala_estar_hall'),
        'area_externa_fachada': processar_ambiente('area_externa_fachada'),
        'garagem': processar_ambiente('garagem'),
        'home_theater': processar_ambiente('home_theater'),
        'quarto01': processar_ambiente('quarto01'),
        'quarto02': processar_ambiente('quarto02'),
        'quarto03': processar_ambiente('quarto03'),
        'suite_quarto01': processar_ambiente('suite_quarto01'),
        'suite_quarto02': processar_ambiente('suite_quarto02'),
        'suite_quarto03': processar_ambiente('suite_quarto03'),
        'banheiro_social_lavabo': processar_ambiente('banheiro_social_lavabo'),
        'area_servico': processar_ambiente('area_servico'),
        'areas_circulacao': processar_ambiente('areas_circulacao'),
    }
    
    # Processar projetos relacionados
    projetos = {
        'arquitetonico': {
            'status': request.form.get('projeto_arquitetonico', ''),
            'contato': request.form.get('arquiteto_contato', '')
        },
        'lumiotecnico': {
            'status': request.form.get('projeto_lumiotecnico', ''),
            'contato': request.form.get('lumiotecnico_contato', '')
        },
        'eletrico': {
            'status': request.form.get('projeto_eletrico', ''),
            'contato': request.form.get('eletrico_contato', '')
        },
        'automacao': {
            'status': request.form.get('automacao_pre_existente', ''),
            'contato': request.form.get('automacao_empresa_anterior', '')
        }
    }
    
    # Processar resumo
    resumo = {
        'circ_auto': request.form.get('total_circ_auto', ''),
        'circ_pre_auto': request.form.get('total_circ_pre_auto', '')
    }
    
    # Atualizar os dados da tabela briefing
    cursor.execute('''
        UPDATE briefing SET
            cliente = ?, endereco = ?, telefone = ?, email = ?,
            familia = ?, expectativas = ?, preocupacoes = ?,
            situacao = ?, area = ?
        WHERE id = ?
    ''', (
        cliente, endereco, telefone, email,
        familia, expectativas, preocupacoes,
        situacao, area, briefing_id
    ))
    
    # Atualizar dados dos ambientes:
    # Primeiro removemos os antigos (incluindo campos_especiais relacionados)
    cursor.execute("DELETE FROM campos_especiais WHERE ambiente_id IN (SELECT id FROM ambientes WHERE briefing_id = ?)", (briefing_id,))
    cursor.execute("DELETE FROM ambientes WHERE briefing_id = ?", (briefing_id,))
    
    # Depois inserimos os novos
    for nome, dados in ambientes.items():
        cursor.execute('''
            INSERT INTO ambientes (briefing_id, nome, tipo, iluminacao_qtde, iluminacao_modo, 
                                  tomadas_qtde, tomadas_modo, assistente_voz, assistente_voz_modelo,
                                  ar_condicionado, ar_condicionado_obs, tv, tv_obs,
                                  sonorizacao, sonorizacao_obs, janela_motorizada, janela_motorizada_obs,
                                  cortina_motorizada, cortina_motorizada_obs, outros_sistemas, 
                                  outros_sistemas_obs, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            briefing_id, nome,
            'Convencional' if dados.get('convencional') == 'Sim' else 'Não tem',
            dados.get('iluminacao_qtde', ''),
            dados.get('iluminacao_modo', ''),
            dados.get('tomadas_qtde', ''),
            dados.get('tomadas_modo', ''),
            dados.get('assistente_voz', ''),
            dados.get('assistente_voz_modelo', ''),
            dados.get('ar_condicionado', ''),
            dados.get('ar_condicionado_obs', ''),
            dados.get('tv', ''),
            dados.get('tv_obs', ''),
            dados.get('sonorizacao', ''),
            dados.get('sonorizacao_obs', ''),
            dados.get('janela_motorizada', ''),
            dados.get('janela_motorizada_obs', ''),
            dados.get('cortina_motorizada', ''),
            dados.get('cortina_motorizada_obs', ''),
            dados.get('outros_sistemas', ''),
            dados.get('outros_sistemas_obs', ''),
            dados.get('notas', '')
        ))
        
        ambiente_id = cursor.lastrowid
        
        # Inserir campos especiais se existirem
        if nome == 'sala_estar_hall' and 'biometria' in dados:
            cursor.execute('''
                INSERT INTO campos_especiais (ambiente_id, tipo_campo, valor, observacao)
                VALUES (?, ?, ?, ?)
            ''', (ambiente_id, 'biometria', dados.get('biometria', ''), dados.get('biometria_obs', '')))
        elif nome == 'area_externa_fachada' and 'irrigacao' in dados:
            cursor.execute('''
                INSERT INTO campos_especiais (ambiente_id, tipo_campo, valor, observacao)
                VALUES (?, ?, ?, ?)
            ''', (ambiente_id, 'irrigacao', dados.get('irrigacao', ''), dados.get('irrigacao_obs', '')))
        elif nome == 'garagem' and 'portao' in dados:
            cursor.execute('''
                INSERT INTO campos_especiais (ambiente_id, tipo_campo, valor, observacao)
                VALUES (?, ?, ?, ?)
            ''', (ambiente_id, 'portao', dados.get('portao', ''), dados.get('portao_obs', '')))
    
    # Atualizar projetos relacionados
    cursor.execute("DELETE FROM projetos_relacionados WHERE briefing_id = ?", (briefing_id,))
    for tipo, dados in projetos.items():
        cursor.execute('''
            INSERT INTO projetos_relacionados (briefing_id, tipo, status, contato)
            VALUES (?, ?, ?, ?)
        ''', (briefing_id, tipo, dados.get('status', ''), dados.get('contato', '')))
    
    # Atualizar resumo
    cursor.execute("DELETE FROM resumo WHERE briefing_id = ?", (briefing_id,))
    cursor.execute('''
        INSERT INTO resumo (briefing_id, circ_auto, circ_pre_auto)
        VALUES (?, ?, ?)
    ''', (briefing_id, resumo.get('circ_auto', ''), resumo.get('circ_pre_auto', '')))
    
    conn.commit()
    conn.close()
    
    action = request.form.get('action')
    if action == 'imprimir':
        # Redirecionar para a funcionalidade de impressão
        # Isso requer adaptar a funcionalidade de PDF para usar número de controle
        return redirect(url_for('imprimir_pdf', numero_controle=numero_controle))
    else:
        # Redirecionar de volta para a visualização
        return redirect(url_for('visualizar', numero_controle=numero_controle))

# Rota para gerar PDF de um briefing pelo número de controle
@app.route('/imprimir_pdf/<numero_controle>')
def imprimir_pdf(numero_controle):
    # Gerar PDF usando pdfkit
    if pdfkit_config is None:
        return 'Erro: wkhtmltopdf não está configurado corretamente. Verifique o console para mais informações.'
    
    # Buscar dados do briefing
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM briefing WHERE numero_controle = ?
    ''', (numero_controle,))
    briefing = dict(cursor.fetchone() or {})
    
    if not briefing:
        conn.close()
        return 'Briefing não encontrado.'
    
    # Buscar ambientes associados a este briefing
    cursor.execute('''
        SELECT * FROM ambientes WHERE briefing_id = ?
    ''', (briefing['id'],))
    
    ambientes = {}
    for row in cursor.fetchall():
        ambiente = dict(row)
        nome = ambiente['nome']
        ambientes[nome] = ambiente
        
        # Buscar campos especiais para ambientes específicos
        if nome in ['sala_estar_hall', 'area_externa_fachada', 'garagem']:
            cursor.execute('''
                SELECT tipo_campo, valor, observacao FROM campos_especiais WHERE ambiente_id = ?
            ''', (ambiente['id'],))
            
            for campo in cursor.fetchall():
                campo_info = dict(campo)
                ambientes[nome][campo_info['tipo_campo']] = campo_info['valor']
                ambientes[nome][campo_info['tipo_campo'] + '_obs'] = campo_info['observacao']
    
    # Buscar projetos relacionados
    cursor.execute('''
        SELECT * FROM projetos_relacionados WHERE briefing_id = ?
    ''', (briefing['id'],))
    
    projetos = {}
    for row in cursor.fetchall():
        projeto = dict(row)
        projetos[projeto['tipo']] = {
            'status': projeto['status'],
            'contato': projeto['contato']
        }
    
    # Buscar resumo
    cursor.execute('''
        SELECT * FROM resumo WHERE briefing_id = ?
    ''', (briefing['id'],))
    
    resumo = dict(cursor.fetchone() or {'circ_auto': '', 'circ_pre_auto': ''})
    
    conn.close()
    
    # Preparar dados para renderização do template
    dados_completos = {
        'numero_controle': numero_controle,
        'cliente': briefing.get('cliente', ''),
        'endereco': briefing.get('endereco', ''),
        'telefone': briefing.get('telefone', ''),
        'email': briefing.get('email', ''),
        'perfil': {
            'familia': briefing.get('familia', ''),
            'expectativas': briefing.get('expectativas', ''),
            'preocupacoes': briefing.get('preocupacoes', '')
        },
        'informacoes_iniciais': {
            'situacao': briefing.get('situacao', ''),
            'area': briefing.get('area', '')
        },
        'ambientes': ambientes,
        'projetos': projetos,
        'resumo': resumo
    }
    
    # Renderizar o template com os dados
    rendered = render_template('pdf_template.html', 
                               dados=dados_completos, 
                               now=datetime.now())
    
    try:
        # Gerar o PDF
        pdf_filename = f"briefing_{numero_controle}_{briefing.get('cliente', '').replace(' ', '_')}.pdf"
        pdfkit.from_string(rendered, pdf_filename, configuration=pdfkit_config)
        return send_file(pdf_filename, as_attachment=True)
    except Exception as e:
        return f'Erro ao gerar PDF: {e}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
