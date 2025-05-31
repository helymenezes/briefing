import sqlite3
import os

def reconstruir_banco():
    # Verificar se o banco de dados existe
    if os.path.exists('database.db'):
        # Fazer backup do banco de dados original
        if os.path.exists('database_backup.db'):
            os.remove('database_backup.db')
        os.rename('database.db', 'database_backup.db')
        print("Backup do banco de dados criado como 'database_backup.db'")
    
    # Criar novo banco de dados
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Criar tabelas com estrutura atualizada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS briefing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            briefing_id INTEGER,
            circ_auto TEXT,
            circ_pre_auto TEXT,
            FOREIGN KEY (briefing_id) REFERENCES briefing(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("Banco de dados reconstruído com sucesso!")

if __name__ == "__main__":
    reconstruir_banco()
