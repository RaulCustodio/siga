# app.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import pyrebase

# --- INICIALIZAÇÃO DO FIREBASE ---

# Inicializa o app do Firebase Admin (para operações de backend)
# Usamos @st.cache_resource para garantir que isso rode apenas uma vez.
@st.cache_resource
def initialize_firebase_admin():
    # Verifica se o app já foi inicializado
    if not firebase_admin._apps:
        # st.secrets lê o arquivo .streamlit/secrets.toml
        cred = credentials.Certificate(dict(st.secrets["firebase_service_account"]))
        firebase_admin.initialize_app(cred)
    return firebase_admin.get_app()

# Inicializa o cliente Pyrebase (para autenticação de cliente)
@st.cache_resource
def initialize_pyrebase():
    config = dict(st.secrets["firebase_web_config"])
    return pyrebase.initialize_app(config)

app_admin = initialize_firebase_admin()
pyrebase_auth = initialize_pyrebase().auth()
db = firestore.client()

# --- GERENCIAMENTO DE ESTADO ---
# Inicializa o st.session_state para controlar o estado de login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = None

# --- INTERFACE DA APLICAÇÃO ---

st.set_page_config(page_title="App com Firebase", layout="centered")

st.title("Bem-vindo à Aplicação 🚀")

# Se o usuário já estiver logado, mostre uma mensagem e o link para o dashboard
if st.session_state['logged_in']:
    user_email = st.session_state['user_info']['email']
    st.success(f"Você está logado como: {user_email}")
    st.page_link("pages/1_Dashboard.py", label="Acessar o Dashboard")
    
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['user_info'] = None
        st.rerun()

# Se não estiver logado, mostre as abas de Login e Cadastro
else:
    choice = st.radio("Escolha uma opção:", ('Login', 'Cadastrar'), horizontal=True)

    if choice == 'Login':
        st.header("Faça seu Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Senha", type="password")
            submit_button = st.form_submit_button("Login")

            if submit_button:
                try:
                    user = pyrebase_auth.sign_in_with_email_and_password(email, password)
                    st.session_state['logged_in'] = True
                    st.session_state['user_info'] = user
                    st.success("Login realizado com sucesso!")
                    st.rerun() # Recarrega a página para mostrar o estado logado
                except Exception as e:
                    st.error("Email ou senha incorretos. Por favor, tente novamente.")
                    # st.error(e) # descomente para ver o erro completo

    elif choice == 'Cadastrar':
        st.header("Crie sua Conta")
        with st.form("signup_form"):
            name = st.text_input("Nome Completo")
            email = st.text_input("Email")
            password = st.text_input("Senha", type="password")
            submit_button = st.form_submit_button("Cadastrar")

            if submit_button:
                if name and email and password:
                    try:
                        # Cria o usuário na Autenticação do Firebase
                        user = auth.create_user(email=email, password=password)
                        
                        # Salva informações adicionais (nome) no Firestore
                        user_data = {"name": name, "email": email}
                        db.collection("users").document(user.uid).set(user_data)
                        
                        st.success("Conta criada com sucesso! Você já pode fazer o login.")
                    except auth.EmailAlreadyExistsError:
                        st.error("Este email já está em uso. Por favor, escolha outro.")
                    except Exception as e:
                        st.error(f"Ocorreu um erro: {e}")
                else:
                    st.warning("Por favor, preencha todos os campos.")