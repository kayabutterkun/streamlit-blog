import tabula
import json
import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_raw():
    dfs = tabula.read_pdf("bidding-wars/tender-bids-from-mar-2012-to-jul-2023.pdf",  pages='all', stream=True)
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
    eateries['Month'] = pd.to_datetime(eateries['Month'], format = '%b-%Y')
    eateries['Year'] = eateries['Month'].dt.year

    f = open('bidding-wars/location.json')
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

@st.cache_data
def load_eateries():
    raw = load_raw()
    eateries = clean(raw)
    return eateries
