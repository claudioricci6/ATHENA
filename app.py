import streamlit as st
import requests

# Configura la pagina
st.set_page_config(
    page_title="ATHENA – MDT IPMN",
    layout="centered"
)

# Titolo della pagina
st.title("🧠 ATHENA – Supporto MDT IPMN")
st.markdown(
    "Inserisci il **caso clinico** come in una discussione MDT."
)

# Text area per il caso clinico
case_text = st.text_area(
    "Caso clinico",
    height=200,
    placeholder="Esempio:\nRMN pancreas: BD-IPMN corpo 32 mm..."
)

# Bottone per inviare il caso
if st.button("Valuta caso"):
    if not case_text.strip():
        st.warning("Inserisci un caso clinico.")
    else:
        with st.spinner("ATHENA sta ragionando..."):
            try:
                # URL del webhook di n8n (usa il link giusto da n8n)
                url = "https://claudioricci6.app.n8n.cloud/webhook/ATHENA"

                
                # Fai la richiesta al webhook
                response = requests.post(
                    url,
                    json={"text": case_text},  # Passa il testo clinico
                    timeout=120
                )
                
                # Gestisci la risposta
                response.raise_for_status()
                result = response.json()

                st.success("Valutazione MDT completata")

                # Mostra il risultato del ragionamento MDT
                st.markdown("## 📋 Risultato MDT")
                st.markdown(result.get("mdt_output", "Nessun output"))

            except Exception as e:
                st.error(f"Errore: {e}")

