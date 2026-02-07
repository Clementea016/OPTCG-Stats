import streamlit as st
import math
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="OPTCG probabilities", page_icon="🏴‍☠️")

def calcular_p_fallo(N, K, n_busq, take):
    total_comb = math.comb(N, n_busq)
    return sum((math.comb(K, i) * math.comb(N - K, n_busq - i)) / total_comb for i in range(take))

st.title("🏴‍☠️ OPTCG Probability Calculator")
st.markdown("Tool for probabilities in OPTCG")

menu = st.sidebar.radio("Selecciona herramienta:", 
    ["Searcher", "Searchable targets comparison", "Mulligan for 1 card", "Chances to see x amount of cards in x draws"])

if menu == "Searcher":
    st.header("🔍 Searcher Analysis")
    col1, col2 = st.columns(2)
    with col1:
        N = st.number_input("Deck Size", value=50)
        K = st.number_input("Targets", value=12)
    with col2:
        n = st.number_input("Searcher amount (i.e 5)", value=5)
        take = st.number_input("Cards grabbed (1, 2)", value=1)
    
    veces = st.slider("Total uses in the match", 1, 10, 4)
    p_f = calcular_p_fallo(N, K, n, take)
    
    data = []
    for k in range(veces + 1):
        pk = math.comb(veces, k) * (p_f**k) * ((1 - p_f)**(veces - k))
        data.append({"Result": f"Whiff {k} times", "Probability": f"{pk*100:.2f}%"})
    
    st.table(pd.DataFrame(data))
    st.info(f"Probability of whiffing: {p_f*100:.2f}%")

elif menu == "Searchable targets comparison":
    st.header("⚖️ Comparing")
    N = st.number_input("Deck Size", value=50)
    n = st.number_input("Searcher amount", value=5)
    v = st.slider("Total uses in the match", 1, 10, 4)
    
    c1, c2 = st.columns(2)
    K1 = c1.number_input("Targets case A", value=10)
    K2 = c2.number_input("Targets case B", value=15)
    
    pfA = calcular_p_fallo(N, K1, n, 1)
    pfB = calcular_p_fallo(N, K2, n, 1)
    
    comp_data = []
    for k in range(v + 1):
        pkA = math.comb(v, k) * (pfA**k) * ((1 - pfA)**(v - k))
        pkB = math.comb(v, k) * (pfB**k) * ((1 - pfB)**(v - k))
        comp_data.append({"Whiffs": k, f"Case A (K={K1})": f"{pkA*100:.2f}%", f"Case B (K={K2})": f"{pkB*100:.2f}%"})
    
    st.table(pd.DataFrame(comp_data))

elif menu == "Mulligan for 1 card":
    st.header("🃏 Initial hands/Life")
    K = st.number_input("Copies in deck", 1, 4, 4)
    p_f = math.comb(K, 0) * math.comb(45, 5) / math.comb(50, 5)
    
    st.metric("Initial Hand/Life", f"{(1-p_f)*100:.2f}%")
    st.metric("With a mulligan", f"{(1-p_f**2)*100:.2f}%")

elif menu == "Chances to see x amount of cards in x draws":
    st.header("📊 Cards seen stats")
    K = st.number_input("Total copies", value=4)
    vistas_str = st.text_input("Seen/Drawn cards (separate w commas(,))", "5, 10, 15, 20, 25")
    
    vistas = [int(x.strip()) for x in vistas_str.split(",")]
    res_data = []
    for n in vistas:
        fila = {"Seen/Drawn": n}
        for x in range(1, K + 1):
            p_acum = sum((math.comb(K, k) * math.comb(50 - K, n - k)) / math.comb(50, n) for k in range(x, min(n, K) + 1))
            fila[f"{x} Total Copies"] = f"{p_acum*100:.2f}%"
        res_data.append(fila)
    st.dataframe(pd.DataFrame(res_data))