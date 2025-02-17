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
st.markdown(f"### Datos Generados ({total_caballos} registros)")
st.dataframe(df)
