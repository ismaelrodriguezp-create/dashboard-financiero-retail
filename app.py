import streamlit as st
import pandas as pd
from components.kpis import mostrar_kpis
from components.graficos import grafico_ingresos_gastos, grafico_gastos
from components.tabla import tabla_categorias

st.set_page_config(
    page_title="Dashboard Financiero",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Financiero — Tienda Retail")
st.markdown("---")

archivo = st.sidebar.file_uploader("Sube tu archivo Excel o CSV", type=["csv", "xlsx"])

if archivo:
    if archivo.name.endswith(".csv"):
        df = pd.read_csv(archivo)
    else:
        df = pd.read_excel(archivo)
    st.sidebar.success("Archivo cargado correctamente")
else:
    df = pd.read_csv("data/ventas_ejemplo.csv")
    st.sidebar.info("Usando datos de ejemplo")

meses = ["Todos"] + sorted(df["mes"].unique().tolist())
mes_sel = st.sidebar.selectbox("Filtrar por mes", meses)

if mes_sel != "Todos":
    df_filtrado = df[df["mes"] == mes_sel]
else:
    df_filtrado = df

mostrar_kpis(df_filtrado)

st.markdown("### Tendencia de ingresos y gastos")
col1, col2 = st.columns(2)
with col1:
    grafico_ingresos_gastos(df)
with col2:
    grafico_gastos(df_filtrado)

st.markdown("### Rentabilidad por categoría")
tabla_categorias(df_filtrado)
