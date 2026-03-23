import streamlit as st

def render_options(title, opt1, opt2):
    st.markdown(f"## {title}")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(opt1)

    with c2:
        st.markdown(opt2)

def write_diet():
    cafe = """## Café da Manhã
    - 2 Bananas
    - 1 Maçã
    - 60 g de aveia
    - 30 g de whey
    - 20 g de pasta de amendoim
    """

    almoco_1 = """### Opção 1
    - Arroz 350 g
    - Feijão 100 g
    - Carne 140 g
    - Azeite 15 g
    """

    almoco_2 = """### Opção 2
    - Macarrão 350 g
    - Frango 130 g
    - Azeite 25 g
    """

    cafe_tarde = """## Lanche da Tarde
    - 2 bananas
    - 60 g de aveia
    - 3 ovos
    """

    pre_treino = """## Pré-Treino
    - Pão de hambúrguer
    - Carne 100 g
    - Iogurte 100 g
    """

    st.markdown(cafe)
    st.divider()

    render_options("Almoço", almoco_1, almoco_2)
    st.divider()

    st.markdown(cafe_tarde)
    st.divider()

    st.markdown(pre_treino)
    st.divider()

    render_options("Janta", almoco_1, almoco_2)
    
