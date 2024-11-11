import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conexao = sqlite3.connect(ROOT_PATH / "meu_banco.sqlite")
cursor = conexao.cursor()
cursor.row_factory = sqlite3.Row


# criando tabelas
def criar_tabela(cursor):
    cursor.execute("CREATE TABLE clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100), email VARCHAR(100))")
    conexao.commit()

# inserindo registros
def inserir_registro(conexao, cursor, nome, email):
    data = (nome, email)
    cursor.execute("INSERT INTO clientes (nome, email) VALUES (?,?);", data)
    conexao.commit()

# atualizando registros
def atualizar_registro(conexao, cursor, nome, email, id):
    data = (nome, email, id)
    cursor.execute('UPDATE clientes SET nome=?, email=? WHERE id=?', data)
    conexao.commit()

# excluindo registros
def excluir_registro(conexao, cursor, id):
    data = (id,)
    cursor.execute('DELETE FROM clientes WHERE id=?', data)
    conexao.commit()

# inserir múltiplos registros
def inserir_muitos(conexao, cursor, dados):
    cursor.executemany('INSERT INTO clientes (nome, email) VALUES(?, ?)', dados)
    conexao.commit()
dados = [
    ('Pedro', 'pedrin@realg.com'),
    ('Markin', 'derok61@realg.com'),
    ('Brenda', 'brenda@realg.com'),
]    


# consultando registros
def recuperar_cliente(cursor, id):
    cursor.execute('SELECT * FROM clientes WHERE id=?', (id,))
    return cursor.fetchone()
#cliente = recuperar_cliente(cursor, 3)
#print(dict(cliente))


# listando registros
def listar_clientes(cursor):
    return cursor.execute('SELECT * FROM clientes ORDER BY nome DESC')

clientes = listar_clientes(cursor)
for cliente in clientes:
    print(dict(cliente))
    print(f'Seja bem vindo(a) ao sistema, {cliente["nome"]}!')
