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
    ["Searcher", "Searchable targets comparison", "Mulligan for a single card", "Chances to see cards in x draws"])

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
    
    # Aplicamos hide_index=True y usamos use_container_width para que ocupe el ancho de la pantalla
    st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)
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
    
    st.dataframe(pd.DataFrame(comp_data), hide_index=True, use_container_width=True)

elif menu == "Mulligan for a single card":
    st.header("🃏 Mulligan for a single card/cards in life")
    
    col1, col2 = st.columns(2)
    with col1:
        K_inicial = st.number_input("Card amount in deck", value=4, min_value=1, max_value=50)
    with col2:
        hand_size = st.number_input("Hand size/Life amount (e.g. 5)", value=5, min_value=1, max_value=50)
    
    try:
        p_fallo_mano = math.comb(50 - K_inicial, hand_size) / math.comb(50, hand_size)
        prob_mano_1 = (1 - p_fallo_mano) * 100
        prob_mulligan = (1 - (p_fallo_mano ** 2)) * 100
        
        df_mulligan = pd.DataFrame({
            "Scenario": [f"Initial Hand ({hand_size} cards)", "With Mulligan (All or nothing)"],
            "Success Probability": [f"{prob_mano_1:.2f}%", f"{prob_mulligan:.2f}%"]
        })
        
        st.dataframe(df_mulligan, hide_index=True, use_container_width=True)
        
    except ValueError:
        st.error("Hand size cannot be greater than remaining cards in deck.")

elif menu == "Chances to see cards in x draws":
    st.header("📊 Cards seen stats")
    K = st.number_input("Total copies", value=4)
    vistas_str = st.text_input("Seen/Drawn cards (separate with commas)", "17, 20, 23, 25, 28")
    
    try:
        vistas = [int(x.strip()) for x in vistas_str.split(",")]
        res_data = []
        for n in vistas:
            fila = {"Seen/Drawn": n}
            for x in range(1, K + 1):
                p_acum = sum((math.comb(K, k) * math.comb(50 - K, n - k)) / math.comb(50, n) for k in range(x, min(n, K) + 1))
                fila[f"{x} Total Copies"] = f"{p_acum*100:.2f}%"
            res_data.append(fila)
        
        st.dataframe(pd.DataFrame(res_data), hide_index=True, use_container_width=True)
    except Exception as e:
        st.error("Please enter valid numbers separated by commas.")