import streamlit as st
import pandas as pd
import sqlite3

from src.transform_db import calculate_macros, create_date_db
from src.metrics import *
from src.figures import *
from metas import *
from dieta import write_diet


def add_line_diet(conn, date, ref, alimento, quantidade):
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO diet (Data, Refeição, Alimento, Quantidade)
        VALUES (?, ?, ?, ?)
        """,
        (date, ref, alimento, quantidade)
    )

    conn.commit()

def personalize_metric():
    st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: #B82B30;
        border: 1px solid #B82B30;
        padding: 15px;
        border-radius: 12px;
    }

    div[data-testid="stMetric"] > div {
        color: white;
    }

    div[data-testid="stMetricLabel"] p {
        color: white;
    }

    div[data-testid="stMetricValue"] {
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    st.title('Diet Control')

    # ------------ TABELA MACROS ------------
    conn_macros = sqlite3.connect('./db/macros.db')
    df_macros = pd.read_sql_query('SELECT * from macros', conn_macros)
    df_macros.to_csv('diet_macros.csv')

    # ------------ TABELA DIETA ------------
    conn_diet = sqlite3.connect('./db/diet_control.db')
    df_diet = pd.read_sql_query('SELECT * from diet', conn_diet)

    df_diet = calculate_macros(df_diet, df_macros)
    df_diet['Data'] = pd.to_datetime(df_diet['Data'])

    # ------------ TABELA CAFEÍNA ------------
    conn_coff = sqlite3.connect('./db/coffein.db')
    df_coff = pd.read_sql_query('SELECT * from coffein', conn_coff)

    
    # ------------ TABELA DATAS ------------
    df_date = pd.DataFrame({
        'Data': pd.date_range(
            start=df_diet['Data'].min(),
            end='31/12/2026',
            freq='D'
        )
    })
    df_date['Mes_Ano'] = df_date['Data'].dt.to_period('M') 

    # ------------ TABELA DIETA FINAL ------------
    df_diet = df_date.merge(df_diet, on='Data', how='left')

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Macros', 'Controle Mensal', 'Controle Diário', 'Dieta', 'Tabelas', 'Remover Dados'])

    # ====================================================== PAGE 1 ======================================================
    with tab1:
        alimentos = df_macros['alimento'].tolist()

        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.write('Adicionar Refeição')

            date = st.date_input('Data')

            refs = ['Café da Manhã', 'Almoço', 'Lanche da Tarde', 'Pré Treino', 'Janta']
            ref = st.selectbox('Refeição', refs)

            alimento = st.selectbox('Alimento', alimentos)

            quantidade = st.number_input('Quantidade (g)', min_value=0.0)

            c1, c2 = st.columns(2)
            with c1:
                bt_add =  st.button('Adicionar refeição')

            with c2:
                bt_simul = st.button('Calcular macros')

            if bt_add:
                if date and ref and alimento and quantidade > 0:
                    st.markdown(
                        f'''
                        ## Adicionado:
                        - {date}
                        - {ref}
                        - {alimento}
                        - {quantidade}
                        '''
                    )
                    add_line_diet(conn_diet, date, ref, alimento, quantidade)
                else:
                    st.warning('Preencha os campos corretamente')

            if bt_simul:
                cals_simul, prot_simul, carbo_simul = simulate_macros(df_macros, alimento, quantidade)

                st.markdown(
                    f"""
                    ## {alimento} - {quantidade}g
                    - Calorias: {cals_simul} kcal
                    - Proteínas: {prot_simul}g
                    - Carboidratos: {carbo_simul}g
                    """
                )
                


    # ====================================================== PAGE 2 ======================================================
    with tab2:
        col1, col2 = st.columns(2)

        mes_atual = pd.Timestamp.today().to_period('M')
        mes_atual_str = str(mes_atual)

        dia_atual = pd.Timestamp.today().normalize()

        meses = sorted(df_diet['Mes_Ano'].astype(str).unique(), reverse=True)
        index_padrao = meses.index(mes_atual_str) if mes_atual_str in meses else 0

        with col1:
            opcao = st.radio(
                'Período',
                ['Mês Atual', 'Selecionar mês', 'Todos']
            )

        with col2:
            mes_selecionado = st.selectbox(
                'Selecione o mês',
                meses,
                index=index_padrao,
                disabled=(opcao != 'Selecionar mês')
            )

        if opcao == 'Mês Atual':
            df_filtrado = df_diet[df_diet['Mes_Ano'] == mes_atual]
            
        elif opcao == 'Selecionar mês':
            df_filtrado = df_diet[df_diet['Mes_Ano'].astype(str) == mes_selecionado]
        else:
            df_filtrado = df_diet
        
        fig1 = fig_consumo_dia(df_filtrado, 'Calorias (kcal)')
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = fig_consumo_dia(df_filtrado, 'Proteínas (g)')
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = fig_consumo_dia(df_filtrado, 'Carboidratos (g)')
        st.plotly_chart(fig3, use_container_width=True)

    # ====================================================== PAGE 3 ======================================================
    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            opcao_dia = st.radio(
                'Dia', 
                ['Hoje', 'Selecionar']
            )

        dias = sorted(df_diet['Data'].astype(str).unique(), reverse=False)

        if str(dia_atual) in dias:
            index_hoje = dias.index(str(dia_atual))
        else:
            index_hoje = 0  

        
        with c2:
            dia_selecionado = st.selectbox(
                'Selecione o dia', 
                dias, 
                index=index_hoje,
                disabled= (opcao_dia != 'Selecionar')
            )


        if opcao_dia == 'Hoje':
            df_day = df_diet[df_diet['Data'] == dia_atual]
            selected_day = dia_atual
        elif opcao_dia == 'Selecionar':
            df_day = df_diet[df_diet['Data'] == dia_selecionado]
            selected_day = dia_selecionado

        macros_labels = ['Calorias (kcal)', 'Proteínas (g)', 'Carboidratos (g)']
    

        ref_cals, ref_prot, ref_carbo = [], [], []
        for r in refs:
            day_cals, r_cals = calculate_vals(df_day, r, selected_day, 'Calorias (kcal)')
            day_prot, r_prot = calculate_vals(df_day, r, selected_day, 'Proteínas (g)')
            day_carbo, r_carbo = calculate_vals(df_day, r, selected_day, 'Carboidratos (g)')

            ref_cals.append(r_cals)
            ref_prot.append(r_prot)
            ref_carbo.append(r_carbo)
        
        ref_labels = ['Dia', 'Café', 'Almoço', 'Lanche 1', 'Lanche 2', 'Janta']

        df_cals = pd.DataFrame({
            'Refs': ref_labels,
            'Calorias':[day_cals, ref_cals[0], ref_cals[1], ref_cals[2], ref_cals[3], ref_cals[4]],
            'Meta':[CALO_META_DIA, REF1_CALS_META_DIA, REF2_CALS_META_DIA, REF3_CALS_META_DIA, REF4_CALS_META_DIA, REF5_CALS_META_DIA]
        })
        df_cals['Delta'] = df_cals['Meta'] - df_cals['Calorias']
        df_cals['Completed'] = df_cals['Calorias']/df_cals['Meta']*100

        df_prot = pd.DataFrame({
            'Refs': ref_labels,
            'Proteínas':[day_prot, ref_prot[0], ref_prot[1], ref_prot[2], ref_prot[3], ref_prot[4]],
            'Meta':[PROTEIN_META_DIA, REF1_PROT_META_DIA, REF2_PROT_META_DIA, REF3_PROT_META_DIA, REF4_PROT_META_DIA, REF5_PROT_META_DIA]
        })
        df_prot['Delta'] = df_prot['Meta'] - df_prot['Proteínas']
        df_prot['Completed'] = df_prot['Proteínas']/df_prot['Meta']*100

        df_carbo = pd.DataFrame({
            'Refs': ref_labels,
            'Carboidratos':[day_carbo, ref_carbo[0], ref_carbo[1], ref_carbo[2], ref_carbo[3], ref_carbo[4]],
            'Meta':[CARBO_META_DIA, REF1_CARBO_META_DIA, REF2_CARBO_META_DIA, REF3_CARBO_META_DIA, REF4_CARBO_META_DIA, REF5_CARBO_META_DIA]
        })
        df_carbo['Delta'] = df_carbo['Meta'] - df_carbo['Carboidratos']
        df_carbo['Completed'] = df_carbo['Carboidratos']/df_carbo['Meta']*100

        # Merging all dfs
        df_macro_vals = {
            'Calorias (kcal)':df_cals,
            'Proteínas (g)': df_prot, 
            'Carboidratos (g)':df_carbo
        }

        # st.write(df_macro_vals)

        macros_completed_day = {}
        for m in macros_labels:
            df = df_macro_vals[m]
            macros_completed_day[m] = df[df['Refs'] == 'Dia']['Completed'].sum()

        valor = macros_completed_day["Calorias (kcal)"]

        msg = f'PARABÉNS, VOCÊ BATEU A META ({valor:.0f}%)' if valor > 80 else f'MELHORE AMANHÃ ({valor:.0f}%)'

        (st.success if valor > 80 else st.error)(msg)

        fig_cals_day = comparative_figure(df_cals, 'Calorias')
        st.plotly_chart(fig_cals_day, use_container_width=True)

        fig_prot_day = comparative_figure(df_prot, 'Proteínas')
        st.plotly_chart(fig_prot_day, use_container_width=True)

        fig_carbo_day = comparative_figure(df_carbo, 'Carboidratos')
        st.plotly_chart(fig_carbo_day, use_container_width=True)

    # ====================================================== PAGE 4 ======================================================
    with tab4:
        write_diet()


    # ====================================================== PAGE 5 ======================================================
    with tab5:
        st.write('Alimentação')
        df_diet['Data'] = df_diet['Data'].dt.strftime('%d/%m')
        st.dataframe(df_diet[['Data', 'Refeição', 'Alimento', 'Quantidade', 'Calorias (kcal)', 'Proteínas (g)', 'Carboidratos (g)']])

        st.write('Macros')
        st.dataframe(df_macros[['alimento', 'quantidade_g', 'calorias_kcal', 'proteínas_g', 'carboidratos_g']])

        st.write('Cafeína')
        st.dataframe(df_coff)

        st.write('Remover Linhas')
    
    # ====================================================== PAGE 6 ======================================================
    with tab6:
        st.markdown('''
        ## Remover Dados:
        - Selecione a tabela 
        - Selecione o ID da linha
        - Clique no botão e voilà!
        ''')
        tabela = st.selectbox('Tabela', ['Macros', 'Dieta', 'Cafeína'])

        if tabela == 'Dieta':
            df = df_diet.copy()
            nome_tabela = 'diet'
            conn_selected = conn_diet
        elif tabela == 'Macros':
            df = df_macros.copy()
            nome_tabela = 'macros'
            conn_selected = conn_macros
        else:
            df = df_coff.copy()
            nome_tabela = 'coffeine'
            conn_selected = conn_coff

        st.dataframe(df)

        linha_id = st.selectbox(
            'Selecione o ID para remover',
            df['id']
        )
        if st.button('Remover'):
            cursor = conn_selected.cursor()
            
            cursor.execute(
                f"DELETE FROM {nome_tabela} WHERE id = ?",
                (linha_id,)
            )
            
            conn_selected.commit()
            st.success('Linha removida!')


if __name__ == "__main__":
    main()