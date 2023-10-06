import tabula
import json
import streamlit as st
import pandas as pd
import plotly.express as px
from data import load_eateries

def mapPlot(eateries):
    summary = eateries.groupby(['GoogleName', 'Address', 'Lat', 'Long'])['Bid'].agg(['min','max','mean','median','count']).reset_index()
    fig = px.scatter_mapbox(summary, lat="Lat", lon="Long", hover_name="GoogleName", hover_data={'median':True, 'count':True, "min": True,'max':True, 'Address': True, 'Lat': False, 'Long': False},
                        color="median", color_continuous_scale = px.colors.sequential.Tealgrn, zoom=10)
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(marker={'size': 12})
    fig.update_layout(width = 1200, height = 500)

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


eateries = load_eateries()
mapPlot(eateries)