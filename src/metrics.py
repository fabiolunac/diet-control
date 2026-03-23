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