import mysql.connector
from xml.dom import minidom
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do banco de dados
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_DATABASE')

# Conectando ao banco de dados
conexao = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cursor = conexao.cursor()

# Executando a consulta SQL para obter os dados da coluna
consulta = f"select recupera2023.invoice.xml, recupera2023.invoice.invoice_id from recupera2023.invoice where recupera2023.invoice.id = any (select recupera2023.input.invoice from recupera2023.input where recupera2023.input.id = any (select recupera2023.goal_input.input from recupera2023.goal_input where recupera2023.goal_input.goal = any (select recupera2023.goal.id from recupera2023.goal where recupera2023.goal.state = 'SP' and recupera2023.goal.agreement = any (select recupera2023.agreement.id from recupera2023.agreement where recupera2023.agreement.year = 2022 and recupera2023.agreement.company = any (select recupera2023.company.id from recupera2023.company where recupera2023.company.group = 3)))));"
cursor.execute(consulta)

# Obtendo todos os resultados
resultados = cursor.fetchall()

# Iterando sobre os resultados e criando arquivos XML
for i, dado in enumerate(resultados):

    # Convertendo o XML para uma string formatada
    xml_string = str(dado[0])

    # Salvando o XML em um arquivo
    nome_arquivo = f'{str(dado[1])}.xml'
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write(xml_string)
    
    print(f"Dados exportados para o arquivo {nome_arquivo} com sucesso!")

# Fechando a conexão com o banco de dados
conexao.close()