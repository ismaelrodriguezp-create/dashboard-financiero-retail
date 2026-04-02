import streamlit as st

def mostrar_kpis(df):
    ingresos = df["ingresos"].sum()
    gastos   = df["gastos"].sum()
    utilidad = ingresos - gastos
    margen   = (utilidad / ingresos * 100) if ingresos > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Ingresos totales", f"S/ {ingresos:,.0f}", delta="↑ 12.4% vs mes anterior")
    col2.metric("📈 Utilidad neta",    f"S/ {utilidad:,.0f}", delta="↑ 8.1% vs mes anterior")
    col3.metric("📊 Margen bruto",     f"{margen:.1f}%",      delta="↓ 1.2%", delta_color="inverse")
    col4.metric("💸 Gastos totales",   f"S/ {gastos:,.0f}",   delta="↑ 5.3%", delta_color="inverse")

def mostrar_metas(df, meta_ingresos, meta_utilidad):
    ingresos  = df["ingresos"].sum()
    utilidad  = ingresos - df["gastos"].sum()
    porc_ing  = min(ingresos / meta_ingresos, 1.0) if meta_ingresos > 0 else 0
    porc_util = min(utilidad / meta_utilidad, 1.0) if meta_utilidad > 0 else 0

    st.markdown("""
    <div style="background:white; border-radius:16px; padding:20px 24px;
                border:1px solid #E2E8F0; box-shadow:0 2px 8px rgba(108,63,232,0.07);">
        <p style="margin:0 0 16px; font-size:14px; font-weight:600; color:#1B2A4A;">
            🎯 Progreso hacia metas del mes
        </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<p style='font-size:13px; color:#64748B; margin-bottom:6px;'>Ingresos <span style='float:right; font-weight:600; color:#1B2A4A;'>S/ {ingresos:,.0f} / S/ {meta_ingresos:,.0f}</span></p>", unsafe_allow_html=True)
        st.progress(porc_ing)
        st.markdown(f"<p style='font-size:12px; color:#6C3FE8; margin-top:4px;'>{porc_ing*100:.1f}% completado</p>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p style='font-size:13px; color:#64748B; margin-bottom:6px;'>Utilidad <span style='float:right; font-weight:600; color:#1B2A4A;'>S/ {utilidad:,.0f} / S/ {meta_utilidad:,.0f}</span></p>", unsafe_allow_html=True)
        st.progress(porc_util)
        st.markdown(f"<p style='font-size:12px; color:#6C3FE8; margin-top:4px;'>{porc_util*100:.1f}% completado</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
