import streamlit as st
import pandas as pd
from components.kpis import mostrar_kpis, mostrar_metas
from components.graficos import grafico_ingresos_gastos, grafico_gastos, grafico_barras_horizontal
from components.tabla import tabla_categorias, mostrar_recomendaciones

st.set_page_config(page_title="Panel Financiero | Retail", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    div[data-testid="metric-container"] {
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 2px 12px rgba(108,63,232,0.08);
    }
    div[data-testid="metric-container"] label { font-size: 13px !important; }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] { font-size: 26px !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:4px;">
    <div style="display:flex; align-items:center; gap:14px;">
        <div style="background:#6C3FE8; border-radius:14px; padding:10px 14px;">
            <span style="font-size:24px;">📊</span>
        </div>
        <div>
            <h1 style="margin:0; font-size:26px; font-weight:700;">Panel Financiero</h1>
            <p style="margin:0; font-size:13px; color:#64748B;">Tienda Retail · Análisis automatizado</p>
        </div>
    </div>
    <div style="background:#F3EFFE; border:1px solid #D4BAFB; border-radius:10px; padding:8px 16px;">
        <p style="margin:0; color:#6C3FE8; font-size:12px; font-weight:600;">● EN VIVO</p>
    </div>
</div>
<hr style="border:none; border-top:1px solid #E2E8F0; margin:16px 0 20px;">
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Configuración")
    st.markdown("---")
    archivo = st.file_uploader("Subir Excel o CSV", type=["csv","xlsx"])
    st.markdown("---")
    meses_label = ""

if archivo:
    df = pd.read_csv(archivo) if archivo.name.endswith(".csv") else pd.read_excel(archivo)
    st.sidebar.success("✓ Archivo cargado")
else:
    df = pd.read_csv("data/ventas_ejemplo.csv")
    st.sidebar.info("Usando datos de ejemplo")

meses   = ["Todos"] + sorted(df["mes"].unique().tolist())
mes_sel = st.sidebar.selectbox("Filtrar por mes", meses)
df_fil  = df[df["mes"] == mes_sel] if mes_sel != "Todos" else df

st.sidebar.markdown("---")
meta_ing  = st.sidebar.number_input("Meta ingresos (S/)",  min_value=0, value=100000, step=5000)
meta_util = st.sidebar.number_input("Meta utilidad (S/)", min_value=0, value=30000,  step=1000)

tab1, tab2, tab3 = st.tabs(["📊 Resumen General", "📈 Análisis de Ventas", "💡 Recomendaciones"])

with tab1:
    mostrar_kpis(df_fil)
    st.markdown("<br>", unsafe_allow_html=True)
    mostrar_metas(df_fil, meta_ing, meta_util)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Tendencia mensual")
        grafico_ingresos_gastos(df)
    with col2:
        st.markdown("#### Composición de gastos")
        grafico_gastos(df_fil)
    st.markdown("#### Ingresos por categoría")
    grafico_barras_horizontal(df_fil)
    st.markdown("#### Rentabilidad por categoría")
    tabla_categorias(df_fil)

with tab3:
    st.markdown("#### 💡 Recomendaciones automáticas basadas en tus datos")
    mostrar_recomendaciones(df_fil)

st.markdown("""
<hr style="border:none; border-top:1px solid #E2E8F0; margin-top:2rem;">
<p style="text-align:center; color:#94A3B8; font-size:12px;">Panel Financiero Retail · Python & Streamlit · Desarrollado por Ismael Rodriguez</p>
""", unsafe_allow_html=True)
