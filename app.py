import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

st.set_page_config(layout='wide')
st.title("Decreto de reducción de gasto - 2024")

df = pd.read_csv("clean_data.csv")

df['TOTAL'] = (df['TOTAL'] / 1_000_000).round(2)

sectores = df['Sector'].unique().tolist()

# Barras con tipo de gasto

t1 = df.groupby('Tipo de gasto')['TOTAL'].sum().sort_values(ascending=False).reset_index()

# Barras con sectores

t2 = df.groupby('Sector')['TOTAL'].sum().sort_values(ascending=False).head(10).reset_index()

t3 = df.groupby('Entidad')['TOTAL'].sum().sort_values(ascending=False).head(10).reset_index()

t4 = df[df['Tipo de gasto'] == 'Funcionamiento'].groupby('Cuenta')['TOTAL'].sum().sort_values(ascending=False).reset_index()

fig = px.bar(t1, x='Tipo de gasto', y='TOTAL', title='Tipo de gasto <br><sup>Cifras en miles de millones de pesos</sup>')

fig.update_layout(yaxis_tickformat='.0f')

st.plotly_chart(fig)



fig = px.bar(t2, x='Sector', y='TOTAL', title='Top 10 - Sectores <br><sup>Cifras en miles de millones de pesos</sup>')
             
fig.update_layout(yaxis_tickformat='.0f')

st.plotly_chart(fig)

fig = px.bar(t3, x='Entidad', y='TOTAL', title='Top 10 - Sectores <br><sup>Cifras en miles de millones de pesos</sup>')
fig.update_layout(yaxis_tickformat='.0f')

st.plotly_chart(fig)

fig = px.bar(t4, x='Cuenta', y='TOTAL', title='Cuentas de funcionamiento <br><sup>Cifras en miles de millones de pesos</sup>')
fig.update_layout(yaxis_tickformat='.0f')
st.plotly_chart(fig)


st.header("Descarga de datos")
        
binary_output = BytesIO()
df.to_excel(binary_output, index=False)
st.download_button(label = 'Descargar excel',
                    data = binary_output.getvalue(),
                    file_name = 'datos.xlsx')