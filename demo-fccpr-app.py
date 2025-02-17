import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.express as px

# Configurar la página
st.set_page_config(page_title="Dashboard Caballos Criollos", layout="wide")
st.title("\U0001F40E Dashboard de Caballos Criollos Colombianos de Paso")
st.markdown("### Fundación de Criadores de Caballos de Paso de Puerto Rico")

# Botón para resetear la aplicación
if st.sidebar.button("🔄 Resetear Página"):
    st.experimental_set_query_params()

# Listado de nombres de caballos con género asociado
nombres_machos = ["Relámpago", "Tormenta", "Lucero", "Centella", "Huracán", "Destello", "Sombra", "Fuego",
                   "Rayo", "Viento", "Sol", "Corcel", "Trueno", "Águila", "Pegaso", "Olimpo", "Titan",
                   "Poseidón", "Resorte", "Duende", "Natán"]
nombres_hembras = ["Brisa", "Luna", "Estrella", "Encantadora", "Bireina", "Bohemia", "Mágica", "Dulce Sueño"]

# Listado de ciudades de Puerto Rico con exposiciones de caballos
ciudades_puerto_rico = ["San Juan", "Ponce", "Bayamón", "Carolina", "Mayagüez"]

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
        sexo = random.choice(["Macho", "Hembra"])
        nombre = random.choice(nombres_machos if sexo == "Macho" else nombres_hembras)
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

# Panel de Filtros
st.sidebar.header("Filtros Avanzados")
modalidad_seleccionada = st.sidebar.multiselect("Seleccionar modalidad", modalidades, default=modalidades)
edad_min, edad_max = st.sidebar.slider("Rango de edad (meses)", 36, 120, (36, 120))
sexo_seleccionado = st.sidebar.multiselect("Seleccionar sexo", ["Macho", "Hembra"], default=["Macho", "Hembra"])
ciudad_seleccionada = st.sidebar.multiselect("Seleccionar ciudad", ciudades_puerto_rico, default=ciudades_puerto_rico)
fecha_inicio, fecha_fin = st.sidebar.date_input("Seleccionar rango de fechas", [datetime.today() - timedelta(days=5*365), datetime.today()])
puntaje_min, puntaje_max = st.sidebar.slider("Filtrar por puntaje", 2, 20, (2, 20))

tipo_grafico = st.sidebar.selectbox("Seleccionar tipo de gráfico", ["Barras", "Pastel", "Histograma"])

# Aplicar filtros
df["Fecha"] = pd.to_datetime(df["Fecha"])
df_filtrado = df[(df["Modalidad"].isin(modalidad_seleccionada)) &
                 (df["Sexo"].isin(sexo_seleccionado)) &
                 (df["Edad (meses)"].between(edad_min, edad_max)) &
                 (df["Ciudad"].isin(ciudad_seleccionada)) &
                 (df["Fecha"].between(pd.Timestamp(fecha_inicio), pd.Timestamp(fecha_fin))) &
                 (df["Puntaje"].between(puntaje_min, puntaje_max))]

# Mostrar tabla
total_caballos = len(df_filtrado)
st.markdown(f"### Datos Filtrados ({total_caballos} registros)")
st.dataframe(df_filtrado)

# Generación de gráficos
variables_numericas = ["Edad (meses)", "Puntaje"]
variables_categoricas = ["Sexo", "Modalidad", "Ciudad", "Grado"]
variable_seleccionada = st.sidebar.selectbox("Seleccionar variable para graficar", variables_numericas + variables_categoricas)

df_variable = df_filtrado[variable_seleccionada].value_counts().reset_index()
df_variable.columns = [variable_seleccionada, "count"]

if not df_filtrado.empty:
    if tipo_grafico == "Barras":
        fig = px.bar(df_variable, x=variable_seleccionada, y="count", labels={variable_seleccionada: variable_seleccionada, "count": "Cantidad"}, title=f"Distribución de {variable_seleccionada}")
    elif tipo_grafico == "Pastel":
        fig = px.pie(df_variable, names=variable_seleccionada, values="count", title=f"Distribución de {variable_seleccionada}")
    else:
        fig = px.histogram(df_filtrado, x=variable_seleccionada, nbins=20, title=f"Distribución de {variable_seleccionada}")
    st.plotly_chart(fig)
else:
    st.warning("No hay datos disponibles para generar el gráfico.")
