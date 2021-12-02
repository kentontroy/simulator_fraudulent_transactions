import datetime
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import warnings
warnings.simplefilter("ignore")

st.set_page_config(layout="wide")

st.write(
"""
## San Francisco Bay Area ATM Transactions
""")

@st.cache(persist=True, suppress_st_warning=True)
def load(sql: str):
  """ Load data from Hbase """
  pass
  #return as_pandas(cursor)

