# pages/1_Dashboard.py
import streamlit as st
from firebase_admin import firestore

st.set_page_config(page_title="Dashboard", layout="wide")

# --- CONTROLE DE ACESSO ---
# Verifica se o usuário está logado. Se não, redireciona para a página principal.
if not st.session_state.get('logged_in', False):
    st.error("Você precisa estar logado para acessar esta página.")
    st.page_link("app.py", label="Voltar para o Login")
    st.stop() # Interrompe a execução da página

# --- CONTEÚDO DA PÁGINA PROTEGIDA ---

# Obtém o cliente do Firestore (a inicialização já foi feita no app.py)
db = firestore.client()

# Pega informações do usuário do session_state
user_info = st.session_state['user_info']
user_uid = user_info['localId']
user_email = user_info['email']

# Busca o nome do usuário no Firestore
try:
    user_doc = db.collection("users").document(user_uid).get()
    if user_doc.exists:
        user_name = user_doc.to_dict().get("name", "Usuário")
    else:
        user_name = "Usuário"
except Exception as e:
    user_name = "Usuário"
    st.error(f"Não foi possível buscar seu nome: {e}")

st.sidebar.header(f"Bem-vindo, {user_name}!")
if st.sidebar.button("Logout"):
    st.session_state['logged_in'] = False
    st.session_state['user_info'] = None
    st.switch_page("app.py") # Redireciona para a página de login

st.title("📊 Seu Dashboard Protegido")
st.markdown(f"Você está logado com o email: **{user_email}**")

st.divider()

st.header("Conteúdo Exclusivo")
st.write("Aqui você pode colocar gráficos, tabelas e outras informações que só usuários logados podem ver.")

# Exemplo de conteúdo
st.line_chart([10, 20, 15, 30, 25])