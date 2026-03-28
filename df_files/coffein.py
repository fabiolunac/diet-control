import pandas as pd
import sqlite3

table_exists = True

def create_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coffein (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Data DATE NOT NULL,
        Bebida TEXT NOT NULL,
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
    print('2 - Adicionar Linha')
    # print('3 - Deletar Linha')

def read_table(conn):
    df = pd.read_sql_query("SELECT * from coffein", conn)
    print(df)

def add_line(conn):
    cursor = conn.cursor()
    
    new_data = input('Data: ')
    new_bebida = input('Bebida: ')
    new_quantidade = input('Quantidade (ml): ')

    cursor.execute(
        """
        INSERT INTO coffein (data, bebida, quantidade)
        VALUES (?, ?, ?)
        """,
        (new_data, new_bebida, new_quantidade)
    )
    conn.commit()

    print('DADOS ADICIONADOS!')

    # print(f'Dados adicionados: \nALIMENTO: {new_alimento} \nQUANTIDADE: {new_quantidade}g \nCALORIAS: {new_calorias}kcal \nPROTEÍNAS: {new_proteinas}g \nCARBOS: {new_carboidratos}g')




def main():
    conn = sqlite3.connect('./db/coffein.db')

    if table_exists == False:
        create_table(conn)

    df_coff = pd.read_sql_query("SELECT * from coffein", conn)
    df_coff['Data'] = pd.to_datetime(df_coff['Data'])
    # print(df_coff)

    df_date = pd.DataFrame({
        'Data': pd.date_range(
            start=df_coff['Data'].min(),
            end='31/12/2026',
            freq='D'
        )
    })

    df_date['Mes_Ano'] = df_date['Data'].dt.to_period('M') 

    df_coff = df_date.merge(df_coff, how='left', on='Data')

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

            # case 3:
            #     deletar_linha(conn)

            case 0:
                break

            case _:
                print('Opção Inválida')

        input('\nDigite ENTER para continuar')

    conn.close()


if __name__ == "__main__":
    main()