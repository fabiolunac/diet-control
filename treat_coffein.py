import sqlite3
import pandas as pd
from src.transform_db import create_date_db

conn = sqlite3.connect('./db/coffein.db')
cursor = conn.cursor()

df_coff = pd.read_sql_query("SELECT * from coffein", conn)
df_coff['Data'] = pd.to_datetime(df_coff['Data'])
print(df_coff)

df_date = pd.DataFrame({
    'Data': pd.date_range(
        start=df_coff['Data'].min(),
        end='31/12/2026',
        freq='D'
    )
})

df_date['Mes_Ano'] = df_date['Data'].dt.to_period('M') 

df_coff = df_date.merge(df_coff, how='left', on='Data')
# print(df_coff)


