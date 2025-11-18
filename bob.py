# bob.py - Análise da Judicialização da Saúde
# Autora: Maria Fernanda Torres

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Judicialização da Saúde - P2", layout="wide")

st.title("⚖️ Judicialização da Saúde no Brasil")
st.write(
    "Aplicação para analisar decisões judiciais sobre fornecimento de medicamentos e tratamentos, "
    "a partir de uma base de dados em CSV."
)

st.markdown("**Estrutura esperada do arquivo CSV:**")
st.code("ano, tipo_pedido, tribunal, valor_causa, resultado, fundamento_legal", language="text")

arquivo = st.file_uploader("Envie a base de dados (formato .csv)", type=["csv"])

if arquivo is not None:
    # Lê a base
    df = pd.read_csv(arquivo)

    st.subheader("Prévia dos dados")
    st.dataframe(df.head())

    st.write("Colunas encontradas:")
    st.write(list(df.columns))

    # -------- Resumo geral --------
    st.subheader("Resumo geral")

    total_acoes = len(df)
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total de ações analisadas", total_acoes)

    with col2:
        if "resultado" in df.columns:
            deferidas = df[df["resultado"].str.lower() == "deferido"].shape[0]
            if total_acoes > 0:
                perc = deferidas / total_acoes * 100
            else:
                perc = 0
            st.metric("Índice de deferimentos", f"{perc:.2f}%")
        else:
            st.info("Coluna 'resultado' não encontrada na base.")

    # -------- Gráfico: evolução anual --------
    if "ano" in df.columns:
        st.subheader("📈 Evolução de ações por ano")
        evolucao = df.groupby("ano").size().reset_index(name="numero_acoes")
        st.line_chart(evolucao.set_index("ano"))
    else:
        st.info("Coluna 'ano' não encontrada. Não foi possível gerar o gráfico de evolução.")

    # -------- Gráfico: tipos de pedido --------
    if "tipo_pedido" in df.columns:
        st.subheader("📊 Tipos de pedido mais comuns")
        tipos = df["tipo_pedido"].value_counts().reset_index()
        tipos.columns = ["tipo_pedido", "quantidade"]
        st.bar_chart(tipos.set_index("tipo_pedido"))
    else:
        st.info("Coluna 'tipo_pedido' não encontrada. Não foi possível gerar o gráfico de tipos de pedido.")

    # -------- Gráfico: resultados (deferido x indeferido etc.) --------
    if "resultado" in df.columns:
        st.subheader("📊 Distribuição dos resultados dos julgamentos")
        resultados = df["resultado"].value_counts().reset_index()
        resultados.columns = ["resultado", "quantidade"]
        st.bar_chart(resultados.set_index("resultado"))
    else:
        st.info("Coluna 'resultado' não encontrada. Não foi possível gerar o gráfico de resultados.")

    # -------- Resumo estatístico de valores --------
    if "valor_causa" in df.columns:
        st.subheader("📄 Resumo estatístico do valor da causa")
        st.dataframe(df[["valor_causa"]].describe())
    else:
        st.info("Coluna 'valor_causa' não encontrada. Não foi possível gerar o resumo estatístico.")

else:
    st.info("Envie um arquivo CSV para iniciar a análise.")

