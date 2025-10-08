# pages/1_Dashboard.py
import streamlit as st
from firebase_admin import firestore

st.set_page_config(page_title="Dashboard", layout="wide")

# --- CONTROLE DE ACESSO ---
if not st.session_state.get("logged_in", False):
    st.error("Você precisa estar logado para acessar esta página.")
    # st.page_link funciona em versões mais novas; se der erro, troque por st.switch_page("app.py")
    try:
        st.page_link("app.py", label="Voltar para o Login")
    except Exception:
        pass
    st.stop()

# --- FIRESTORE E USER INFO ---
db = firestore.client()
user_info = st.session_state["user_info"]
user_uid = user_info["localId"]
user_email = user_info["email"]

try:
    user_doc = db.collection("users").document(user_uid).get()
    user_name = user_doc.to_dict().get("name", "Usuário") if user_doc.exists else "Usuário"
except Exception as e:
    user_name = "Usuário"
    st.error(f"Não foi possível buscar seu nome: {e}")

# --- SIDEBAR ---
st.sidebar.header(f"Bem-vindo, {user_name}!")
if st.sidebar.button("Logout", use_container_width=True):
    st.session_state["logged_in"] = False
    st.session_state["user_info"] = None
    st.switch_page("app.py")

# --- CSS: remove header nativo e espaços extras ---
st.markdown(
    """
<style>
/* some temas usam header fixo invisível: remova-o */
header[data-testid="stHeader"] { display: none; }

/* zera padding/margin do container principal */
.block-container{
  padding: 0 !important;
  margin: 0 !important;
  max-width: 100% !important;
}

/* zera qualquer margem/padding do main */
main { padding: 0 !important; margin: 0 !important; }

/* wrapper do iframe ocupando quase toda a viewport */
.powerbi-wrap{
  width: 100%;
  height: 95vh;              /* ajuste fino: 95–98vh */
  margin: 0; padding: 0;
}
.powerbi-wrap iframe{
  width: 100%;
  height: 100%;
  border: 0;
}

/* opcional: reduzir padding da sidebar para alinhar melhor com o topo */
section[data-testid="stSidebar"] .css-ng1t4o,  /* fallback temas antigos */
section[data-testid="stSidebar"] .stSidebarContent{
  padding-top: .5rem !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# --- CABEÇALHO DA PÁGINA (compacto) ---
st.markdown(
    f"""
<div style="padding:12px 16px;">
  <h1 style="margin:0;">📊 Seu Dashboard Protegido</h1>
  <p style="margin:.25rem 0 0 0;">Você está logado com o email: <b>{user_email}</b></p>
</div>
<hr style="margin:8px 0 12px 0;"/>
<div style="padding:0 16px 8px 16px;">
  <h2 style="margin:0;">Conteúdo Exclusivo</h2>
  <p style="margin:.25rem 0 0 0;">Quadro de Gestão.</p>
</div>
""",
    unsafe_allow_html=True,
)

# --- EMBED POWER BI (sem wrapper do components.html) ---
st.markdown(
    """
<div class="powerbi-wrap">
  <iframe
    src="https://app.powerbi.com/reportEmbed?reportId=61282380-19b2-486f-a25f-ed2f45b3beae&autoAuth=true&ctid=cae7d061-08f3-40dd-80c3-3c0b8889224a&actionBarEnabled=false&reportCopilotInEmbed=false"
    allowfullscreen="true">
  </iframe>
</div>
""",
    unsafe_allow_html=True,
)
