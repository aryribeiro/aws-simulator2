import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gerenciar Perguntas AWS", layout="wide")

# --- CSS para centralizar ---
st.markdown("""
    <style>
    .block-container {
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Função para carregar o CSV
def load_csv():
    try:
        return pd.read_csv("questions.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["question", "options", "answer", "multiple"])

# Função para salvar no CSV
def save_csv(df):
    df.to_csv("questions.csv", index=False)

# Título
st.title("Gerenciar Perguntas do Simulado AWS")

# --- Formulário para adicionar perguntas ---
st.header("Adicionar Nova Pergunta")
with st.form(key="add_question_form"):
    question = st.text_input("Pergunta", placeholder="Digite a pergunta aqui")
    options = st.text_area("Opções (uma por linha)", placeholder="Opção 1\nOpção 2\nOpção 3")
    answer = st.text_area("Resposta(s) Correta(s) (uma por linha)", placeholder="Resposta 1")
    multiple = st.checkbox("Permite múltiplas respostas?")
    submit_button = st.form_submit_button("Adicionar Pergunta")

    if submit_button:
        if not question.strip():
            st.error("A pergunta não pode estar vazia.")
        elif not options.strip():
            st.error("É necessário fornecer pelo menos uma opção.")
        elif not answer.strip():
            st.error("É necessário fornecer pelo menos uma resposta correta.")
        else:
            # Processa opções e respostas
            opts_list = [opt.strip() for opt in options.split("\n") if opt.strip()]
            ans_list = [ans.strip() for ans in answer.split("\n") if ans.strip()]
            if not all(ans in opts_list for ans in ans_list):
                st.error("Todas as respostas corretas devem estar nas opções fornecidas.")
            else:
                # Carrega o CSV atual
                df = load_csv()
                # Adiciona a nova pergunta
                new_row = {
                    "question": question,
                    "options": str(opts_list),
                    "answer": str(ans_list),
                    "multiple": multiple
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_csv(df)
                st.success("Pergunta adicionada com sucesso!")
                st.rerun()  # Atualizado de experimental_rerun para rerun

# --- Visualizar e remover perguntas ---
st.header("Perguntas Existentes")
df = load_csv()
if df.empty:
    st.info("Nenhuma pergunta cadastrada ainda.")
else:
    # Exibe a tabela com botão de remoção
    for idx, row in df.iterrows():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**Pergunta {idx + 1}:** {row['question']}")
            st.write(f"Opções: {row['options']}")
            st.write(f"Resposta(s): {row['answer']}")
            st.write(f"Múltipla escolha: {row['multiple']}")
        with col2:
            if st.button("Remover", key=f"remove_{idx}"):
                df = df.drop(idx).reset_index(drop=True)
                save_csv(df)
                st.success("Pergunta removida com sucesso!")
                st.rerun()  # Atualizado de experimental_rerun para rerun