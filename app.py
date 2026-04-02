import streamlit as st
import pandas as pd
from components.kpis import mostrar_kpis, mostrar_metas
from components.graficos import grafico_ingresos_gastos, grafico_gastos, grafico_barras_horizontal
from components.tabla import tabla_categorias

st.set_page_config(
    page_title="Panel Financiero | Retail",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    .main { background-color: #F4F6FB; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F2044 0%, #1B3A6B 100%);
        border-right: none;
    }
    section[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
    section[data-testid="stSidebar"] .stSelectbox label { color: #94A3B8 !important; font-size: 12px !important; }
    div[data-testid="metric-container"] {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 2px 8px rgba(15,32,68,0.06);
    }
    div[data-testid="metric-container"] label { color: #64748B !important; font-size: 13px !important; }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #0F2044 !important; font-size: 26px !important; font-weight: 700 !important; }
    .stProgress > div > div { background: #2563EB !important; border-radius: 8px; }
    h1, h2, h3 { color: #0F2044 !important; }
    .st-emotion-cache-1wivap2 { background: white; border-radius: 16px; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:4px;">
    <div style="display:flex; align-items:center; gap:14px;">
        <div style="background:#2563EB; border-radius:14px; padding:10px 14px;">
            <span style="font-size:24px;">📊</span>
        </div>
        <div>
            <h1 style="margin:0; font-size:26px; color:#0F2044; font-weight:700;">Panel Financiero</h1>
            <p style="margin:0; color:#64748B; font-size:13px;">Tienda Retail · Análisis automatizado</p>
        </div>
    </div>
    <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:10px; padding:8px 16px;">
        <p style="margin:0; color:#1D4ED8; font-size:12px; font-weight:600;">● EN VIVO</p>
    </div>
</div>
<hr style="border:none; border-top:1px solid #E2E8F0; margin:16px 0 20px;">
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<p style='font-size:11px; color:#94A3B8; font-weight:600; letter-spacing:0.08em; margin-bottom:4px;'>DATOS</p>", unsafe_allow_html=True)
    archivo = st.file_uploader("Subir Excel o CSV", type=["csv", "xlsx"])
    st.markdown("<hr style='border-color:#1E3A5F; margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px; color:#94A3B8; font-weight:600; letter-spacing:0.08em; margin-bottom:4px;'>FILTROS</p>", unsafe_allow_html=True)

if archivo:
    df = pd.read_csv(archivo) if archivo.name.endswith(".csv") else pd.read_excel(archivo)
    st.sidebar.success("✓ Archivo cargado")
else:
    df = pd.read_csv("data/ventas_ejemplo.csv")
    st.sidebar.info("Usando datos de ejemplo")

meses = ["Todos"] + sorted(df["mes"].unique().tolist())
mes_sel = st.sidebar.selectbox("Mes", meses)
df_filtrado = df[df["mes"] == mes_sel] if mes_sel != "Todos" else df

# Meta mensual configurable
st.sidebar.markdown("<hr style='border-color:#1E3A5F; margin:16px 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:11px; color:#94A3B8; font-weight:600; letter-spacing:0.08em; margin-bottom:4px;'>METAS</p>", unsafe_allow_html=True)
meta_ingresos = st.sidebar.number_input("Meta de ingresos (S/)", min_value=0, value=100000, step=5000)
meta_utilidad = st.sidebar.number_input("Meta de utilidad (S/)", min_value=0, value=30000, step=1000)

# KPIs
mostrar_kpis(df_filtrado)

st.markdown("<br>", unsafe_allow_html=True)

# Metas
mostrar_metas(df_filtrado, meta_ingresos, meta_utilidad)

st.markdown("<br>", unsafe_allow_html=True)

# Gráficos
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 📈 Tendencia mensual")
    grafico_ingresos_gastos(df)
with col2:
    st.markdown("#### 🔵 Composición de gastos")
    grafico_gastos(df_filtrado)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### 📦 Ingresos por categoría")
grafico_barras_horizontal(df_filtrado)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### 🏷️ Rentabilidad por categoría")
tabla_categorias(df_filtrado)

st.markdown("""
<hr style="border:none; border-top:1px solid #E2E8F0; margin-top:2rem;">
<p style="text-align:center; color:#94A3B8; font-size:12px;">Panel Financiero Retail · Python & Streamlit · Desarrollado por Ismael Rodriguez</p>
""", unsafe_allow_html=True)
