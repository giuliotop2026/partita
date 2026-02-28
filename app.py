import streamlit as st
import requests
from bs4 import BeautifulSoup

# CONFIGURAZIONE CANTIERE
st.set_page_config(page_title="BLUE LOCK STREAMER", page_icon="⚽")

st.markdown("# ⚽ PROGETTO BLUE LOCK")
st.markdown("### RADAR MOLECOLARE ACESTREAM")

# INPUT DEL FUORICLASSE
query = st.text_input("COSA VUOI GUARDARE?", placeholder="Napoli, Verona Napoli, F1...")

def SCANSIONE_RADAR(ricerca):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # URL DEL CAVEAU
    base_url = f"https://search-ace.stream/search?q={ricerca.replace(' ', '+')}"

    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # RICERCA PARTICELLE (ID) NELLA PAGINA
        results = []
        for link in soup.find_all('a', href=True):
            if 'acestream://' in link['href']:
                ace_id = link['href'].replace('acestream://', '')
                title = link.get_text().strip() or "PARTICELLA SENZA NOME"
                results.append({"title": title, "id": ace_id})

        return results
    except Exception as e:
        st.error(f"ERRORE NEL CANTIERE: {e}")
        return []

if query:
    risultati = SCANSIONE_RADAR(query)

    if risultati:
        st.success(f"TROVATE {len(risultati)} PARTICELLE CON POLMONI D'ACCIAIO!")
        for r in risultati:
            with st.expander(f"📺 {r['title']}"):
                st.code(r['id'], language="text")
                url_finale = f"acestream://{r['id']}"
                # IL BOTTONE DI INNESTO
                st.markdown(f'''
                    <a href="{url_finale}" target="_blank" style="text-decoration: none;">
                        <button style="background-color: #008CBA; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; width: 100%;">
                            🚀 LANCIA IN ACE PLAYER
                        </button>
                    </a>
                ''', unsafe_allow_all=True)
    else:
        st.warning("NESSUNA PARTICELLA TROVATA. CONTROLLA LO SCUDO WARP.")

st.info("RICORDA: ACE ENGINE DEVE ESSERE ATTIVO IN SOTTOFONDO.")
