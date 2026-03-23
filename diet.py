import sqlite3 
import pandas as pd


table_exists = True

def create_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diet (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Data DATE NOT NULL DEFAULT CURRENT_DATE,
        Refeição TEXT NOT NULL,
        Alimento TEXT NOT NULL,
        Quantidade REAL NOT NULL
    )
    """)

    conn.commit()

    print('Table Created!!')

def mostrar_menu():
    print('--------------------------------------------------------')
    print('Script para gerenciar a tabela de macros')
    print('Menu:')
    print('1 - Ler Tabela')
    # print('2 - Adicionar Linha')
    # print('3 - Deletar Linha')

    print('0 - Sair')

def read_table(conn):
    df_macros = pd.read_sql_query("SELECT * from diet", conn)
    print(df_macros)

def main():
    conn = sqlite3.connect('./db/diet_control.db')

    if table_exists == False:
        create_table(conn)

    while True:
        mostrar_menu()

        try:
            c = int(input('Digite uma opção: '))
        except ValueError:
            print("Digite um número válido!")
            continue

        match c:
            case 1:
                read_table(conn)

            # case 2:
            #     add_line(conn)

            case 0:
                break

            case _:
                print('Opção Inválida')

        input('\nDigite ENTER para continuar')

    conn.close()


if __name__ == "__main__":
    main()
