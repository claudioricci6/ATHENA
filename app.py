import streamlit as st
import requests

# ----------------------------
# CONFIGURAZIONE PAGINA
# ----------------------------
st.set_page_config(
    page_title="ATHENA – Supporto MDT IPMN",
    layout="centered"
)

st.title("🧠 ATHENA – Supporto MDT")
st.markdown("Inserisci il caso clinico come in una discussione MDT.")

# ----------------------------
# INPUT CASO CLINICO
# ----------------------------
case_text = st.text_area(
    "Caso clinico",
    height=200,
    placeholder=(
        "Esempio:\n"
        "RMN pancreas: BD-IPMN corpo 32 mm, MPD 6 mm, nodulo murale 4 mm.\n"
        "CA19-9 45. Paziente 74 anni con BPCO."
    )
)

# ----------------------------
# BOTTONE DI INVIO
# ----------------------------
if st.button("Valuta caso"):
    if not case_text.strip():
        st.warning("Inserisci un caso clinico.")
    else:
        with st.spinner("ATHENA sta ragionando..."):
            try:
                # 🔴 CAMBIA QUESTO URL CON IL TUO WEBHOOK n8n
                url = "https://TUO-N8N.app.n8n.cloud/webhook/athena-ipmn"

                response = requests.post(
                    url,
                    json={"text": case_text},
                    timeout=120
                )

                response.raise_for_status()
                result = response.json()

                st.success("Valutazione MDT completata")

                # ----------------------------
                # OUTPUT MDT
                # ----------------------------
                st.markdown("## 📋 Risultato MDT")

                output = result.get("mdt_output")

                if output:
                    # Output Markdown (titoli, liste, sezioni)
                    st.markdown(output)
                else:
                    st.error("Output vuoto ricevuto dal backend.")
                    st.markdown("### Debug risposta completa:")
                    st.json(result)

            except Exception as e:
                st.error("Errore nella chiamata al backend")
                st.exception(e)


      
