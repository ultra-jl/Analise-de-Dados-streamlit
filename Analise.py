import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# CONFIGURAÇÃO STREAMLIT
# =========================================================

st.set_page_config(layout="wide")
st.title("📊 Informações Gerais")

# =========================================================
# FUNÇÕES
# =========================================================

def carregar_arquivo(caminho): 
    if caminho.endswith(".csv"):
        return pd.read_csv(caminho)
    elif caminho.endswith((".xlsx", ".xls")):
        return pd.read_excel(caminho)
    elif caminho.endswith(".json"):
        return pd.read_json(caminho)
    else:
        st.error("Formato não suportado")
        return None


def padronizar_colunas(df):     
    mapa_colunas = {
        "Product": "Produto",
        "Category": "Categoria",
        "Brand": "Marca",
        "Platform": "Plataforma",
        "City": "Cidade",
        "Price": "Preço",
        "Amount": "Valor",
        "Quantity": "Quantidade",
        "TotalAmount": "ValorTotal",
        "Rating": "Avaliação",
        "Reviews": "Avaliações",
        "OrderDate": "Data_do_pedido"
    }

    df = df.rename(columns=mapa_colunas)
    df["Data_do_pedido"] = pd.to_datetime(df["Data_do_pedido"])
    return df


# =========================================================
# CARREGAMENTO
# =========================================================

df = carregar_arquivo("vendas_loja.csv")
df = padronizar_colunas(df)

# =========================================================
# FILTRO
# =========================================================

meses = sorted(df["Data_do_pedido"].dt.month.unique())
opcoes = ["Ano Todo"] + meses

filtro = st.sidebar.selectbox("📅 Período", opcoes)

if filtro == "Ano Todo":
    df_filtrado = df.copy()
else:
    df_filtrado = df[df["Data_do_pedido"].dt.month == filtro]

# =========================================================
# CÁLCULOS (AGORA TUDO USA df_filtrado)
# =========================================================

# Agrupamento mensal
vendas_por_mes = (
    df_filtrado
    .groupby(df_filtrado["Data_do_pedido"].dt.month)["Quantidade"]
    .sum()
)

vendas_mes_df = vendas_por_mes.reset_index()
vendas_mes_df.columns = ["Mes", "Quantidade"]

# Crescimento mensal
crescimento = vendas_por_mes.pct_change().fillna(0) * 100
crescimento = crescimento.round(2)
crescimento_df = crescimento.reset_index()
crescimento_df.columns = ["Mes", "Crescimento"]

# Faturamento
faturamento_total = df_filtrado["ValorTotal"].sum()
faturamento_diario = (
    df_filtrado
    .groupby("Data_do_pedido")["ValorTotal"]
    .sum()
    .reset_index()
)

# Produtos
produto_vendas = df_filtrado.groupby("Produto")["Quantidade"].sum()
produto_faturamento = df_filtrado.groupby("Produto")["ValorTotal"].sum()
produto_avaliacao = df_filtrado.groupby("Produto")["Avaliação"].mean()

# Marcas
marca_vendas = df_filtrado.groupby("Marca")["Quantidade"].sum()

# Cidades
cidade_vendas = df_filtrado.groupby("Cidade")["Quantidade"].sum()
cidade_faturamento = df_filtrado.groupby("Cidade")["ValorTotal"].sum()

# Categoria x Cidade
faturamento_categoria = (
    df_filtrado
    .groupby(["Categoria", "Cidade"])["ValorTotal"]
    .sum()
    .reset_index()
)

# =========================================================
# LAYOUT GRÁFICOS
# =========================================================

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

fig_faturamento = px.line(
    faturamento_diario,
    x="Data_do_pedido",
    y="ValorTotal",
    title="💰 Faturamento Diário"
)
col1.plotly_chart(fig_faturamento, use_container_width=True)

fig_categoria = px.bar(
    faturamento_categoria,
    x="ValorTotal",
    y="Categoria",
    orientation="h",
    color="Cidade",
    title="📦 Faturamento por Categoria"
)
col2.plotly_chart(fig_categoria, use_container_width=True)

fig_vendas_mes = px.bar(
    vendas_mes_df,
    x="Mes",
    y="Quantidade",
    title="📅 Vendas por Mês"
)
col3.plotly_chart(fig_vendas_mes, use_container_width=True)

fig_crescimento = px.line(
    crescimento_df,
    x="Mes",
    y="Crescimento",
    title="📈 Crescimento Mensal (%)",
    markers=True
)
fig_crescimento.add_hline(y=0)
col4.plotly_chart(fig_crescimento, use_container_width=True)

fig_avaliacao = px.bar(
    produto_avaliacao.reset_index(),
    x="Avaliação",
    y="Produto",
    title="⭐ Avaliação por Produto"
)
col5.plotly_chart(fig_avaliacao, use_container_width=True)

# =========================================================
# RESUMO ESTRATÉGICO
# =========================================================

st.divider()
st.header("📊 Resumo Estratégico")

# KPI PRINCIPAL
k1, k2, k3 = st.columns(3)
k1.metric("💰 Faturamento Total", f"R$ {faturamento_total:,.2f}")
k2.metric("📦 Total de Vendas", df_filtrado["Quantidade"].sum())
k3.metric("🧾 Total de Pedidos", df_filtrado.shape[0])

st.divider()
st.subheader("📋 Dados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)