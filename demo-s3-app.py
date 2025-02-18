import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Configurar la página
st.set_page_config(page_title="Dashboard de Desempeño Deportivo", layout="wide")
st.title("⚽ Dashboard de Desempeño Deportivo")
st.markdown("### Análisis de rendimiento de jugadores en el fútbol colombiano")

# Botón para resetear la aplicación
if st.sidebar.button("🔄 Resetear Página"):
    st.experimental_set_query_params()

# Listado de nombres de jugadores colombianos famosos
jugadores_masculinos = ["James Rodríguez", "Falcao", "Juan Cuadrado", "Carlos Valderrama", "Freddy Rincón", "Rafael Santos Borré", "David Ospina", "Teófilo Gutiérrez", "Luis Díaz", "Yerry Mina"]
jugadores_femeninos = ["Leicy Santos", "Catalina Usme", "Linda Caicedo", "Yoreli Rincón", "Daniela Montoya", "Isabella Echeverri", "Natalia Gaitán", "Tatiana Ariza"]

# Listado de equipos de fútbol de Colombia
equipos_colombia = ["Atlético Nacional", "Millonarios", "América de Cali", "Deportivo Cali", "Junior", "Independiente Medellín", "Santa Fe", "Once Caldas", "Tolima", "Pereira"]

# Tipos de deporte (modalidades)
tipos_deporte = ["Fútbol 11", "Fútbol Sala", "Fútbol Playa"]

# Generar fechas en los últimos 5 años
def generar_fecha():
    hoy = datetime.today()
    fecha_random = hoy - timedelta(days=random.randint(0, 5 * 365))
    return fecha_random.strftime("%Y-%m-%d")

# Generar la base de datos aleatoria
def generar_datos(num_registros):
    data = []
    for _ in range(num_registros):
        categoria = random.choice(["Masculino", "Femenino"])
        nombre = random.choice(jugadores_masculinos if categoria == "Masculino" else jugadores_femeninos)
        edad = random.randint(18, 38)
        tipo_deporte = random.choice(tipos_deporte)
        fecha = generar_fecha()
        equipo = random.choice(equipos_colombia)
        grado = random.choice(["A", "B"])
        desempeno = random.randint(50, 100)  # Porcentaje de desempeño entre 50 y 100

        data.append([nombre, categoria, edad, tipo_deporte, fecha, equipo, grado, desempeno])
    
    return pd.DataFrame(data, columns=["Jugador", "Categoría", "Edad", "Tipo de Deporte", "Fecha", "Equipo", "Grado", "Desempeño (%)"])

# Barra de selección de número de registros
num_registros = st.sidebar.slider("Número de registros a generar", min_value=50, max_value=500, value=200)
df = generar_datos(num_registros)

# Panel de Filtros
st.sidebar.header("Filtros Avanzados")
tipo_seleccionado = st.sidebar.multiselect("Seleccionar Tipo de Deporte", tipos_deporte, default=tipos_deporte)
edad_min, edad_max = st.sidebar.slider("Rango de edad", 18, 38, (18, 38))
categoria_seleccionada = st.sidebar.multiselect("Seleccionar Categoría", ["Masculino", "Femenino"], default=["Masculino", "Femenino"])
equipo_seleccionado = st.sidebar.multiselect("Seleccionar Equipo", equipos_colombia, default=equipos_colombia)
fecha_inicio, fecha_fin = st.sidebar.date_input("Seleccionar rango de fechas", [datetime.today() - timedelta(days=5*365), datetime.today()])
desempeno_min, desempeno_max = st.sidebar.slider("Filtrar por desempeño (%)", 50, 100, (50, 100))

# Aplicar filtros
df["Fecha"] = pd.to_datetime(df["Fecha"])
df_filtrado = df[(df["Tipo de Deporte"].isin(tipo_seleccionado)) &
                 (df["Categoría"].isin(categoria_seleccionada)) &
                 (df["Edad"].between(edad_min, edad_max)) &
                 (df["Equipo"].isin(equipo_seleccionado)) &
                 (df["Fecha"].between(pd.Timestamp(fecha_inicio), pd.Timestamp(fecha_fin))) &
                 (df["Desempeño (%)"].between(desempeno_min, desempeno_max))]

# Mostrar tabla
total_jugadores = len(df_filtrado)
st.markdown(f"### Datos Filtrados ({total_jugadores} registros)")
st.dataframe(df_filtrado)

# Estadísticas clave
st.subheader("🌟 Jugador con Mayor Desempeño")
if not df_filtrado.empty:
    mejor_jugador = df_filtrado.loc[df_filtrado["Desempeño (%)"].idxmax()]
    st.write(mejor_jugador)

st.subheader("⚽ Jugador con Más Participaciones")
if not df_filtrado.empty:
    mas_participaciones = df_filtrado["Jugador"].value_counts().idxmax()
    st.write(f"Nombre: {mas_participaciones}")

st.subheader("🏆 Tipo de Deporte más Jugado")
if not df_filtrado.empty:
    deporte_mas_jugado = df_filtrado["Tipo de Deporte"].value_counts().idxmax()
    st.write(f"Tipo de Deporte: {deporte_mas_jugado}")

# Mostrar gráficos
st.subheader("📊 Distribuciones de Datos")
if not df_filtrado.empty:
    fig_deporte = px.bar(df_filtrado, x="Tipo de Deporte", title="Distribución por Tipo de Deporte")
    st.plotly_chart(fig_deporte)
    
    fig_categoria = px.bar(df_filtrado, x="Categoría", title="Distribución por Categoría")
    st.plotly_chart(fig_categoria)
    
    fig_equipo = px.bar(df_filtrado, x="Equipo", title="Distribución por Equipo")
    st.plotly_chart(fig_equipo)

    # Gráfico de radar estilo PlayStation
    st.subheader("🎮 Gráfico de Habilidades de Jugadores")
    jugador_random = df_filtrado.sample(1).iloc[0]
    categorias = ["Velocidad", "Resistencia", "Defensa", "Ataque", "Pases", "Tiros"]
    valores = [random.randint(50, 100) for _ in categorias]
    valores.append(valores[0])  # Cierre del gráfico

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=valores, theta=categorias + [categorias[0]], fill='toself'))
    fig_radar.update_layout(title=f"Desempeño de {jugador_random['Jugador']}", polar=dict(radialaxis=dict(visible=True)))
    st.plotly_chart(fig_radar)
else:
    st.warning("No hay datos disponibles para generar los gráficos.")
