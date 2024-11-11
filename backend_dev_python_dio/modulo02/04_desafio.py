# --- INTRODUÇÃO ---  # 
# Com o aumento de clientes, a instituição percebeu a necessidade de um sistema robusto
# para gerenciar informações de seus clientes. Dado que o banco atende tanto a indivíduos(pessoas físicas)
# quanto a empresas (pessoas jurídicas), torna-se essencial ter um sistema eficaz para armazenar
# e recuperar informações desses dois tipos de clientes.

# --- OBJETIVOS ---  # 
# Inserir dados dos clientes
# Listar os clientes inseridos, de maneira clara e categorizada
# Funcionalidade de inserção de dados para ambos clientes, validando-os (CPF e/ou CNPJ)

import sqlite3
import logging
import re
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conexao = sqlite3.connect(ROOT_PATH / "desafio.sqlite")
cursor = conexao.cursor()
cursor.row_factory = sqlite3.Row

# criando as tabelas para clientes físicos e jurídicos
def criar_tabela(cursor):
    cursor.execute("CREATE TABLE clientesfisicos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(255), cpf VARCHAR(11), email VARCHAR(50))")
    cursor.execute("CREATE TABLE clientesjuridicos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(255), cnpj VARCHAR(14), email VARCHAR(50))")
    conexao.commit()
criar_tabela(cursor)


# inserindo dados dos clientes físicos
def inserir_registrofisico(conexao, cursor, data):
    try:
        cursor.executemany("INSERT INTO clientesfisicos (nome, cpf, email) VALUES (?, ?, ?);", data)
        conexao.commit()
        logging.info("OK.")
        print("Dados físicos inseridos com sucesso!")
    except Exception as e:
        logging.error("Erro ao inserir dados: %s", str(e))
        print("Ocorreu um erro. Digite novamente!")

# inserindo dados dos clientes jurídicos
def inserir_registrojuridico(conexao, cursor, data):
    try:
        cursor.executemany("INSERT INTO clientesjuridicos (nome, cnpj, email) VALUES (?, ?, ?);", data)
        conexao.commit()
        logging.info("OK.")
        print("Dados jurídicos inseridos com sucesso!")
    except Exception as e:
        logging.error("Erro ao inserir dados: %s", str(e))
        print("Ocorreu um erro. Digite novamente!")

# validação do cpf, cnpj e email
def validar_cpf(cpf):
    return re.fullmatch(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf) is not None
def validar_cnpj(cnpj):
    return re.fullmatch(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', cnpj) is not None
def validar_email(email):
    return re.fullmatch(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email) is not None

# obtendo os dados
def obter_dados_fisico():
    nome = input("Digite seu nome: ")

    while True:
        cpf = input("Digite seu CPF: ")
        if validar_cpf(cpf):
            break
        else:
            print("CPF inválido. Digite novamente! Formato: XXX.XXX.XXX-XX")
            
    while True:
        email = input("Digite seu e-mail: ")
        if validar_email(email):
            break
        else:
            print("E-mail inválido. Digite novamente!")
    return (nome, cpf, email)

def obter_dados_juridico():
    nome = input("Digite o nome da empresa: ")

    while True:
        cnpj = input("Digite o CNPJ: ")
        if validar_cnpj(cnpj):
            break
        else:
            print("CNPJ inválido. Digite novamente! Formato: XX.XXX.XXX/XXXX-XX")

    while True:
        email = input("Digite o e-mail da empresa: ")
        if validar_email(email):
            break
        else:
            print("E-mail inválido. Digite novamente!")
    return (nome, cnpj, email)

# menu base para o usuário selecionar a opção desejada
def menu_principal(conexao, cursor):
    while True:
        print("\nMenu Principal")
        print("1. Cadastrar Pessoa Física ou Jurídica")
        print("2. Listar Clientes")
        print("3. Sair")
        
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            menu_inserir_dados(conexao, cursor)
        elif escolha == "2":
            menu_listar_clientes(cursor)
        elif escolha == "3":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")

# menu cadastro pessoa fisica ou juridica 
def menu_inserir_dados(conexao, cursor):
    escolha = input("Deseja cadastrar pessoa Física (1) ou Jurídica (2)? Digite a opção: ")

    if escolha == "1":
        dados_fisico = obter_dados_fisico()
        lista_dadosfisico = [dados_fisico]
        inserir_registrofisico(conexao, cursor, lista_dadosfisico)

    elif escolha == "2":
        dados_juridico = obter_dados_juridico()
        lista_dadosjuridico = [dados_juridico]
        inserir_registrojuridico(conexao, cursor, lista_dadosjuridico)
    else:
        print("Opção inválida!")

# selecionando quais clientes listar
def menu_listar_clientes(cursor):
    escolha = input("Deseja listar clientes Físicos (1) ou Jurídicos (2)? Digite a opção: ")

    if escolha == "1":
        listar_clientesfisicos(cursor)
    elif escolha == "2":
        listar_clientesjuridicos(cursor)
    else:
        print("Opção inválida!")

def listar_clientesfisicos(cursor):
    clientes = cursor.execute('SELECT * FROM clientesfisicos')
    for cliente in clientes:
        print(dict(cliente))

def listar_clientesjuridicos(cursor):
    clientes = cursor.execute('SELECT * FROM clientesjuridicos')
    for cliente in clientes:
        print(dict(cliente))

menu_principal(conexao, cursor)
