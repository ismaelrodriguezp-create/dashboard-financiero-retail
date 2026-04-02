import streamlit as st

def tabla_categorias(df):
    if "categoria" not in df.columns:
        st.warning("El archivo no tiene columna 'categoria'")
        return

    resumen = df.groupby("categoria").agg(
        Ingresos=("ingresos","sum"), Costo=("gastos","sum")
    ).reset_index()

    resumen["Margen"] = ((resumen["Ingresos"] - resumen["Costo"]) / resumen["Ingresos"] * 100).round(1)

    def estado(m):
        if m >= 35:   return "🟢 Alto"
        elif m >= 20: return "🟡 Regular"
        else:         return "🔴 Bajo"

    resumen["Estado"]   = resumen["Margen"].apply(estado)
    resumen["Ingresos"] = resumen["Ingresos"].apply(lambda x: f"S/ {x:,.0f}")
    resumen["Costo"]    = resumen["Costo"].apply(lambda x: f"S/ {x:,.0f}")
    resumen["Margen"]   = resumen["Margen"].apply(lambda x: f"{x}%")
    resumen.columns     = ["Categoría","Ingresos","Costo","Margen","Estado"]
    st.dataframe(resumen, use_container_width=True, hide_index=True)

def mostrar_recomendaciones(df):
    ingresos = df["ingresos"].sum()
    gastos   = df["gastos"].sum()
    margen   = ((ingresos - gastos) / ingresos * 100) if ingresos > 0 else 0

    recomendaciones = []

    if margen < 25:
        recomendaciones.append(("🔴 Margen crítico", f"Tu margen es {margen:.1f}%. Revisa los gastos de proveedores y considera subir precios en categorías de bajo margen.", "danger"))
    elif margen < 35:
        recomendaciones.append(("🟡 Margen mejorable", f"Tu margen es {margen:.1f}%. Estás bien pero puedes optimizar gastos operativos para llegar al 35%.", "warning"))
    else:
        recomendaciones.append(("🟢 Margen saludable", f"Tu margen es {margen:.1f}%. Excelente gestión financiera. Mantén el control de gastos.", "success"))

    ratio_gastos = (gastos / ingresos * 100) if ingresos > 0 else 0
    if ratio_gastos > 75:
        recomendaciones.append(("⚠️ Gastos elevados", f"Tus gastos representan el {ratio_gastos:.1f}% de tus ingresos. Lo ideal es estar por debajo del 70%.", "warning"))

    if "categoria" in df.columns:
        por_cat = df.groupby("categoria").agg(ing=("ingresos","sum"), gas=("gastos","sum"))
        por_cat["margen"] = ((por_cat["ing"] - por_cat["gas"]) / por_cat["ing"] * 100)
        peor = por_cat["margen"].idxmin()
        peor_margen = por_cat.loc[peor, "margen"]
        if peor_margen < 20:
            recomendaciones.append(("📦 Categoría problemática", f"La categoría '{peor}' tiene solo {peor_margen:.1f}% de margen. Evalúa si es rentable mantenerla.", "danger"))

    colores = {"danger": "#FEF2F2", "warning": "#FFFBEB", "success": "#F0FDF4"}
    bordes  = {"danger": "#FECACA", "warning": "#FDE68A", "success": "#BBF7D0"}
    textos  = {"danger": "#991B1B", "warning": "#92400E", "success": "#166534"}

    for titulo, mensaje, tipo in recomendaciones:
        st.markdown(f"""
        <div style="background:{colores[tipo]}; border:1px solid {bordes[tipo]};
                    border-left:4px solid {textos[tipo]}; border-radius:10px;
                    padding:14px 18px; margin-bottom:10px;">
            <p style="margin:0 0 4px; font-weight:600; color:{textos[tipo]}; font-size:13px;">{titulo}</p>
            <p style="margin:0; color:{textos[tipo]}; font-size:12px; opacity:0.85;">{mensaje}</p>
        </div>
        """, unsafe_allow_html=True)
