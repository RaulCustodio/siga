# pages/3_DocsTemplates.py
import streamlit as st
from pathlib import Path
import mimetypes

st.set_page_config(page_title="📚 Documentação & Templates", layout="wide")

# Caminho base para os arquivos
BASE_DIR = Path(__file__).resolve().parents[1] / "static" / "docs"
BASE_DIR.mkdir(parents=True, exist_ok=True)

st.title("📚 Documentação & Templates")
st.write("Arquivos disponíveis na pasta `static/docs/` e suas subpastas:")

# Função para listar todos os arquivos
def listar_arquivos(base_dir: Path):
    arquivos = []
    for p in base_dir.rglob("*"):
        if p.is_file():
            arquivos.append(p)
    return arquivos

arquivos = listar_arquivos(BASE_DIR)

if not arquivos:
    st.info("Nenhum arquivo encontrado. Adicione arquivos em `static/docs`.")
else:
    for arquivo in arquivos:
        nome_exibicao = arquivo.relative_to(BASE_DIR)
        mime_type, _ = mimetypes.guess_type(arquivo.name)

        st.download_button(
            label=f"📄 {nome_exibicao}",
            data=arquivo.read_bytes(),
            file_name=arquivo.name,
            mime=mime_type or "application/octet-stream",
            key=str(nome_exibicao)
        )
