import streamlit as st
import pandas as pd
import json
import time
import streamlit.components.v1 as components
import requests
from io import StringIO
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()
GOOGLE_DRIVE_CSV_URL = os.getenv("GOOGLE_DRIVE_CSV_URL")

# Configuração do app Streamlit
st.set_page_config(page_title="AWS Simulator (CCP)", page_icon="📝", layout="centered")
st.title("📝 AWS Simulator CCP")
st.markdown("Simulado AWS **Practitioner** 2025, com 65 perguntas.🚀")

st.markdown("""
<style>
    .main {
        background-color: #ffffff;
        color: #333333;
        margin-bottom: 50px; /* Adicionar espaço para o rodapé */
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 3rem; /* Aumentar padding inferior para o rodapé */
    }
    /* Esconde completamente todos os elementos da barra padrão do Streamlit */
    header {display: none !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}
    /* Remove qualquer espaço em branco adicional */
    div[data-testid="stAppViewBlockContainer"] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    /* Remove quaisquer margens extras */
    .element-container {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- CSS para centralizar e estilizar o X vermelho ---
st.markdown("""
    <style>
    /* centraliza o container principal */
    .block-container {
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    /* Estilo para o X vermelho */
    .wrong-mark {
        color: red;
        font-size: 20px;
        font-weight: bold;
        margin-right: 10px;
    }
    /* Estilo para o timer */
    #timer {
        font-size: 24px;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# — Carrega perguntas —
@st.cache_data
def load_questions(url):
    # Baixa o arquivo do Google Drive
    response = requests.get(url)
    response.raise_for_status()  # Levanta um erro se a requisição falhar
    # Lê o conteúdo do CSV a partir da resposta
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    qs = []
    for _, r in df.iterrows():
        opts = json.loads(r["options"].replace("'", '"'))
        ans = set(json.loads(r["answer"].replace("'", '"')))
        # Verifica se r["multiple"] é booleano ou string
        mul = r["multiple"] if isinstance(r["multiple"], bool) else (r["multiple"].lower() == "true")
        qs.append({"q": r["question"], "opts": opts, "ans": ans, "mul": mul})
    return qs

# Carrega as perguntas usando o link do .env
try:
    QUESTIONS = load_questions(GOOGLE_DRIVE_CSV_URL)
except Exception as e:
    st.error(f"Erro ao carregar o arquivo CSV do Google Drive: {e}")
    st.stop()

# — Callbacks —
def start_simulado():
    st.session_state.started = True
    st.session_state.start_ts = time.time()
    st.session_state.finished = False
    for i, q in enumerate(QUESTIONS):
        st.session_state[f"a_{i}"] = [] if q["mul"] else None

def finish_simulado():
    st.session_state.finished = True

# — Estado padrão —
st.session_state.setdefault("started", False)
st.session_state.setdefault("finished", False)

# — Tela inicial —
if not st.session_state.started:
    st.button("Iniciar Simulado", on_click=start_simulado)
    st.stop()

# — Timer ou finalizado —
if not st.session_state.finished:
    elapsed = time.time() - st.session_state.start_ts
    rem = max(0, int(130*60 - elapsed))
    timer_html = f"""
    <div style="position: fixed; top: 0; right: 0; font-family: Arial, sans-serif; z-index: 9999;">
      <div id="timer" style="font-size:18px; color: black;">
        ⏳ Tempo: Carregando...
      </div>
    </div>
    <script>
      let t = {rem};
      function upd() {{
        let m = String(Math.floor(t/60)).padStart(2,'0');
        let s = String(t%60).padStart(2,'0');
        document.getElementById("timer").innerText = "⏳ Tempo: " + m + ":" + s;
        if (t-- <= 0) clearInterval(i);
      }}
      upd(); let i = setInterval(upd,1000);
    </script>
    """
    components.html(timer_html, height=50)
else:
    st.markdown("#### 🚨 Simulado Finalizado!")

# — Exibe perguntas —
for i, q in enumerate(QUESTIONS):
    # Verifica se a resposta está errada, mas só exibe após o simulado ser finalizado
    user_answer = set(st.session_state[f"a_{i}"]) if q["mul"] else {st.session_state[f"a_{i}"]}
    is_wrong = user_answer != q["ans"]
    
    # Exibe o X vermelho antes da pergunta se estiver errada e o simulado estiver finalizado
    if st.session_state.finished and is_wrong:
        st.markdown(f'<span class="wrong-mark">✗</span> **Pergunta {i+1}**', unsafe_allow_html=True)
    else:
        st.subheader(f"Pergunta {i+1}")

    st.write(q["q"])
    if q["mul"]:
        st.multiselect(
            "Escolha",
            q["opts"],
            key=f"a_{i}",
            disabled=st.session_state.finished,
            label_visibility="collapsed"
        )
    else:
        st.radio(
            "Escolha",
            q["opts"],
            key=f"a_{i}",
            disabled=st.session_state.finished,
            label_visibility="collapsed"
        )

# — Finalização ou resultados —
if not st.session_state.finished:
    pend = any(st.session_state.get(f"a_{i}") in (None, []) for i in range(len(QUESTIONS)))
    if pend:
        st.button("Finalizar Simulado", disabled=True)
    else:
        st.button("Finalizar Simulado", on_click=finish_simulado)
else:
    acertos = sum(
        1 for i, q in enumerate(QUESTIONS)
        if (set(st.session_state[f"a_{i}"]) if q["mul"] else {st.session_state[f"a_{i}"]}) == q["ans"]
    )
    pct = acertos / len(QUESTIONS) * 100
    st.metric("Sua Nota (%)", f"{pct:.2f}")
    st.success(f"Acertos: {acertos} de {len(QUESTIONS)}")

# Informações de contato
st.markdown("""
---
#### 📝 AWS Simulator CCP""")
st.markdown(""" Simulado AWS **CCP** 2025, com 65 perguntas.🚀  
Por **Ary Ribeiro**. Contato via e-mail: **aryribeiro@gmail.com**  
obs.: recarregue (F5) para reiniciar o simulado.
""")