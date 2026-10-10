"""
🌎 Dashboard interactivo: métricas sociales, económicas y digitales de Latinoamérica
Ejecutar con:  streamlit run app.py
Requisitos:    pip install streamlit pandas plotly
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ----------------------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA (debe ser la primera instrucción de Streamlit)
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="LatAm Digital Dashboard",
    page_icon="🌎",
    layout="wide",  # usa todo el ancho de la pantalla
)

# Estilo extra muy simple para que las tarjetas de métricas se vean mejor
st.markdown(
    """
    <style>
        div[data-testid="stMetric"] {
            background-color: #F4F6FB;
            border: 1px solid #E1E5F0;
            border-radius: 12px;
            padding: 12px 16px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# 2. CONSTANTES (nombres bonitos para mostrar y colores consistentes)
# ----------------------------------------------------------------------
# Diccionario {nombre que ve el usuario: nombre real de la columna}
METRICAS = {
    "Pagos digitales (%)": "pagos_digitales_pct",
    "Penetración de internet (%)": "penetracion_internet_pct",
    "Velocidad de internet (Mbps)": "velocidad_internet_mbps",
    "Ventas e-commerce (MUSD)": "ventas_ecommerce_musd",
    "Inversión VC (MUSD)": "inversion_vc_musd",
    "Startups fintech (n.º)": "startups_fintech",
    "PIB per cápita (USD)": "pib_per_capita_usd",
    "Desempleo (%)": "tasa_desempleo_pct",
    "Inflación anual (%)": "inflacion_anual_pct",
    "Pobreza (%)": "pobreza_pct",
    "Horas diarias en redes": "horas_diarias_redes",
}

CATEGORIAS = {
    "Red social dominante": "red_social_dominante",
    "Sector líder de VC": "sector_vc_lider",
    "Nivel de ingreso": "nivel_ingreso",
    "Subregión": "subregion",
}

ORDEN_INGRESO = ["Medio-bajo", "Medio-alto", "Alto"]
COLORES_INGRESO = {
    "Medio-bajo": "#EF553B",
    "Medio-alto": "#636EFA",
    "Alto": "#00CC96",
}
PLANTILLA = "plotly_white"


# ----------------------------------------------------------------------
# 3. CARGA DE DATOS
# ----------------------------------------------------------------------
@st.cache_data  # guarda el resultado en memoria para que la app sea rápida
def cargar_datos() -> pd.DataFrame:
    # Busca el CSV en la misma carpeta que app.py
    ruta = Path(__file__).parent / "dataset_latam.csv"
    df = pd.read_csv(ruta, parse_dates=["fecha"])
    df["anio"] = df["fecha"].dt.year
    return df


try:
    df = cargar_datos()
except FileNotFoundError:
    st.error("No encontré `dataset_latam.csv`. Guárdalo en la misma carpeta que `app.py`.")
    st.stop()

# ----------------------------------------------------------------------
# 4. TÍTULO Y SUBTÍTULO
# ----------------------------------------------------------------------
st.title("🌎 LatAm Digital Pulse 🚀")
st.subheader("📊 Economía, redes sociales y pagos digitales en 15 países · 2023-2025 💳📱")
st.divider()

# ----------------------------------------------------------------------
# 5. FILTROS (barra lateral)
# ----------------------------------------------------------------------
st.sidebar.header("🎛️ Filtros")

# --- Dropdowns (selectbox) ---
anio = st.sidebar.selectbox("📅 Año", ["Todos"] + sorted(df["anio"].unique().tolist()))
subregion = st.sidebar.selectbox("🗺️ Subregión", ["Todas"] + sorted(df["subregion"].unique()))
nivel = st.sidebar.selectbox("💰 Nivel de ingreso", ["Todos"] + ORDEN_INGRESO)

st.sidebar.markdown("---")
st.sidebar.subheader("📈 Variables a graficar")
metrica_barras = st.sidebar.selectbox("Gráfico de barras", list(METRICAS.keys()), index=0)
categoria_pie = st.sidebar.selectbox("Gráfico circular (agrupar por)", list(CATEGORIAS.keys()), index=0)
metrica_hist = st.sidebar.selectbox("Histograma", list(METRICAS.keys()), index=1)

st.sidebar.markdown("---")
st.sidebar.subheader("✅ Políticas públicas")

# --- Checkboxes ---
solo_pago_instantaneo = st.sidebar.checkbox("⚡ Solo países con pago instantáneo")
solo_ley_datos = st.sidebar.checkbox("🔒 Solo países con ley de datos personales")

st.sidebar.markdown("---")
mostrar_tabla = st.sidebar.checkbox("👀 Mostrar vista previa de los datos", value=False)

# ----------------------------------------------------------------------
# 6. APLICAR FILTROS
# ----------------------------------------------------------------------
df_filtrado = df.copy()

if anio != "Todos":
    df_filtrado = df_filtrado[df_filtrado["anio"] == anio]
if subregion != "Todas":
    df_filtrado = df_filtrado[df_filtrado["subregion"] == subregion]
if nivel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["nivel_ingreso"] == nivel]
if solo_pago_instantaneo:
    df_filtrado = df_filtrado[df_filtrado["pago_instantaneo"]]
