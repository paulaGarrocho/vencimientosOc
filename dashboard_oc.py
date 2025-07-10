import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Órdenes de Compra", layout="wide")
st.title("📦 Tablero de Órdenes desde Google Sheets")

# 🧠 ID de tu hoja y nombre de la pestaña
GSHEET_ID = '1UZBNDjvAEcK6DhSvU2a83D5RKrrNCHXU'  # <-- cambiá esto por tu ID real
HOJA = 'vencimientos'

# 🔗 URL directa para leer como CSV
url = f"https://docs.google.com/spreadsheets/d/{GSHEET_ID}/gviz/tq?tqx=out:csv&sheet={HOJA}"

@st.cache_data
def cargar_datos_desde_gsheet(url):
    df = pd.read_csv(url)
    df['Fecha de vencimiento'] = pd.to_datetime(df['Fecha de vencimiento'], errors='coerce')
    return df

try:
    df = cargar_datos_desde_gsheet(url)

    # Clasificar estado
    hoy = pd.to_datetime(datetime.today().date())

    def clasificar_estado(fecha_venc):
        if pd.isna(fecha_venc):
            return 'Sin fecha'
        if fecha_venc < hoy:
            return 'Vencida'
        elif fecha_venc <= hoy + timedelta(days=3):
            return 'Por vencer'
        else:
            return 'Vigente'

    df['Estado'] = df['Fecha de vencimiento'].apply(clasificar_estado)

    # Contar
    cantidad_vigente = df[df['Estado'] == 'Vigente'].shape[0]
    cantidad_por_vencer = df[df['Estado'] == 'Por vencer'].shape[0]
    cantidad_vencida = df[df['Estado'] == 'Vencida'].shape[0]

    # Estilo tarjetas
    st.markdown("""
        <style>
        .card-container { display: flex; justify-content: space-between; gap: 1rem; margin-bottom: 2rem; }
        .card {
            flex: 1;
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            text-align: center;
            font-size: 1.3rem;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
        }
        .vigente { background-color: #2ecc71; }
        .por-vencer { background-color: #f39c12; }
        .vencida { background-color: #e74c3c; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card-container">
        <div class="card vigente">🟢 Vigentes<br>{cantidad_vigente}</div>
        <div class="card por-vencer">🟠 Por vencer<br>{cantidad_por_vencer}</div>
        <div class="card vencida">🔴 Vencidas<br>{cantidad_vencida}</div>
    </div>
    """, unsafe_allow_html=True)

    # Filtro
    estado_seleccionado = st.selectbox("🔍 Filtrar por estado", ["Todos", "Vigente", "Por vencer", "Vencida"])
    df_filtrado = df if estado_seleccionado == "Todos" else df[df['Estado'] == estado_seleccionado]

    # Tabla
    st.subheader("📋 Detalle de órdenes")
    st.dataframe(df_filtrado.sort_values(by='Fecha de vencimiento'), use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar datos desde Google Sheets: {e}")
