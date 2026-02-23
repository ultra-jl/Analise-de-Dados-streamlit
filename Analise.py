import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# CONFIGURAÇÃO STREAMLIT
# =========================================================

st.set_page_config(layout="wide", page_title="Dashboard de Vendas")
st.title("Informações Gerais")

# =========================================================
# FUNÇÕES
# =========================================================

def carregar_arquivo(caminho): 
    if caminho.endswith(".csv"):
        return pd.read_csv(caminho)
    elif caminho.endswith(".xlsx") or caminho.endswith(".xls"):
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
    df.rename(columns=mapa_colunas, inplace=True)
    df["Data_do_pedido"] = pd.to_datetime(df["Data_do_pedido"])
    return df

# =========================================================
# CARREGAMENTO
# =========================================================

# Nota: Certifique-se que o arquivo "vendas_loja.csv" está no mesmo diretório
df = carregar_arquivo("vendas_loja.csv")
df = padronizar_colunas(df)

# =========================================================
# FILTRO
# =========================================================

meses = sorted(df["Data_do_pedido"].dt.month.unique().tolist())
opcoes = ["Ano Todo"] + meses

filtro = st.sidebar.selectbox("Período (Mês)", opcoes)
if filtro == "Ano Todo":
    df_filtrado = df.copy()
else:
    df_filtrado = df[df["Data_do_pedido"].dt.month == filtro]

# =========================================================
# CÁLCULOS (Variáveis em minúsculo)
# =========================================================

# Agrupamentos temporais baseados no DF original para contexto anual
mes_serie = df["Data_do_pedido"].dt.month
lista_vendas_por_mes = df.groupby(mes_serie)["Quantidade"].sum()

mes_mais_vendas = lista_vendas_por_mes.idxmax()
mes_menos_vendas = lista_vendas_por_mes.idxmin()

faturamento_meses = df.groupby(mes_serie)["ValorTotal"].sum()
mes_top_faturamento = faturamento_meses.idxmax()
mes_bottom_faturamento = faturamento_meses.idxmin()

# Cálculos baseados no filtro lateral
faturamento_total = df_filtrado["ValorTotal"].sum()
faturamento_diario = df_filtrado.groupby("Data_do_pedido")["ValorTotal"].sum().reset_index()

crescimento = lista_vendas_por_mes.pct_change() * 100
crescimento = crescimento.fillna(0).round(2)
crescimento_df = crescimento.reset_index()
crescimento_df.columns = ["mes", "crescimento"]

# Produtos
lista_de_produtos = df_filtrado.groupby("Produto")["Quantidade"].sum()
produto_mais_vendido = lista_de_produtos.idxmax()
produto_menos_vendido = lista_de_produtos.idxmin()

faturamento_produtos = df_filtrado.groupby("Produto")["ValorTotal"].sum()
produto_mais_faturado = faturamento_produtos.idxmax()
produto_menos_faturado = faturamento_produtos.idxmin()

avaliacao_produto = df_filtrado.groupby("Produto")["Avaliação"].mean()
produto_top_avaliacao = avaliacao_produto.idxmax()
produto_bottom_avaliacao = avaliacao_produto.idxmin()

# Marcas e Cidades
lista_marcas_vendidas = df_filtrado.groupby("Marca")["Quantidade"].sum()
marca_top_vendida = lista_marcas_vendidas.idxmax()
marca_bottom_vendida = lista_marcas_vendidas.idxmin()

lista_cidades = df_filtrado.groupby("Cidade")["Quantidade"].sum()
cidade_mais_vendida = lista_cidades.idxmax()
cidade_menos_vendida = lista_cidades.idxmin()

faturamento_cidades = df_filtrado.groupby("Cidade")["ValorTotal"].sum()
cidade_top_faturamento = faturamento_cidades.idxmax()
cidade_bottom_faturamento = faturamento_cidades.idxmin()

# Dataframes para gráficos
vendas_mes_df = lista_vendas_por_mes.reset_index()
vendas_mes_df.columns = ["mes", "quantidade"]

faturamento_tipo_produtos = df_filtrado.groupby(["Categoria", "Cidade"])["ValorTotal"].sum().reset_index()

# =========================================================
# LAYOUT GRÁFICOS
# =========================================================

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

fig_faturamento = px.line(faturamento_diario, x="Data_do_pedido", y="ValorTotal", title="Faturamento Diário")
col1.plotly_chart(fig_faturamento, use_container_width=True)

fig_t_produtos = px.bar(faturamento_tipo_produtos, x="ValorTotal", y="Categoria",
                       orientation="h", color="Cidade", title="Faturamento por Categoria")
col2.plotly_chart(fig_t_produtos, use_container_width=True)

fig_vendas_mes = px.bar(vendas_mes_df, x="mes", y="quantidade", title="Vendas por Mês")
col3.plotly_chart(fig_vendas_mes, use_container_width=True)

fig_crescimento = px.line(crescimento_df, x="mes", y="crescimento",
                          title="Crescimento % Mês a Mês", markers=True)
fig_crescimento.add_hline(y=0)
col4.plotly_chart(fig_crescimento, use_container_width=True)

fig_av_produto = px.bar(df_filtrado.groupby("Produto")["Avaliação"].mean().reset_index(),
                       x="Avaliação", y="Produto", title="Avaliação por Produto")
col5.plotly_chart(fig_av_produto, use_container_width=True)

# =========================================================
# RESUMO ESTRATÉGICO
# =========================================================

st.divider()
st.header("📊 Resumo Estratégico")

# Cidades
st.subheader("🏙 Cidades")
c1, c2, c3, c4 = st.columns(4)
c1.metric("🏆 Maior Faturamento", cidade_top_faturamento)
c2.metric("📉 Menor Faturamento", cidade_bottom_faturamento)
c3.metric("📦 Mais Vendas", cidade_mais_vendida)
c4.metric("⚠️ Menos Vendas", cidade_menos_vendida)

# Meses
st.subheader("📅 Meses")
m1, m2, m3, m4 = st.columns(4)
m1.metric("📈 Mais Vendas (Mês)", mes_mais_vendas)
m2.metric("📉 Menos Vendas (Mês)", mes_menos_vendas)
m3.metric("💰 Maior Faturamento", mes_top_faturamento)
m4.metric("💸 Menor Faturamento", mes_bottom_faturamento)

# Produtos
st.subheader("📦 Produtos")
p1, p2, p3, p4 = st.columns(4)
p1.metric("🏆 Mais Faturado", produto_mais_faturado)
p2.metric("📉 Menos Faturado", produto_menos_faturado)
p3.metric("⭐ Melhor Avaliação", produto_top_avaliacao)
p4.metric("⚠️ Pior Avaliação", produto_bottom_avaliacao)

# Marcas e Totais
st.subheader("🏷 Marcas e Visão Geral")
b1, b2, b3, b4 = st.columns(4)
b1.metric("📦 Marca Mais Vendida", marca_top_vendida)
b2.metric("💰 Faturamento Total", f"R$ {faturamento_total:,.2f}")
b3.metric("📦 Total de Itens", df_filtrado["Quantidade"].sum())
b4.metric("🧾 Total de Pedidos", df_filtrado.shape[0])

st.divider()
st.subheader("📋 Dados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)
