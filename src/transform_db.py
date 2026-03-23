import sqlite3
import pandas as pd

def add_cal(df_diet, df_macros):
    df_diet['Calorias (kcal)'] = (
        (df_diet['Alimento'].map(df_macros.set_index('alimento')['calorias_kcal']) * df_diet['Quantidade']) 
        / 
        df_diet['Alimento'].map(df_macros.set_index('alimento')['quantidade_g'])
    )

    return df_diet

def add_protein(df_diet, df_macros):
    df_diet['Proteínas (g)'] = (
        (df_diet['Alimento'].map(df_macros.set_index('alimento')['proteínas_g']) * df_diet['Quantidade']) 
        / 
        df_diet['Alimento'].map(df_macros.set_index('alimento')['quantidade_g'])
    )
    return df_diet

def add_carbo(df_diet, df_macros):
    df_diet['Carboidratos (g)'] = (
        (df_diet['Alimento'].map(df_macros.set_index('alimento')['carboidratos_g']) * df_diet['Quantidade']) 
        / 
        df_diet['Alimento'].map(df_macros.set_index('alimento')['quantidade_g'])
    )
    return df_diet

def create_date_db(df_diet):
    df_date = pd.DataFrame({
        'Data': pd.date_range(
            start=df_diet['Data'].min(),
            end='31/12/2026',
            freq='D'
        )
    })

    df_date['Mes_Ano'] = df_date['Data'].dt.to_period('M') 

    return df_date

def calculate_macros(df_diet, df_macros):
    df_diet = add_cal(df_diet, df_macros)
    df_diet = add_protein(df_diet, df_macros)
    df_diet = add_carbo(df_diet, df_macros)

    return df_diet
