import streamlit as st

def mostrar_kpis(df):
    ingresos = df["ingresos"].sum()
    gastos = df["gastos"].sum()
    utilidad = ingresos - gastos
    margen = (utilidad / ingresos * 100) if ingresos > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Ingresos totales", f"S/ {ingresos:,.0f}")
    col2.metric("📈 Utilidad neta", f"S/ {utilidad:,.0f}")
    col3.metric("📊 Margen bruto", f"{margen:.1f}%")
    col4.metric("💸 Gastos totales", f"S/ {gastos:,.0f}")
