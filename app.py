# app.py
import streamlit as st

st.set_page_config(page_title="HOME", page_icon="🏠", layout="wide")

# 👉 NÃO registre app.py como página
home = st.Page("pages/0_Home.py",           title="🏠 Início")
dash = st.Page("pages/1_Dashboard.py",      title="📊 Dashboard")
mpp  = st.Page("pages/2_MppReader.py",      title="🗂️ Leitor de Arquivos MPP")
docs = st.Page("pages/3_DocsTemplates.py", title="📚 Documentação & Templates")
pg = st.navigation({"Menu Principal": [home, dash, mpp, docs]})

pg.run()
