import streamlit as st

st.set_page_config(page_title="FTMO Calc", page_icon="📊", layout="centered")

st.title("📊 FTMO Mobile Calc")
st.write("Calcolatore taglia e parametri per iPhone.")

asset = st.selectbox("Seleziona l'Asset:", ["EURUSD", "USDJPY", "XAUUSD (Oro)", "XAGUSD (Argento)"])
direzione = st.radio("Direzione del Trade:", ["Long (Compra)", "Short (Vendi)"])
prezzo_ingresso = st.number_input("Prezzo di Ingresso attuale:", value=1.00000, format="%.5f" if "EUR" in asset else "%.2f")
rischio_usd = st.number_input("Rischio Massimo ($):", value=500.0, step=50.0)
rr_ratio = st.slider("Rapporto Rischio / Rendimento (Target RR):", min_value=1.0, max_value=5.0, value=2.0, step=0.5)

if asset == "EURUSD":
    distanza_sl = st.number_input("Distanza Stop Loss (PIP, es. 25):", value=25.0, step=1.0)
    valore_pip_standard = 10.0
    lotti = rischio_usd / (distanza_sl * valore_pip_standard)
    moltiplicatore = 0.0001
    if direzione == "Long (Compra)":
        prezzo_sl = prezzo_ingresso - (distanza_sl * moltiplicatore)
        prezzo_tp = prezzo_ingresso + (distanza_sl * moltiplicatore * rr_ratio)
    else:
        prezzo_sl = prezzo_ingresso + (distanza_sl * moltiplicatore)
        prezzo_tp = prezzo_ingresso - (distanza_sl * moltiplicatore * rr_ratio)

elif asset == "USDJPY":
    distanza_sl = st.number_input("Distanza Stop Loss (PIP, es. 20):", value=20.0, step=1.0)
    lotti = rischio_usd / (distanza_sl * (10.0 / prezzo_ingresso * 100)) if prezzo_ingresso > 0 else 0
    moltiplicatore = 0.01
    if direzione == "Long (Compra)":
        prezzo_sl = prezzo_ingresso - (distanza_sl * moltiplicatore)
        prezzo_tp = prezzo_ingresso + (distanza_sl * moltiplicatore * rr_ratio)
    else:
        prezzo_sl = prezzo_ingresso + (distanza_sl * moltiplicatore)
        prezzo_tp = prezzo_ingresso - (distanza_sl * moltiplicatore * rr_ratio)

elif asset == "XAUUSD (Oro)":
    distanza_sl = st.number_input("Distanza Stop Loss (DOLLARI, es. 5.00):", value=5.0, step=0.5)
    lotti = rischio_usd / (distanza_sl * 100.0)
    if direzione == "Long (Compra)":
        prezzo_sl = prezzo_ingresso - distanza_sl
        prezzo_tp = prezzo_ingresso + (distanza_sl * rr_ratio)
    else:
        prezzo_sl = prezzo_ingresso + distanza_sl
        prezzo_tp = prezzo_ingresso - (distanza_sl * rr_ratio)

elif asset == "XAGUSD (Argento)":
    distanza_sl = st.number_input("Distanza Stop Loss (DOLLARI, es. 1.00):", value=1.0, step=0.1)
    lotti = rischio_usd / (distanza_sl * 5000.0)
    if direzione == "Long (Compra)":
        prezzo_sl = prezzo_ingresso - distanza_sl
        prezzo_tp = prezzo_ingresso + (distanza_sl * rr_ratio)
    else:
        prezzo_sl = prezzo_ingresso + distanza_sl
        prezzo_tp = prezzo_ingresso - (distanza_sl * rr_ratio)

st.markdown("---")
st.subheader("🎯 Risultati")
st.metric(label="LOTTI DA USARE", value=f"{lotti:.2f}")
st.metric(label="PREZZO STOP LOSS (SL)", value=f"{prezzo_sl:.5f}" if "EUR" in asset else f"{prezzo_sl:.2f}")
st.metric(label="PREZZO TAKE PROFIT (TP)", value=f"{prezzo_tp:.5f}" if "EUR" in asset else f"{prezzo_tp:.2f}")
