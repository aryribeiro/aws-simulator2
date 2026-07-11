import streamlit as st
import pandas as pd
import json
import ast
import html
import time
import requests
from io import StringIO
from pathlib import Path
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()
GOOGLE_DRIVE_CSV_URL = os.getenv("GOOGLE_DRIVE_CSV_URL")
LOCAL_CSV = Path(__file__).parent / "questions.csv"
EXAM_DURATION = 90 * 60  # 90 minutos, em segundos (duração real do exame CLF-C02)

# Configuração do app Streamlit
st.set_page_config(page_title="AWS Simulator (CCP)", page_icon="📝", layout="centered")
st.title("📝 AWS Simulator CCP")
st.markdown("Simulado AWS **Practitioner** 2026, com 65 perguntas.🚀")

st.markdown("""
<style>
    /* centraliza o container principal */
    .block-container {
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        padding-top: 1rem;
        padding-bottom: 3rem;
    }
    /* Esconde completamente todos os elementos da barra padrão do Streamlit */
    header {display: none !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}
    /* Garante quebra de linha em alternativas longas (radio e checkbox) */
    div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stCheckbox"] div[data-testid="stMarkdownContainer"] p {
        white-space: normal !important;
        overflow-wrap: break-word;
        line-height: 1.5;
    }
    /* Alinha o marcador ao topo do texto e dá respiro entre alternativas */
    div[data-testid="stRadio"] label,
    div[data-testid="stCheckbox"] label {
        align-items: flex-start !important;
        padding: 4px 0;
    }
    /* Alternativas no feedback pós-resposta */
    .opt {
        padding: 10px 14px;
        border-radius: 8px;
        border: 1px solid #d0d0d0;
        background: #fafafa;
        color: #1a1a1a;
        margin: 6px 0;
        line-height: 1.5;
        overflow-wrap: break-word;
    }
    .opt-ok {
        background: #e6f4ea;
        border-color: #34a853;
    }
    .opt-bad {
        background: #fce8e6;
        border-color: #ea4335;
    }
    /* Timer fixo no canto superior direito da janela */
    .timer-box {
        position: fixed;
        top: 8px;
        right: 16px;
        z-index: 9999;
        font-family: Arial, sans-serif;
        font-size: 18px;
        color: black;
        background: #ffffff;
        border: 1px solid #dddddd;
        border-radius: 8px;
        padding: 4px 12px;
    }
</style>
""", unsafe_allow_html=True)

# — Carrega perguntas —
def parse_list(cell):
    """Lê a célula como JSON; aceita também o formato legado (repr Python)."""
    try:
        return json.loads(cell)
    except (json.JSONDecodeError, TypeError):
        return ast.literal_eval(cell)

def parse_questions(df):
    qs = []
    for _, r in df.iterrows():
        opts = parse_list(r["options"])
        ans = set(parse_list(r["answer"]))
        # Verifica se r["multiple"] é booleano ou string
        mul = r["multiple"] if isinstance(r["multiple"], bool) else (str(r["multiple"]).lower() == "true")
        qs.append({"q": r["question"], "opts": opts, "ans": ans, "mul": mul})
    return qs

@st.cache_data(ttl=7200)  # 2 horas
def load_questions(url):
    if url:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = "utf-8"  # Drive envia sem charset; evita mojibake
            return parse_questions(pd.read_csv(StringIO(response.text)))
        except Exception:
            if LOCAL_CSV.exists():
                return parse_questions(pd.read_csv(LOCAL_CSV, encoding="utf-8"))
            raise
    if LOCAL_CSV.exists():
        return parse_questions(pd.read_csv(LOCAL_CSV, encoding="utf-8"))
    raise RuntimeError(
        "Defina GOOGLE_DRIVE_CSV_URL no arquivo .env ou coloque um questions.csv na pasta do app."
    )

try:
    QUESTIONS = load_questions(GOOGLE_DRIVE_CSV_URL)
except Exception as e:
    st.error(f"Erro ao carregar as perguntas: {e}")
    st.stop()

TOTAL = len(QUESTIONS)

# — Callbacks —
def start_simulado():
    st.session_state.started = True
    st.session_state.timed = st.session_state.modo_sel.startswith("⏱️")
    st.session_state.start_ts = time.time()
    st.session_state.finished = False

def lock_single(i):
    """Trava a resposta de escolha única assim que o aluno marca uma alternativa."""
    escolha = st.session_state.get(f"a_{i}")
    if escolha is not None:
        st.session_state[f"resp_{i}"] = [escolha]

def lock_multiple(i, opts):
    """Trava a resposta de múltipla escolha ao confirmar."""
    st.session_state[f"resp_{i}"] = [
        o for j, o in enumerate(opts) if st.session_state.get(f"a_{i}_{j}")
    ]