if solo_ley_datos:
    df_filtrado = df_filtrado[df_filtrado["ley_datos_personales"]]

# Si los filtros no dejan ninguna fila, avisamos y detenemos la app
if df_filtrado.empty:
    st.warning("⚠️ No hay datos con esta combinación de filtros. Prueba con otra. 🔄")
    st.stop()

# ----------------------------------------------------------------------
# 7. TARJETAS DE RESUMEN (KPIs)
# ----------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("🏳️ Países", df_filtrado["pais"].nunique())
c2.metric("💳 Pagos digitales (prom.)", f"{df_filtrado['pagos_digitales_pct'].mean():.1f} %")
c3.metric("🌐 Internet (prom.)", f"{df_filtrado['penetracion_internet_pct'].mean():.1f} %")
c4.metric("🛒 E-commerce total", f"{df_filtrado['ventas_ecommerce_musd'].sum():,.0f} MUSD")

# ----------------------------------------------------------------------
# 8. VISTA PREVIA DEL DATAFRAME (se muestra solo si el checkbox está activo)
# ----------------------------------------------------------------------
if mostrar_tabla:
    st.markdown("### 🔍 Vista previa de los datos filtrados")
    st.caption(f"Mostrando 10 de {len(df_filtrado)} filas")
    st.dataframe(df_filtrado.head(10), hide_index=True)

st.markdown("")  # espacio en blanco

# ----------------------------------------------------------------------
# 9. GRÁFICOS
# ----------------------------------------------------------------------
col_izq, col_der = st.columns(2)

# ---------- GRÁFICO 1: BARRAS HORIZONTALES ----------
with col_izq:
    st.markdown(f"### 📊 {metrica_barras} por país")
    columna = METRICAS[metrica_barras]

    # Promedio de la métrica por país (y su nivel de ingreso para colorear)
    datos_barras = (
        df_filtrado.groupby(["pais", "nivel_ingreso"], as_index=False)[columna]
        .mean()
        .sort_values(columna, ascending=True)  # el mayor queda arriba
    )

    fig_barras = px.bar(
        datos_barras,
        x=columna,
        y="pais",
        color="nivel_ingreso",
        orientation="h",
        text_auto=".1f",
        color_discrete_map=COLORES_INGRESO,
        category_orders={"nivel_ingreso": ORDEN_INGRESO},
        labels={columna: metrica_barras, "pais": "", "nivel_ingreso": "Nivel de ingreso"},
        template=PLANTILLA,
    )
    fig_barras.update_layout(
        height=520,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    fig_barras.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig_barras)
    st.caption("Promedio trimestral del periodo filtrado. Pasa el cursor sobre las barras 🖱️")

# ---------- GRÁFICO 2: DONUT ----------
with col_der:
    st.markdown(f"### 🍩 Ventas e-commerce por {categoria_pie.lower()}")
    col_cat = CATEGORIAS[categoria_pie]

    datos_pie = df_filtrado.groupby(col_cat, as_index=False)["ventas_ecommerce_musd"].sum()

    fig_pie = px.pie(
        datos_pie,
        names=col_cat,
        values="ventas_ecommerce_musd",
        hole=0.5,  # hole > 0 lo convierte en donut
        color_discrete_sequence=px.colors.qualitative.Bold,
        labels={"ventas_ecommerce_musd": "Ventas (MUSD)"},
        template=PLANTILLA,
    )
    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(line=dict(color="white", width=2)),
    )
    fig_pie.update_layout(
        height=520,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, x=0),
        annotations=[
            dict(
                text=f"{datos_pie['ventas_ecommerce_musd'].sum():,.0f}<br>MUSD",
                x=0.5,
                y=0.5,
                font_size=20,
                showarrow=False,
            )
        ],
    )
    st.plotly_chart(fig_pie)
    st.caption("Suma de ventas e-commerce acumuladas en el periodo filtrado.")

# ---------- GRÁFICO 3: HISTOGRAMA (ancho completo) ----------
st.markdown(f"### 📈 Distribución de: {metrica_hist}")
columna_hist = METRICAS[metrica_hist]

fig_hist = px.histogram(
    df_filtrado,
    x=columna_hist,
    color="nivel_ingreso",
    nbins=20,
    marginal="box",  # agrega un boxplot arriba para ver outliers
    barmode="overlay",
    opacity=0.75,
    color_discrete_map=COLORES_INGRESO,
    category_orders={"nivel_ingreso": ORDEN_INGRESO},
    hover_data=["pais", "fecha"],
    labels={columna_hist: metrica_hist, "nivel_ingreso": "Nivel de ingreso", "count": "Frecuencia"},
    template=PLANTILLA,
)
fig_hist.update_layout(
    height=480,
    margin=dict(l=10, r=10, t=10, b=10),
    yaxis_title="Frecuencia (país-trimestre)",
    bargap=0.05,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
)
st.plotly_chart(fig_hist)

# ----------------------------------------------------------------------
# 10. PIE DE PÁGINA
# ----------------------------------------------------------------------
st.divider()
st.caption("🧪 Datos simulados con fines educativos · Hecho con Streamlit + Plotly Express 💙")