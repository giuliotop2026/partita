import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="BLUE LOCK STREAMER", page_icon="⚽")
st.markdown("# ⚽ PROGETTO BLUE LOCK")

query = st.text_input("COSA VUOI GUARDARE?", placeholder="Leeds, Napoli, F1...")

def SCANSIONE_AVANZATA(ricerca):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    url = f"https://search-ace.stream/search?q={ricerca.replace(' ', '+')}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
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
                # CORRETTO: unsafe_allow_html=True
                st.markdown(f'<a href="{url_f}" target="_blank"><button style="width:100%; padding:10px; background:#008CBA; color:white; border:none; border-radius:5px; cursor:pointer;">🚀 LANCIA ACE PLAYER</button></a>', unsafe_allow_html=True)
    else:
        st.error("IL RADAR AUTOMATICO È STATO BLOCCATO DAL CAVEAU.")
        st.markdown(f"### 🛡️ USA IL PONTE MANUALE")
        st.write("IL CANTIERE AUTOMATICO È INIBITO, MA PUOI PRENDERE L'ID DIRETTAMENTE QUI:")
        # CORRETTO: unsafe_allow_html=True
        st.markdown(f'<a href="https://search-ace.stream/search?q={query.replace(" ", "+")}" target="_blank"><button style="width:100%; padding:15px; background:#FF4B4B; color:white; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">🔗 APRI CAVEAU RICERCA (MANUALE)</button></a>', unsafe_allow_html=True)
