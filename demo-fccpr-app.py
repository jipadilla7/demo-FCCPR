import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# Configurar la página
st.set_page_config(page_title="Dashboard Caballos Criollos", layout="wide")
st.title("🐎 Dashboard de Caballos Criollos Colombianos de Paso")
st.markdown("### Fundación de Criadores de Caballos de Paso de Puerto Rico")

# Listado de nombres de caballos
nombres_caballos = [
    "Relámpago", "Tormenta", "Lucero", "Centella", "Huracán", "Destello", "Sombra", "Brisa", "Fuego",
    "Rayo", "Viento", "Sol", "Luna", "Estrella", "Corcel", "Trueno", "Águila", "Pegaso", "Olimpo", "Titan",
    "Poseidón", "Encantadora", "Bireina", "Bohemia", "Mágica", "Resorte", "Dulce Sueño", "Duende", "Natán"
]

# Listado de ciudades de Puerto Rico con exposiciones de caballos
ciudades_puerto_rico = [
    "San Juan", "Ponce", "Bayamón", "Carolina", "Arecibo", "Mayagüez", "Caguas", "Guaynabo", "Humacao", "Fajardo"
]

# Modalidades de competencia
modalidades = ["P1 Trote y Galope", "P2 Trocha y Galope", "P3 Trocha", "P4 Paso Fino"]

# Rankings en feria y sus puntajes asociados
ranking_puntaje = {"GC": 20, "GCR": 16, "1": 10, "2": 8, "3": 6, "4": 4, "5": 2}

# Generar fechas en los últimos 5 años
def generar_fecha():
    hoy = datetime.today()
    fecha_random = hoy - timedelta(days=random.randint(0, 5 * 365))
    return fecha_random.strftime("%Y-%m-%d")

# Generar la base de datos aleatoria
def generar_datos(num_registros):
    data = []
    for _ in range(num_registros):
        nombre = random.choice(nombres_caballos)
        sexo = random.choice(["Macho", "Hembra"])
        edad = random.randint(36, 120)
        modalidad = random.choice(modalidades)
        ranking = random.choice(list(ranking_puntaje.keys()))
        fecha = generar_fecha()
        ciudad = random.choice(ciudades_puerto_rico)
        grado = random.choice(["A", "B"])
        puntaje = ranking_puntaje[ranking]

        data.append([nombre, sexo, edad, modalidad, ranking, fecha, ciudad, grado, puntaje])
    
    return pd.DataFrame(data, columns=["Nombre", "Sexo", "Edad (meses)", "Modalidad", "Ranking", "Fecha", "Ciudad", "Grado", "Puntaje"])

# Barra de selección de número de registros
num_registros = st.sidebar.slider("Número de registros a generar", min_value=50, max_value=500, value=200)
df = generar_datos(num_registros)

# Mostrar tabla
total_caballos = len(df)
st.markdown(f"### Datos Seleccionados ({total_caballos} registros)")
st.dataframe(df)

# Filtros
modalidad_seleccionada = st.sidebar.multiselect("Seleccionar modalidad", modalidades, default=modalidades)
edad_min, edad_max = st.sidebar.slider("Rango de edad (meses)", 36, 120, (36, 120))
sexo_seleccionado = st.sidebar.multiselect("Seleccionar sexo", ["Macho", "Hembra"], default=["Macho", "Hembra"])
ciudad_seleccionada = st.sidebar.multiselect("Seleccionar ciudad", ciudades_puerto_rico, default=ciudades_puerto_rico)
fecha_inicio, fecha_fin = st.sidebar.date_input("Seleccionar rango de fechas", [datetime.today() - timedelta(days=5*365), datetime.today()])
puntaje_min, puntaje_max = st.sidebar.slider("Filtrar por puntaje", 2, 20, (2, 20))

# Aplicar filtros
df["Fecha"] = pd.to_datetime(df["Fecha"])
df_filtrado = df[(df["Modalidad"].isin(modalidad_seleccionada)) &
                 (df["Sexo"].isin(sexo_seleccionado)) &
                 (df["Edad (meses)"].between(edad_min, edad_max)) &
                 (df["Ciudad"].isin(ciudad_seleccionada)) &
                 (df["Fecha"].between(pd.Timestamp(fecha_inicio), pd.Timestamp(fecha_fin))) &
                 (df["Puntaje"].between(puntaje_min, puntaje_max))]

# Opción de visualización de gráficos
tipo_grafico = st.selectbox("Seleccionar tipo de gráfico", ["Barras", "Torta", "Histograma"])

if not df_filtrado.empty:
    if tipo_grafico == "Barras":
        fig = px.bar(df_filtrado, x="Modalidad", y="Puntaje", text_auto=True)
    elif tipo_grafico == "Torta":
        fig = px.pie(df_filtrado, names="Ciudad")
    elif tipo_grafico == "Histograma":
        fig = px.histogram(df_filtrado, x="Edad (meses)")

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No hay datos disponibles para los filtros seleccionados.")





