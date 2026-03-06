import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuração da página para ficar com visual de app no celular
st.set_page_config(page_title="App CAO", layout="centered")

st.title("📱 Gestão de Atividades - CAO")

# Criando a conexão com o Google Sheets
# Importante: cole o link completo da sua planilha abaixo
url_planilha = "COLE_AQUI_O_LINK_DA_SUA_PLANILHA"

conn = st.connection("gsheets", type=GSheetsConnection)

# Lendo os dados da aba 'Dados'
try:
    dados = conn.read(spreadsheet=url_planilha, worksheet="Dados")
    # Limpando linhas vazias caso existam
    dados = dados.dropna(how="all")
except Exception as e:
    st.error(f"Erro ao carregar a planilha: Verifique o link e se a aba 'Dados' existe.")
    dados = pd.DataFrame()

# Mostrar os dados atuais para o grupo
st.subheader("📋 Cronograma Atual")
if not dados.empty:
    # Mostra os dados em formato de tabela interativa
    st.dataframe(dados, use_container_width=True, hide_index=True)
else:
    st.info("Nenhuma atividade cadastrada ainda.")

st.divider()

# Formulário para adicionar nova demanda
st.subheader("➕ Adicionar Nova Demanda")
with st.form("nova_demanda_form", clear_on_submit=True):
    tipo = st.selectbox("Tipo de Trabalho", ["Grupo de 6", "Grupo de 5", "Grupo de 3", "Individual"])
    disciplina = st.text_input("Disciplina (ex: Gestão Integrada de Crise)")
    docente = st.text_input("Docente (ex: Maj Tomás)")
    tema = st.text_input("Tema / Missão (ex: PEC 18)")
    responsaveis = st.text_input("Responsáveis")
    previsao = st.date_input("Previsão de Entrega")
    status = st.selectbox("Status", ["Pendente", "Em Andamento", "Concluído"])
    
    submit = st.form_submit_button("Salvar no Google Sheets")
    
    if submit:
        nova_linha = pd.DataFrame([{
            "TIPO": tipo,
            "DISCIPLINA": disciplina,
            "DOCENTE": docente,
            "TEMA": tema,
            "RESPONSAVEIS": responsaveis,
            "PREVISAO": previsao.strftime("%d/%m/%Y"),
            "STATUS": status
        }])
        
        # Junta o dado novo com os dados antigos
        dados_atualizados = pd.concat([dados, nova_linha], ignore_index=True)
        
        # Envia a atualização para o Google Sheets
        conn.update(worksheet="Dados", data=dados_atualizados)
        
        st.success("✅ Atividade adicionada com sucesso!")
        st.rerun() # Atualiza a tela instantaneamente