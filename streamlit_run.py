import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import plotly.express as px
from supabase import create_client, Client

# --- Supabase helper ---
def get_client() -> Client:
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in .env")
    return create_client(url, key)

# --- Streamlit App ---
def main():
    st.title("Country Data Dashboard")

    try:
        supabase = get_client()
    except RuntimeError as e:
        st.error(str(e))
        return

    # Fetch data from Supabase
    try:
        response = supabase.table("countries").select("*").execute()
        data = pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Error fetching data from Supabase: {e}")
        return

    if data.empty:
        st.warning("No data returned from Supabase.")
        return

    # Show raw data
    if st.checkbox("Show raw data"):
        st.subheader("Raw Data")
        st.dataframe(data)

    # 1️⃣ Population chart
    if "Country" in data.columns and "Population" in data.columns:
        st.subheader("Population by Country")
        data["Population"] = pd.to_numeric(data["Population"], errors="coerce")
        fig_pop = px.bar(data, x="Country", y="Population", title="Population by Country")
        st.plotly_chart(fig_pop, use_container_width=True)

    # 2️⃣ Area chart
    if "Country" in data.columns and "Area_km2" in data.columns:
        st.subheader("Area (km²) by Country")
        data["Area_km2"] = pd.to_numeric(data["Area_km2"], errors="coerce")
        fig_area = px.bar(data, x="Country", y="Area_km2", title="Area by Country")
        st.plotly_chart(fig_area, use_container_width=True)

    # 3️⃣ Capitals table
    if "Country" in data.columns and "Capital" in data.columns:
        st.subheader("Country Capitals")
        st.table(data[["Country", "Capital"]])

if __name__ == "__main__":
    main()
