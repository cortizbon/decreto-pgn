import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO

DIC_COLORES = {'verde':["#009966"],
               'ro_am_na':["#FFE9C5", "#F7B261","#D8841C", "#dd722a","#C24C31", "#BC3B26"],
               'az_verd': ["#CBECEF", "#81D3CD", "#0FB7B3", "#009999"],
               'ax_viol': ["#D9D9ED", "#2F399B", "#1A1F63", "#262947"],
               'ofiscal': ["#F9F9F9", "#2635bf"]}

st.set_page_config(layout='wide')
st.title("Decreto de reducción de gasto - 2024")

df = pd.read_csv("clean_data.csv")

df['TOTAL_alt'] = (df['TOTAL'] / 1_000_000).round(2)

sectores = df['Sector'].unique().tolist()

tab1, tab2, tab3, tab4 = st.tabs(['General',
                                'Transferencias corrientes',
                                'Prestaciones sociales',
                                'Descarga de datos'])

# Barras con tipo de gasto

with tab1:

    t1 = df.groupby('Tipo de gasto')['TOTAL_alt'].sum().sort_values(ascending=False).reset_index()

    # Barras con sectores

    t2 = df.groupby('Sector')['TOTAL_alt'].sum().sort_values(ascending=False).head(10).reset_index()

    t3 = df.groupby('Entidad')['TOTAL_alt'].sum().sort_values(ascending=False).head(10).reset_index()

    t4 = df[df['Tipo de gasto'] == 'Funcionamiento'].groupby('Cuenta')['TOTAL_alt'].sum().sort_values(ascending=False).reset_index()

    fig = make_subplots(rows=2, cols=2, subplot_titles=('Reducción por tipo de gasto<br><sup>Cifras en miles de millones de pesos</sup>',
                                                        'Reducción por sector<br><sup>Cifras en miles de millones de pesos</sup>',
                                                        'Reducción por entidad<br><sup>Cifras en miles de millones de pesos</sup>',
                                                        'Reducción en cuentas de funcionamiento<br><sup>Cifras en miles de millones de pesos</sup>'))

    # Add barplots to each subplot
    fig.add_trace(go.Bar(x=t1['Tipo de gasto'], y=t1['TOTAL_alt'],marker=dict(color="#81D3CD")), row=1, col=1)
    fig.add_trace(go.Bar(x=t2['Sector'], y=t2['TOTAL_alt'],marker=dict(color="#81D3CD")), row=1, col=2)
    fig.add_trace(go.Bar(x=t3['Entidad'], y=t3['TOTAL_alt'],marker=dict(color="#81D3CD")), row=2, col=1)
    fig.add_trace(go.Bar(x=t4['Cuenta'], y=t4['TOTAL_alt'],marker=dict(color="#81D3CD")), row=2, col=2)

    fig.update_xaxes(showticklabels=False, row=1, col=1)
    fig.update_xaxes(showticklabels=False, row=1, col=2)
    fig.update_xaxes(showticklabels=False, row=2, col=1)
    fig.update_xaxes(showticklabels=False, row=2, col=2)

    fig.update_yaxes(tickformat='.0f', row=1, col=1)
    fig.update_yaxes(tickformat='.0f', row=1, col=2)
    fig.update_yaxes(tickformat='.0f', row=2, col=1)
    fig.update_yaxes(tickformat='.0f', row=2, col=2)

    fig.update_layout(
    width=1400,  # Set the width of the figure
    height=1000,  # Set the height of the figure
    title_text="Reducción del gasto - 2024",
    title_x=0.5,
    showlegend=False)

    st.plotly_chart(fig)

with tab2:
    trans = df[df['Cuenta'] == 'Transferencias corrientes']
    sectores = trans['Sector'].unique().tolist()
    sector = st.selectbox("Seleccione un sector", sectores)
    entidades = trans[trans['Sector'] == sector]['Entidad'].unique().tolist()
    entidad = st.selectbox("Seleccione una entidad", entidades)
    filtro = trans[(trans['Sector'] == sector) & (trans['Entidad'] == entidad)]
    piv = filtro.groupby('Rubro')['TOTAL_alt'].sum().sort_values(ascending=False).reset_index()

    fig = px.bar(piv, x='Rubro', y='TOTAL_alt', title='Distribución de la reducción en transferencias corrientes<br><sup>Cifras en miles de millones de pesos</sup>')

    fig.update_layout(yaxis_tickformat='.0f',
    xaxis=dict(
        showticklabels=False
    ))

    st.plotly_chart(fig)

with tab3:
    prest = df[df['Subcuenta'] == 'Prestaciones para cubrir riesgos sociales']
    sectores = prest['Sector'].unique().tolist()
    sector = st.selectbox("Seleccione un sector", sectores)
    entidades = prest[prest['Sector'] == sector]['Entidad'].unique().tolist()
    entidad = st.selectbox("Seleccione una entidad", entidades)
    filtro = prest[(prest['Sector'] == sector) & (prest['Entidad'] == entidad)]
    piv = filtro.groupby('Rubro')['TOTAL_alt'].sum().sort_values(ascending=False).reset_index()

    fig = px.bar(piv, x='Rubro', y='TOTAL_alt', title='Distribución de la reducción en transferencias corrientes<br><sup>Cifras en miles de millones de pesos</sup>')

    fig.update_layout(yaxis_tickformat='.0f',
    xaxis=dict(
        showticklabels=False
    ))

    st.plotly_chart(fig)
# with tab4:
    # inversión
#    inv = df[df['Tipo de gasto'] == 'Inversión']
#    entidades = inv['Entidad'].unique().tolist()
#    entidad = st.selectbox("Seleccione una entidad", entidades)
#    filtro2 = inv[inv['Entidad'] == entidad]
#    piv2 = filtro2.groupby("Rubro")['TOTAL_alt'].sum().sort_values(ascending=False).reset_index()
#    fig = px.bar(piv2, x='Rubro', y='TOTAL_alt', title='Distribución de la reducción en inversión<br><sup>Cifras en miles de millones de pesos</sup>')

#    fig.update_layout(yaxis_tickformat='.0f',
#   xaxis=dict(
#       showticklabels=False
#   ))

#   st.plotly_chart(fig)    
with tab4:
    st.header("Descarga de datos")
            
    binary_output = BytesIO()
    df.drop(columns='TOTAL_alt').to_excel(binary_output, index=False)
    st.download_button(label = 'Descargar excel',
                        data = binary_output.getvalue(),
                        file_name = 'datos.xlsx')