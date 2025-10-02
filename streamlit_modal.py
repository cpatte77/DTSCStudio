import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from supabase import create_client, Client

# --- Load Supabase ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # read-only key

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Streamlit App ---
st.title("Country Data Dashboard")

# Fetch data
try:
    response = supabase.table("countries").select("*").execute()
    data = pd.DataFrame(response.data)
except Exception as e:
    st.error(f"Error fetching data from Supabase: {e}")
    data = pd.DataFrame()

if not data.empty:
    # Show raw data
    if st.checkbox("Show raw data"):
        st.subheader("Raw Data")
        st.dataframe(data)

    # Population chart
    st.subheader("Population by Country")
    data["population"] = pd.to_numeric(data["population"], errors="coerce")
    st.bar_chart(data.set_index("name")["population"])

    # Area chart
    st.subheader("Area (km²) by Country")
    data["area"] = pd.to_numeric(data["area"], errors="coerce")
    st.bar_chart(data.set_index("name")["area"])

    # Capitals table
    st.subheader("Country Capitals")
    st.table(data[["name", "capital"]])

else:
    st.warning("No data available in Supabase.")
