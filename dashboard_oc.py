import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="Órdenes de Compra", layout="wide")

st.title("📦 Tablero de Órdenes de Compra")

# Cargar datos desde Excel o Google Sheets
@st.cache_data
def cargar_datos(ruta_excel):
    df = pd.read_excel(ruta_excel)
    df['Fecha de vencimiento'] = pd.to_datetime(df['Fecha de vencimiento'])
    return df

# Subí tu archivo o conectá con GSheets más adelante
archivo = st.file_uploader("📤 Subí archivo Excel con órdenes", type=["xlsx"])

if archivo:
    df = cargar_datos(archivo)

    # Clasificar estado
    hoy = pd.to_datetime(datetime.today().date())

    def clasificar_estado(fecha_venc):
        if fecha_venc < hoy:
            return 'Vencida'
        elif fecha_venc <= hoy + timedelta(days=3):
            return 'Por vencer'
        else:
            return 'Vigente'

    df['Estado'] = df['Fecha de vencimiento'].apply(clasificar_estado)

    # Mostrar gráfico
    resumen = df['Estado'].value_counts().reset_index()
    resumen.columns = ['Estado', 'Cantidad']

    fig = px.bar(resumen, x='Estado', y='Cantidad', color='Estado',
                 title='Estado de órdenes de compra', text='Cantidad')
    st.plotly_chart(fig, use_container_width=True)

    # Mostrar tabla completa
    st.subheader("📋 Detalle de órdenes")
    st.dataframe(df.sort_values(by='Fecha de vencimiento'), use_container_width=True)

else:
    st.info("Esperando que subas un archivo Excel con tus órdenes de compra.")
