import pandas as pd
import sqlite3

table_exists = True

def create_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS macros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alimento TEXT NOT NULL,
        quantidade_g REAL NOT NULL,
        calorias_kcal REAL NOT NULL,
        proteínas_g REAL NOT NULL,
        carboidratos_g REAL NOT NULL
    )
    """)

    conn.commit()

    print('Table Created!!')

def add_line(conn):
    cursor = conn.cursor()
    
    new_alimento      = input('Alimento: ')
    new_quantidade    = input('Quantidade (g): ')
    new_calorias      = input('Caloras (kcal): ')
    new_proteinas     = input('Proteínas (g): ')
    new_carboidratos  = input('Carboidratos (g): ')

    cursor.execute(
        """
        INSERT INTO macros (alimento, quantidade_g, calorias_kcal, proteínas_g, carboidratos_g)
        VALUES (?, ?, ?, ?, ?)
        """,
        (new_alimento, new_quantidade, new_calorias, new_proteinas, new_carboidratos)
    )
    conn.commit()

    print(f'Dados adicionados: \nALIMENTO: {new_alimento} \nQUANTIDADE: {new_quantidade}g \nCALORIAS: {new_calorias}kcal \nPROTEÍNAS: {new_proteinas}g \nCARBOS: {new_carboidratos}g')


def mostrar_menu():
    print('--------------------------------------------------------')
    print('Script para gerenciar a tabela de macros')
    print('Menu:')
    print('1 - Ler Tabela')
    print('2 - Adicionar Linha')
    print('3 - Deletar Linha')

    print('0 - Sair')

def read_table(conn):
    df_macros = pd.read_sql_query("SELECT * from macros", conn)
    print(df_macros)

def deletar_linha(conn):
    cursor = conn.cursor()

    rowid = int(input('Digite o id da linha: '))

    cursor.execute(
    """
    DELETE FROM macros
    WHERE rowid = ?
    """, (rowid,)
    )

    conn.commit()

    print(f'Linhar {rowid} deletada')



def main():
    conn = sqlite3.connect('./db/macros.db')

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

            case 2:
                add_line(conn)

            case 3:
                deletar_linha(conn)

            case 0:
                break

            case _:
                print('Opção Inválida')

        input('\nDigite ENTER para continuar')

    conn.close()


if __name__ == "__main__":
    main()



