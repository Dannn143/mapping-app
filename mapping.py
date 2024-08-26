from pathlib import Path
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(layout='wide')
st.header('Map of Locations')

uploaded_file = st.file_uploader("Upload Your Location Data in an Excel File", type=['xlsx'])

if uploaded_file is not None:
    df = pd.read_excel(io=uploaded_file, engine='openpyxl', sheet_name='Sheet1')

    if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
        st.error('The DataFrame must contain Latitude and Longitude columns.')
    else:
        df = df.dropna(subset=['Latitude', 'Longitude'])
    if not df.empty:
        m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=10)
        for i, row in df.iterrows():
            folium.Marker(location=[row['Latitude'], row['Longitude']], popup=row['Building']).add_to(m)
        st.dataframe(df)
        st_folium(m, width=1000, height=700)
    else:
        st.write('No valid locations to display on the map.')
