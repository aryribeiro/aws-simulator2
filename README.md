Obs.: caso o app esteja no modo "sleeping" (dormindo) ao entrar, basta clicar no botão que estará disponível e aguardar, para ativar o mesmo. 
![print](https://github.com/user-attachments/assets/22fde294-0bbc-45b9-9d03-9dc1aa32d629)

# AWS Simulator (SAA-C03)

Um web app de simulado para a certificação AWS SAA-C03 (2025), construído com Python e Streamlit.
Permite carregar perguntas de um CSV hospedado no Google Drive, controlar tempo de prova com cronômetro fixo no canto superior direito, e exibir correção automática ao final.

## Funcionalidades

- 65 perguntas baseadas no exame AWS SAA-C03 (2025).
- Timer de 130 minutos exibido no canto superior direito da tela.
- Suporte a perguntas de escolha única e múltipla.
- Correção automática ao final, com destaque visual para respostas erradas.
- Visual limpo e focado, com elementos do Streamlit ocultos via CSS.
- Compatível com computadores (sugestão de uso).

## Pré-requisitos

- Python 3.8 ou superior
- Conta Google Drive para armazenar o CSV
- Variável de ambiente GOOGLE_DRIVE_CSV_URL com o link direto do CSV exportado

## Instalação

1. Clone este repositório:

git clone https://github.com/aryribeiro/simulator-aws.git
cd simulator-aws

2. (Opcional) Crie e ative um ambiente virtual:

python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate       # Windows

3. Instale as dependências:

pip install -r requirements.txt

4. Crie um arquivo `.env` com a seguinte variável:

GOOGLE_DRIVE_CSV_URL="https://drive.google.com/uc?export=download&id=SEU_ID_DO_ARQUIVO"

## Como usar

Execute o app com o comando abaixo e acesse no navegador:

streamlit run app.py
e o arquivo manage_questions.py serve para adicionar perguntas e respostas no arquivo questions.csv.. após isso, basta fazer upload do csv para o Google Drive e usar o web app em ambiente local ou em produção.

## Autor

- Ary Ribeiro
- Contato: aryribeiro@gmail.com