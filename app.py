import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="BLUE LOCK STREAMER", page_icon="⚽")
st.markdown("# ⚽ PROGETTO BLUE LOCK")

query = st.text_input("COSA VUOI GUARDARE?", placeholder="Leeds, Napoli, F1...")

def SCANSIONE_AVANZATA(ricerca):
    # USER-AGENT DI UN VERO MAC PER AGGIRARE I BLOCCHI
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    url = f"https://search-ace.stream/search?q={ricerca.replace(' ', '+')}"
    
    try:
        # INNESTO TIMEOUT PER NON BLOCCARE IL CANTIERE
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None # BLOCCO RILEVATO
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # SCANSIONE DELLE RIGHE DELLA TABELLA (DENSITÀ TECNICA)
        for row in soup.find_all('tr'):
            links = row.find_all('a', href=True)
            for l in links:
                if 'acestream://' in l['href']:
                    ace_id = l['href'].replace('acestream://', '')
                    title = row.get_text().strip().split('\n')[0]
                    results.append({"title": title, "id": ace_id})
        return results
    except:
        return None

if query:
    risultati = SCANSIONE_AVANZATA(query)
    
    if risultati:
        st.success(f"PARTICELLE TROVATE PER: {query}")
        for r in risultati:
            with st.expander(f"📺 {r['title']}"):
                url_f = f"acestream://{r['id']}"
                st.markdown(f'<a href="{url_f}" target="_blank"><button style="width:100%; padding:10px; background:#008CBA; color:white; border:none; border-radius:5px;">🚀 LANCIA ACE PLAYER</button></a>', unsafe_allow_all=True)
    else:
        # IL PONTE DI EMERGENZA (10000% CERTEZZA)
        st.error("IL RADAR AUTOMATICO È STATO BLOCCATO DAL CAVEAU.")
        st.markdown(f"### 🛡️ USA IL PONTE MANUALE")
        st.write("IL CANTIERE AUTOMATICO È INIBITO, MA PUOI PRENDERE L'ID DIRETTAMENTE QUI:")
        st.markdown(f'<a href="https://search-ace.stream/search?q={query.replace(" ", "+")}" target="_blank"><button style="width:100%; padding:15px; background:#FF4B4B; color:white; border:none; border-radius:5px; font-weight:bold;">🔗 APRI CAVEAU RICERCA (MANUALE)</button></a>', unsafe_allow_all=True)
