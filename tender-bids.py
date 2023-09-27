import tabula
import json
import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_raw():
    dfs = tabula.read_pdf("tender-bids-from-mar-2012-to-jul-2023.pdf",  pages='all', stream=True)
    for i in range(0, len(dfs)):
        if (dfs[i].shape[1] == 7):
            dfs[i].dropna(axis = 1, thresh = 10, inplace = True)
        if ( (dfs[i].shape[1] > 7) or (dfs[i].shape[1] < 6) ):
            raise Exception(f"Df {i} has {dfs[i].shape[1]} columns. Expected 6 only")
        dfs[i].columns = ["HawkerCentre", "Stall","StallArea", "Trade","Bid","Month"]

    df = pd.concat(dfs)
    df = df.dropna()

    return df

@st.cache_data
def clean(df):
    eateries = df[(df.Trade.isin(['COOKED FOOD', 'HALAL COOKED FOOD', 'INDIAN CUISINE','DRINKS']))].copy()
    eateries['Bid'] = pd.to_numeric( eateries.Bid.str.replace('[^0-9.]','', regex = True) )
    eateries['StallArea'] = pd.to_numeric(eateries.StallArea)

    f = open('location.json')
    manualEateriesDb = json.load(f)
    f.close()

    address = {}
    name = {}
    lat = {}
    longt = {}

    for key, value in manualEateriesDb.items():
        nameIndex = 0
        latIndex = 1
        longIndex = 2

        adres = key
        if len(value) == 4:
            adres = value[0].upper()
            nameIndex += 1
            latIndex += 1
            longIndex += 1

        address[key] = adres
        name[adres] = value[nameIndex].upper()
        lat[adres] = value[latIndex]
        longt[adres] = value[longIndex]

    eateries['Address'] = eateries['HawkerCentre'].map(address)
    eateries['GoogleName'] = eateries['Address'].map(name)
    eateries['Lat'] = eateries['Address'].map(lat)
    eateries['Long'] = eateries['Address'].map(longt)

    return eateries

def stallAreaPlot(eateries, option):
    if option != 'All':
        eateries = eateries[eateries.GoogleName == option]
    
    fig = px.scatter(
        eateries, x="StallArea", y="Bid", color="Trade",
        labels = {"Bid": "Bid ($)", "StallArea": "Stall Area (sqm)"},
        hover_data = ["GoogleName", "Month"],
        title = "Stall area vs winning bid"
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="right",
        x=0.8
    ))

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

raw = load_raw()
eateries = clean(raw)

markets = ['All']
markets.extend(eateries['GoogleName'].unique())
option = st.selectbox(
    'Please select market',
    markets
)

stallAreaPlot(eateries, option)