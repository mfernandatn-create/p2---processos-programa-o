# app.py - Judicialização da Saúde no Brasil
# Autora: Maria Fernanda Torres

import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Judicialização da Saúde - P2", layout="wide")

st.title("⚖️ Judicialização da Saúde no Brasil")
st.write(
    """
    Esta aplicação permite analisar decisões judiciais relacionadas à saúde,
    com foco em fornecimento de medicamentos, tratamentos e outros pedidos.
    Envie uma base de dados em CSV para visualizar métricas e gráficos.
    """
)

st.markdown("**Estrutura esperada do arquivo CSV:**")
st.code("ano, tipo_pedido, tribunal, valor_causa, resultado, fundamento_legal", language="text")

# Upload do arquivo
arquivo = st.file_uploader("Envie a base de dados (formato .csv)", type=["csv"])

if arquivo is not None:
    # Lê o CSV enviado
    df = pd.read_csv(arquivo)

    st.subheader("Prévia dos dados")
    st.dataframe(df.head())

    st.write("Colunas encontradas na base:")
    st.write(list(df.columns))

    # ---------------- RESUMO GERAL ----------------
    st.subheader("Resumo geral")

    total_acoes = len(df)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de ações analisadas", total_acoes)

    # índice de deferimentos (se coluna "resultado" existir)
    if "resultado" in df.columns:
        # normaliza texto pra evitar diferença Deferido/deferido
        resultados_normalizados = df["resultado"].astype(str).str.strip().str.lower()
        deferidas = resultados_normalizados[resultados_normalizados == "deferido"].shape[0]
        perc_deferidas = (deferidas / total_acoes * 100) if total_acoes > 0 else 0

        with col2:
            st.metric("Ações deferidas", deferidas)

        with col3:
            st.metric("Índice de deferimento", f"{perc_deferidas:.2f}%")
    else:
        st.info("Coluna 'resultado' não encontrada. Não foi possível calcular o índice de deferimentos.")

    st.markdown("---")

    # ---------------- GRÁFICO: AÇÕES POR ANO ----------------
    if "ano" in df.columns:
        st.subheader("📈 Evolução do número de ações por ano")

        evolucao = df.groupby("ano").size().reset_index(name="numero_acoes")
        evolucao = evolucao.sort_values("ano")

        st.line_chart(evolucao.set_index("ano"))
    else:
        st.info("Coluna 'ano' não encontrada. Não foi possível gerar o gráfico de evolução anual.")

    # ---------------- GRÁFICO: TIPOS DE PEDIDO ----------------
    if "tipo_pedido" in df.columns:
        st.subheader("📊 Tipos de pedido mais comuns")

        tipos = df["tipo_pedido"].value_counts().reset_index()
        tipos.columns = ["tipo_pedido", "quantidade"]

        st.bar_chart(tipos.set_index("tipo_pedido"))
    else:
        st.info("Coluna 'tipo_pedido' não encontrada. Não foi possível gerar o gráfico de tipos de pedido.")

    # ---------------- GRÁFICO: RESULTADO DOS JULGAMENTOS ----------------
    if "resultado" in df.columns:
        st.subheader("📊 Distribuição dos resultados dos julgamentos")

        resultados = df["resultado"].value_counts().reset_index()
        resultados.columns = ["resultado", "quantidade"]

        st.bar_chart(resultados.set_index("resultado"))
    else:
        st.info("Coluna 'resultado' não encontrada. Não foi possível gerar o gráfico de resultados.")

    # ---------------- RESUMO ESTATÍSTICO DO VALOR DA CAUSA ----------------
    if "valor_causa" in df.columns:
        st.subheader("📄 Resumo estatístico do valor da causa")

        # tenta converter pra número, se vier como texto
        df["valor_causa_num"] = pd.to_numeric(df["valor_causa"], errors="coerce")
        st.dataframe(df[["valor_causa_num"]].describe())
    else:
        st.info("Coluna 'valor_causa' não encontrada. Não foi possível gerar o resumo estatístico.")

    st.success("Análise concluída! Explore os gráficos e métricas acima.")
else:
    st.info("Envie um arquivo CSV para iniciar a análise.")

