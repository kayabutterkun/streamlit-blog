import tabula
import json
import streamlit as st
import pandas as pd
import plotly.express as px
from data import load_eateries


def stallAreaPlot(eateries, option):
    if option != 'All Markets':
        eateries = eateries[eateries.GoogleName == option]
    
    fig = px.scatter(
        eateries, x="StallArea", y="Bid", color="Trade",
        labels = {"Bid": "Bid ($)", "StallArea": "Stall Area (sqm)"},
        hover_data = ["GoogleName", "Month"],
        title = f"Stall area vs winning bid for {option}"
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="right",
        x=0.8
    ))

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


eateries = load_eateries()

markets = ['All Markets']
markets.extend(eateries['GoogleName'].unique())
option = st.selectbox(
    'Please select market',
    markets
)

stallAreaPlot(eateries, option)