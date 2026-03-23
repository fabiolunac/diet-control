import plotly.graph_objects as go
import plotly.express as px
from parameters import *

def comparative_figure(df, type):
    fig = go.Figure()
    fig.add_bar(
        x=df['Refs'],
        y=df[type],
        name='Consumido'
    )
    fig.add_bar(
        x=df['Refs'],
        y=df['Delta'],
        name='Falta',
        marker_color='rgba(255, 0, 0, 0.2)',
        text=df['Completed'].round(1),
        texttemplate='%{text}%',
        textposition='outside'
    )
    fig.update_layout(
        barmode='stack',
        title=f'Comparativo de {type}',
        yaxis_title='(kcal)', 
        xaxis_title = 'Refeição'
    )
    return fig


def fig_consumo_dia(df, type):
    """
    df: base de dados

    type: Calorias (kcal), Proteínas (g), Carboidratos (g)
    """
    value_dia = df.groupby('Data')[type].sum().reset_index()

    if type == 'Calorias (kcal)':
        meta = CALO_META_DIA
        unit = 'kcal'
    elif type == 'Proteínas (g)':
        meta = PROTEIN_META_DIA
        unit = 'g'
    elif type == 'Carboidratos (g)':
        meta = CARBO_META_DIA
        unit = 'g'
    else:
        'Tipo inválido'

    fig = px.bar(
        value_dia, 
        x="Data",
        y=type,
        text=type
    )

    fig.update_traces(
        texttemplate='%{text:.2f}',
        textposition='outside'
    )
    fig.add_hline(
        y=meta,
        line_color='red',
        line_dash='dot', 
        line_width=3,
        annotation_text=f'Meta: {meta}{unit}',
        annotation_position='top right'
    )
    fig.update_layout(
        title=f"{type} por Dia",
        xaxis_title="Data",
        yaxis_title=type,
        showlegend=False,
        xaxis=dict(
            tickformat="%d/%m"
        )
    )
    return fig