# — Estado padrão —
st.session_state.setdefault("started", False)
st.session_state.setdefault("finished", False)

# — Tela inicial —
if not st.session_state.started:
    st.radio(
        "Modo do simulado:",
        ["⏱️ Com tempo (90 minutos, como no exame real)", "🍃 Sem limite de tempo"],
        key="modo_sel",
    )
    st.button("Iniciar Simulado", on_click=start_simulado)
    st.stop()

# — Encerramento automático —
def tempo_restante():
    return max(0, int(EXAM_DURATION - (time.time() - st.session_state.start_ts)))

respondidas = sum(1 for i in range(TOTAL) if f"resp_{i}" in st.session_state)

if not st.session_state.finished:
    if st.session_state.timed and tempo_restante() <= 0:
        st.session_state.finished = True
        st.session_state.tempo_esgotado = True
    elif respondidas == TOTAL:
        st.session_state.finished = True

# — Timer ou status —
@st.fragment(run_every=1.0)
def render_timer():
    rem = tempo_restante()
    if rem <= 0:
        if not st.session_state.finished:
            st.session_state.finished = True
            st.session_state.tempo_esgotado = True
        st.rerun(scope="app")
    m, s = divmod(rem, 60)
    st.markdown(f'<div class="timer-box">⏳ Tempo: {m:02d}:{s:02d}</div>', unsafe_allow_html=True)

if not st.session_state.finished:
    if st.session_state.timed:
        render_timer()
    st.progress(respondidas / TOTAL, text=f"Respondidas: {respondidas} de {TOTAL}")
elif st.session_state.get("tempo_esgotado"):
    st.markdown("#### ⏰ Tempo esgotado! Simulado Finalizado.")
else:
    st.markdown("#### 🚨 Simulado Finalizado!")

# — Renderização do feedback de uma pergunta já respondida —
def render_feedback(q, resposta):
    user = set(resposta)
    if not resposta:
        st.markdown("**⚠️ Não respondida.** As respostas corretas estão destacadas abaixo:")
    elif user == q["ans"]:
        st.markdown("**✅ Você acertou!**")
    else:
        st.markdown("**❌ Você errou.** As respostas corretas estão destacadas em verde:")
    for opt in q["opts"]:
        texto = html.escape(opt)
        if opt in q["ans"]:
            sufixo = " ✅" if opt in user else " ✅ <em>(resposta correta)</em>"
            st.markdown(f'<div class="opt opt-ok">{texto}{sufixo}</div>', unsafe_allow_html=True)
        elif opt in user:
            st.markdown(f'<div class="opt opt-bad">{texto} ❌ <em>(sua resposta)</em></div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="opt">{texto}</div>', unsafe_allow_html=True)

# — Exibe perguntas —
for i, q in enumerate(QUESTIONS):
    with st.container(border=True):
        st.markdown(f"**Pergunta {i+1} de {TOTAL}**")
        st.write(q["q"])

        if f"resp_{i}" in st.session_state or st.session_state.finished:
            render_feedback(q, st.session_state.get(f"resp_{i}", []))
        elif q["mul"]:
            n_ans = len(q["ans"])
            st.caption(f"Escolha {n_ans} alternativas e confirme:")
            for j, opt in enumerate(q["opts"]):
                st.checkbox(opt, key=f"a_{i}_{j}")
            marcadas = sum(bool(st.session_state.get(f"a_{i}_{j}")) for j in range(len(q["opts"])))
            st.button(
                "Confirmar resposta",
                key=f"c_{i}",
                disabled=marcadas != n_ans,
                on_click=lock_multiple,
                args=(i, q["opts"]),
            )
        else:
            st.radio(
                "Escolha uma alternativa:",
                q["opts"],
                index=None,
                key=f"a_{i}",
                on_change=lock_single,
                args=(i,),
                label_visibility="collapsed",
            )

# — Resultado final —
if st.session_state.finished:
    acertos = sum(
        1 for i, q in enumerate(QUESTIONS)
        if set(st.session_state.get(f"resp_{i}", [])) == q["ans"]
    )
    pct = acertos / TOTAL * 100
    st.metric("Sua Nota (%)", f"{pct:.2f}")
    st.success(f"Acertos: {acertos} de {TOTAL}")

# Informações de contato
st.markdown("""
---
#### 📝 AWS Simulator CCP""")
st.markdown(""" Simulado AWS **CCP** 2026, com 65 perguntas.🚀
Por **Ary Ribeiro**. Contato via e-mail: **aryribeiro@gmail.com**
obs.: recarregue (F5) para reiniciar o simulado.
""")
