import streamlit as st
import pandas as pd

def tabla_categorias(df):
    if "categoria" not in df.columns:
        st.warning("El archivo no tiene columna 'categoria'")
        return

    resumen = df.groupby("categoria").agg(
        Ingresos=("ingresos", "sum"),
        Costo=("gastos", "sum")
    ).reset_index()

    resumen["Margen %"] = ((resumen["Ingresos"] - resumen["Costo"]) / resumen["Ingresos"] * 100).round(1)
    resumen["Ingresos"] = resumen["Ingresos"].apply(lambda x: f"S/ {x:,.0f}")
    resumen["Costo"] = resumen["Costo"].apply(lambda x: f"S/ {x:,.0f}")
    resumen["Margen %"] = resumen["Margen %"].apply(lambda x: f"{x}%")
    resumen.columns = ["Categoría", "Ingresos", "Costo", "Margen"]

    st.dataframe(resumen, use_container_width=True, hide_index=True)
