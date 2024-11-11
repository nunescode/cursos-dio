import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conexao = sqlite3.connect(ROOT_PATH / "meu_banco.sqlite")
cursor = conexao.cursor()
cursor.row_factory = sqlite3.Row

try:

    cursor.execute('DELETE FROM clientes WHERE id=6')
    conexao.commit()

    cursor.execute('INSERT INTO clientes (nome, email) VALUES(?, ?)', ("Teste 5", "teste5@g.com"))
    cursor.execute('INSERT INTO clientes (id, nome, email) VALUES(?, ?, ?)', (7, "Teste 7", "teste7@g.com"))
    conexao.commit()
except Exception as exc:
    print(f"Ops! Algum erro ocorreu...' {exc}")
    conexao.rollback()


