import pandas as pd

dia_atual = pd.Timestamp.today().normalize()

def calculate_cals_ref_day(df, ref):
    return df[(df['Refeição'] == ref) & (df['Data'] == dia_atual)]['Calorias (kcal)'].sum()

def calculate_prot_ref_day(df, ref):
    return df[(df['Refeição'] == ref) & (df['Data'] == dia_atual)]['Proteínas (g)'].sum()

def calculate_carbo_ref_day(df, ref):
    return df[(df['Refeição'] == ref) & (df['Data'] == dia_atual)]['Carboidratos (g)'].sum()

def calculate_cals_day(df):
    return df[(df['Data'] == dia_atual)]['Calorias (kcal)'].sum()

def calculate_prot_day(df):
    return df[(df['Data'] == dia_atual)]['Proteínas (g)'].sum()

def calculate_carbo_day(df):
    return df[(df['Data'] == dia_atual)]['Carboidratos (g)'].sum()

def calculate_macros(alimento, quantidade, df_macros):

    den = (df_macros[df_macros['alimento'] == alimento]['quantidade_g'].sum())

    cals = (df_macros[df_macros['alimento'] == alimento]['calorias_kcal'].sum())/den * quantidade
    prot = df_macros[df_macros['alimento'] == alimento]['proteínas_g'].sum()/den * quantidade
    carbo = df_macros[df_macros['alimento'] == alimento]['carboidratos_g'].sum()/den * quantidade

    return cals, prot, carbo
