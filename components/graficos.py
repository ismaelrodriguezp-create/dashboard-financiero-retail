import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

AZUL       = "#2563EB"
AZUL_DARK  = "#0F2044"
ROJO       = "#EF4444"
VERDE      = "#10B981"
AMARILLO   = "#F59E0B"
GRIS_BG    = "#F8FAFC"

def _layout_base(fig, height=320):
    fig.update_layout(
        height=height,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#64748B", size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(showgrid=False, color="#94A3B8"),
        yaxis=dict(gridcolor="#F1F5F9", color="#94A3B8"),
    )
    return fig

def grafico_ingresos_gastos(df):
    resumen = df.groupby("mes")[["ingresos", "gastos"]].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=resumen["mes"], y=resumen["ingresos"], name="Ingresos",
        line=dict(color=AZUL, width=3),
        fill="tozeroy", fillcolor="rgba(37,99,235,0.07)",
        mode="lines+markers", marker=dict(size=6, color=AZUL)
    ))
    fig.add_trace(go.Scatter(
        x=resumen["mes"], y=resumen["gastos"], name="Gastos",
        line=dict(color=ROJO, width=2, dash="dot"),
        mode="lines+markers", marker=dict(size=5, color=ROJO)
    ))
    fig = _layout_base(fig)
    fig.update_layout(legend=dict(orientation="h", y=-0.3, x=0))
    st.plotly_chart(fig, use_container_width=True)

def grafico_gastos(df):
    valores = {
        "Proveedores": df["gastos"].sum() * 0.42,
        "Personal":    df["gastos"].sum() * 0.28,
        "Alquiler":    df["gastos"].sum() * 0.18,
        "Otros":       df["gastos"].sum() * 0.12,
    }
    fig = px.pie(
        values=list(valores.values()),
        names=list(valores.keys()),
        hole=0.6,
        color_discrete_sequence=[AZUL, VERDE, AMARILLO, ROJO]
    )
    fig.update_traces(textposition="outside", textinfo="percent+label",
                      marker=dict(line=dict(color="white", width=2)))
    fig.update_layout(
        height=320, paper_bgcolor="white", showlegend=False,
        margin=dict(l=10, r=10, t=20, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

def grafico_barras_horizontal(df):
    if "categoria" not in df.columns:
        return
    resumen = df.groupby("categoria")["ingresos"].sum().reset_index()
    resumen = resumen.sort_values("ingresos", ascending=True)
    colores = [AZUL if i == len(resumen)-1 else "#93C5FD" for i in range(len(resumen))]
    fig = go.Figure(go.Bar(
        x=resumen["ingresos"],
        y=resumen["categoria"],
        orientation="h",
        marker=dict(color=colores, line=dict(width=0)),
        text=resumen["ingresos"].apply(lambda x: f"S/ {x:,.0f}"),
        textposition="outside",
        textfont=dict(size=12, color="#0F2044")
    ))
    fig = _layout_base(fig, height=280)
    fig.update_layout(
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", showticklabels=False),
        yaxis=dict(showgrid=False),
        bargap=0.35
    )
    st.plotly_chart(fig, use_container_width=True)
