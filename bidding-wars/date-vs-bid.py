import tabula
import json
import streamlit as st
import pandas as pd
import plotly.express as px
from data import load_eateries

def bidScatterPlot(eateries, option):
    if option != 'All Markets':
        eateries = eateries[eateries.GoogleName == option]
    
    fig = px.scatter(
        eateries, x="Month", y="Bid", color="Trade",
        labels = {"Bid": "Bid ($)", "Month": "Month"},
        hover_data = ["GoogleName", "StallArea"],
        title = f"Month vs winning bid for {option}"
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="right",
        x=0.8
    ))

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def medianBidScatterPlot(eateries, option):
    if option != 'All Markets':
        eateries = eateries[eateries.GoogleName == option]
    
    yearly = eateries.groupby([ 'Trade', 'Year'])['Bid'].agg(['min','max','mean','median','count']).reset_index()
    fig = px.line(
        yearly, x="Year", y="median", color="Trade",
        labels = {"Bid": "Bid ($)"},
        hover_data = ["count","mean"],
        title = f"Yearly median bid for {option}"
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

medianBidScatterPlot(eateries, option)