import streamlit as st
import requests
import json

# =========================
# CONFIG
# =========================
WEBHOOK_URL = "https://claudioricci6.app.n8n.cloud/webhook-test/ATHENA"

st.set_page_config(
    page_title="ATHENA – IPMN MDT",
    layout="wide"
)

# =========================
# UI
# =========================
st.title("🧠 ATHENA – IPMN MDT Decision Support")
st.caption("Inserisci il caso clinico come faresti nella chat MDT. Testo libero.")

caso = st.text_area(
    label="Caso clinico",
    height=220,
    placeholder=(
        "Esempio:\n"
        "Paziente di 80 anni, BD-IPMN 30 mm, MPD 10 mm, "
        "nodulo murale 6 mm, CA19-9 100, asintomatico."
    )
)

valuta = st.button("🔍 Valuta caso MDT")

# =========================
# LOGICA
# =========================
if valuta:
    if not caso.strip():
        st.warning("Inserisci un caso clinico prima di procedere.")
    else:
        with st.spinner("Analisi MDT in corso..."):
            try:
                response = requests.post(
                    WEBHOOK_URL,
                    json={"message": caso},
                    timeout=90
                )

                response.raise_for_status()
                data = response.json()

                st.divider()
                st.subheader("📋 Valutazione MDT")

                # Mostra JSON strutturato (robusto a qualsiasi output)
                st.json(data["output"])

            except requests.exceptions.Timeout:
                st.error("Timeout: il backend n8n non ha risposto in tempo.")
            except requests.exceptions.HTTPError as e:
                st.error(f"Errore HTTP dal backend: {e}")
            except KeyError:
                st.error(
                    "Risposta non valida dal backend.\n"
                    "Assicurati che Respond to Webhook restituisca:\n"
                    "{ \"output\": {...} }"
                )
            except Exception as e:
                st.error(f"Errore imprevisto: {e}")

# =========================
# FOOTER
# =========================
st.divider()
st.caption(
    "⚠️ Decision support non autonomo. "
    "Da utilizzare in contesto MDT secondo linee guida."
)
