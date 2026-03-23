import pandas as pd
import sqlite3

df_dates = pd.DataFrame({
    'Data': pd.date_range(
        start='20/03/2026',
        end='31/12/2026',
        freq='D'
    )
})

df_final = df_dates.merge(df_diet, on='Data', how='left')