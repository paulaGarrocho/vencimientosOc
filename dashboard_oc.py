import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Órdenes de Compra", layout="wide")
st.title("📦 Tablero de Órdenes de Compra")

# 1. Cargar archivo Excel
@st.cache_data
def cargar_datos(archivo):
    df = pd.read_excel(archivo)
    df['Fecha de vencimiento'] = pd.to_datetime(df['Fecha de vencimiento'])
    return df

archivo = st.file_uploader("📤 Subí archivo Excel con órdenes", type=["xlsx"])

if archivo:
    df = cargar_datos(archivo)

    # 2. Clasificar estado según vencimiento
    hoy = pd.to_datetime(datetime.today().date())

    def clasificar_estado(fecha_venc):
        if fecha_venc < hoy:
            return 'Vencida'
        elif fecha_venc <= hoy + timedelta(days=3):
            return 'Por vencer'
        else:
            return 'Vigente'

    df['Estado'] = df['Fecha de vencimiento'].apply(clasificar_estado)

    # 3. Calcular cantidad por estado
    cantidad_vigente = df[df['Estado'] == 'Vigente'].shape[0]
    cantidad_por_vencer = df[df['Estado'] == 'Por vencer'].shape[0]
    cantidad_vencida = df[df['Estado'] == 'Vencida'].shape[0]

    # 4. Mostrar tarjetas coloridas
    st.markdown("""
        <style>
        .card-container {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 2rem;
        }
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

    # 5. Filtro por estado
    estado_seleccionado = st.selectbox(
        "🔍 Filtrar por estado de órdenes",
        ["Todos", "Vigente", "Por vencer", "Vencida"]
    )

    if estado_seleccionado != "Todos":
        df_filtrado = df[df['Estado'] == estado_seleccionado]
    else:
        df_filtrado = df

    # 6. Mostrar tabla
    st.subheader("📋 Detalle de órdenes")
    st.dataframe(df_filtrado.sort_values(by='Fecha de vencimiento'), use_container_width=True)

else:
    st.info("📄 Por favor, subí un archivo Excel con al menos una columna llamada 'Fecha de vencimiento'.")
