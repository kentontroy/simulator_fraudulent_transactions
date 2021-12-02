import datetime
import json
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import warnings
warnings.simplefilter("ignore")

x = "pk.eyJ1Ijoia2VudG9udHJveSIsImEiOiJja3NnYnRzYTAxaXRzMm9udm5rcTVneXFpIn0.CBsFJ2v1T9BQsfnd0tXOhg:"

st.set_page_config(layout="wide")

st.write(
"""
## High Frequency ATM Transactions in San Francisco Bay Area
""")

st.sidebar.image("/Users/kdavis/Documents/Demos/COD/src/demo-logo.png")
bank = st.sidebar.text_input("Filter by Bank", "")
st.sidebar.image("/Users/kdavis/Documents/Demos/COD/src/demo-partner-pic.png")

@st.cache(persist=True, suppress_st_warning=True)
def load(filter: str) -> pd.DataFrame :
  """ Load data from Hbase """
  
  dfTime = []
  dfAtm = []
  dfLat = [] 
  dfLon = []
  dfAmount = []
  dfAccountId = []
  dfTransId = []

  with open("/Users/kdavis/Documents/Demos/COD/src/demo.output", "r") as f: 
    records = f.readlines()
    for r in records:
      j = json.loads(r)  
      if len(filter.strip()) > 0 and j["atm"].upper() != filter.upper():
        continue
      dfTime.append(j["timestamp"])
      dfAtm.append(j["atm"])
      dfLat.append(float(j["location"]["lat"]))
      dfLon.append(float(j["location"]["lon"]))
      dfAmount.append("${:,.2f}".format(j["amount"]))
      dfAccountId.append(j["account_id"])
      dfTransId.append(j["transaction_id"])
     
  dfTuples = list(zip(dfTime, dfAtm, dfLat, dfLon, dfAmount, dfAccountId, dfTransId))
  df = pd.DataFrame(
    dfTuples,
    columns = ["Timestamp", "Atm", "Lat", "Lon", "Amount", "Account ID", "Transaction ID"]
  )

  return df

df = load(bank)
dfCopy = df.copy(deep=True)

# Display the Geo-encoded layer
hexagons = pdk.Layer(
  "HexagonLayer",
  dfCopy,
  get_position=["Lon", "Lat"], 
  auto_highlight=True,
  elevation_scale=50,
  pickable=True,
  elevation_range=[0, 100],
  extruded=True,
  coverage=0.25
)

viewState = pdk.ViewState(
  longitude=-122.0778, latitude=37.3949, zoom=11, min_zoom=6, max_zoom=20, 
  pitch=40.5, bearing=-27.36
)

apiKeys={}
apiKeys["mapbox"]=x

deck = (pdk.Deck(initial_view_state=viewState, layers=[hexagons], 
                 api_keys=apiKeys,
                 map_provider="mapbox", 
                 map_style="mapbox://styles/mapbox/satellite-streets-v11"))

deckchart = st.pydeck_chart(deck)

st.write(dfCopy)
