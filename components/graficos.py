import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def grafico_ingresos_gastos(df):
    resumen = df.groupby("mes")[["ingresos", "gastos"]].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=resumen["mes"], y=resumen["ingresos"],
                             name="Ingresos", line=dict(color="#378ADD", width=2)))
    fig.add_trace(go.Scatter(x=resumen["mes"], y=resumen["gastos"],
                             name="Gastos", line=dict(color="#D85A30", width=2)))
    fig.update_layout(title="Ingresos vs Gastos", height=350,
                      legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)

def grafico_gastos(df):
    categorias_gasto = {
        "Proveedores": df["gastos"].sum() * 0.42,
        "Personal":    df["gastos"].sum() * 0.28,
        "Alquiler":    df["gastos"].sum() * 0.18,
        "Otros":       df["gastos"].sum() * 0.12,
    }
    fig = px.pie(
        values=list(categorias_gasto.values()),
        names=list(categorias_gasto.keys()),
        title="Composición de gastos",
        hole=0.5,
        color_discrete_sequence=["#378ADD", "#1D9E75", "#EF9F27", "#D85A30"]
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)
