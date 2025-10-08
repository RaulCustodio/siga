# pages/0_Home.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import pyrebase

st.set_page_config(page_title="HOME", page_icon="🏠", layout="wide")

@st.cache_resource
def initialize_firebase_admin():
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase_service_account"]))
        firebase_admin.initialize_app(cred)
    return firebase_admin.get_app()

@st.cache_resource
def initialize_pyrebase():
    cfg = dict(st.secrets["firebase_web_config"])
    return pyrebase.initialize_app(cfg)

initialize_firebase_admin()
pyrebase_auth = initialize_pyrebase().auth()
db = firestore.client()

if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "user_info"  not in st.session_state: st.session_state["user_info"]  = None

# CSS opcional
st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}
.appview-container .main .block-container {padding-top:0; padding-bottom:0; max-width:100% !important;}
[data-testid="stSidebar"] > div:first-child {height: 100vh;}
</style>
""", unsafe_allow_html=True)

st.title("Bem-vindo à Aplicação 🚀")

if st.session_state["logged_in"]:
    user_email = st.session_state["user_info"]["email"]
    st.success(f"Você está logado como: **{user_email}**")
    st.page_link("pages/1_Dashboard.py", label="📊 Acessar Dashboard")
    st.page_link("pages/2_MppReader.py", label="🗂️ Anexar Cronograma MPP")
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user_info"] = None
        st.rerun()
else:
    choice = st.radio("Escolha uma opção:", ["Login", "Cadastrar"], horizontal=True)

    if choice == "Login":
        st.header("Faça seu Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar")
        if submit:
            try:
                user = pyrebase_auth.sign_in_with_email_and_password(email, password)
                st.session_state["logged_in"] = True
                st.session_state["user_info"] = user
                st.success("Login realizado com sucesso!")
                st.rerun()
            except Exception:
                st.error("Email ou senha incorretos. Tente novamente.")

    else:  # Cadastrar
        st.header("Crie sua Conta")
        with st.form("signup_form"):
            name = st.text_input("Nome Completo")
            email = st.text_input("Email")
            password = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Cadastrar")
        if submit:
            if not (name and email and password):
                st.warning("Por favor, preencha todos os campos.")
            else:
                try:
                    user = auth.create_user(email=email, password=password)
                    db.collection("users").document(user.uid).set({"name": name, "email": email})
                    st.success("Conta criada com sucesso! Você já pode fazer login.")
                except auth.EmailAlreadyExistsError:
                    st.error("Este email já está em uso.")
                except Exception as e:
                    st.error(f"Ocorreu um erro ao criar sua conta: {e}")
