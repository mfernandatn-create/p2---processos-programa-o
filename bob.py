# app.py - Análise da Judicialização da Saúde no Brasil
# Autora: Maria Fernanda Torres

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Judicialização da Saúde - P2", layout="wide")

st.title("⚖️ Judicialização da Saúde no Brasil")
st.subheader("Análise de decisões judiciais sobre fornecimento de medicamentos e tratamentos médicos")

st.write("Envie um arquivo CSV com os seguintes campos:")
st.code("ano, tipo_pedido, tribunal, valor_causa, resultado, fundamento_legal", language="text")

arquivo = st.file_uploader("Envie a base de dados", type=["csv"])

if arquivo is not None:
    df = pd.read_csv(arquivo)

    st.subheader("Prévia dos dados")
    st.dataframe(df.head())

    st.write("Colunas identificadas no arquivo:")
    st.write(list(df.columns))

    # Resumo geral
    st.subheader("Resumo geral dos dados")

    col1, col2 = st.columns(2)

    with col1:
        total_acoes = len(df)
        st.metric("Total de ações analisadas", total_acoes)

    with col2:
        if "resultado" in df.columns:
            deferidas = df[df["resultado"] == "Deferido"].shape[0]
            percentual = (deferidas / total_acoes) * 100
            st.metric("Índice de deferimentos", f"{percentual:.2f}%")

    # Gráfico: evolução anual
    if "ano" in df.columns:
        st.subheader("📈 Evolução de ações judiciais ao longo dos anos")
        fig1, ax1 = plt.subplots()
        df.groupby("ano")["ano"].count().plot(kind="line", marker="o", ax=ax1)
        ax1.set_ylabel("Número de ações")
        st.pyplot(fig1)

    # Gráfico: tipos de pedido
    if "tipo_pedido" in df.columns:
        st.subheader("📊 Tipos de pedido mais comuns")
        fig2, ax2 = plt.subplots()
        df["tipo_pedido"].value_counts().plot(kind="bar", ax=ax2)
        ax2.set_ylabel("Quantidade")
        st.pyplot(fig2)

    # Gráfico de pizza: deferimentos x indeferimentos
    if "resultado" in df.columns:
        st.subheader("🥧 Resultado dos julgamentos")
        fig3, ax3 = plt.subplots()
        df["resultado"].value_counts().plot(kind="pie", autopct='%1.1f%%', ax=ax3)
        ax3.set_ylabel("")
        st.pyplot(fig3)

    # Resumo estatístico
    st.subheader("📄 Resumo estatístico descritivo")
    if "valor_causa" in df.columns:
        st.dataframe(df[["valor_causa"]].describe())

    st.success("Análise concluída! Explore os gráficos e métricas acima.")
else:
    st.info("Por favor, envie um arquivo CSV para iniciar a análise.")
