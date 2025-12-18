import pymysql
import os

# Configurações do Banco (Baseado no que você me passou)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'port': 3306,
    # Não definimos 'database' aqui porque o script.sql pode conter o comando CREATE DATABASE
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

SQL_FILE = 'script.sql'

def run_sql_script():
    print(f"--- Iniciando execução do script: {SQL_FILE} ---")
    
    # Verifica se o arquivo existe
    if not os.path.exists(SQL_FILE):
        print(f"ERRO: O arquivo '{SQL_FILE}' não foi encontrado.")
        return

    # 1. Conecta ao Servidor MySQL
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print("Conexão com o MySQL estabelecida com sucesso.")
    except pymysql.MySQLError as e:
        print(f"ERRO ao conectar ao MySQL: {e}")
        return

    try:
        with connection.cursor() as cursor:
            # 2. Lê o arquivo SQL
            with open(SQL_FILE, 'r', encoding='utf-8') as f:
                script_content = f.read()

            # 3. Separa os comandos
            # O execute() do driver geralmente executa apenas um comando por vez.
            # Vamos separar por ponto e vírgula (;).
            statements = script_content.split(';')

            for statement in statements:
                # Remove espaços em branco e quebras de linha extras
                stmt = statement.strip()
                
                if stmt:
                    try:
                        print(f"Executando comando: {stmt[:50]}...") # Mostra o começo do comando
                        cursor.execute(stmt)
                    except pymysql.MySQLError as e:
                        # Ignora avisos de "tabela já existe" se for o caso, ou para o script
                        print(f"ERRO ao executar comando: {e}")
                        # Opcional: connection.rollback() se quiser desfazer tudo ao errar
            
            connection.commit()
            print("\n--- Script executado com sucesso! Tabelas criadas. ---")

    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        connection.close()
        print("Conexão encerrada.")

if __name__ == '__main__':
    run_sql_script()