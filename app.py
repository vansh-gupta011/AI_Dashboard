import os
import json
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Constants
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("🌍 Population Analysis Dashboard")
st.sidebar.header("Upload CSV File")

uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# User Query Input (Moved outside the if-block)
user_query = st.text_input("💬 Type your query (e.g., 'Show me data for China and India from 2001 to 2015.')")

def parse_query_with_openai(query):
    """Parses the user query using OpenAI's GPT model."""
    chat = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
    system_message = SystemMessage(content="""
        You are an AI assistant that extracts country names and year ranges from user queries related to population data.
        Input: 'Show me data for China and India from 2001 to 2015.'
        Output: {"countries": ["China", "India"], "start_year": 2001, "end_year": 2015}
        
        If no years are specified, return None for start_year and end_year.
    """)
    response = chat([system_message, HumanMessage(content=query)])
    return json.loads(response.content) if response else {}

# Ensure the DataFrame is loaded only if the file exists
if uploaded_file:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    if os.path.exists(file_path):
        st.warning(f"⚠️ File '{uploaded_file.name}' already exists.")
    else:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("✅ File uploaded and stored successfully!")
        
        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://127.0.0.1:8000/upload", files=files)

        if response.status_code == 200:
            st.success("✅ File processed successfully!")
        else:
            st.error("❌ Error processing file.")

    # Load the JSON data safely
    try:
        with open("files.json", "r") as file:
            data = json.load(file)
        df = pd.DataFrame(data)
    except FileNotFoundError:
        st.error("❌ Error: 'files.json' not found. Please upload and process a CSV file first.")
        st.stop()

    # Convert population columns to numeric
    year_columns = [col for col in df.columns if col.isdigit()]
    df[year_columns] = df[year_columns].apply(pd.to_numeric, errors='coerce')
    df["Mean Population"] = df[year_columns].mean(axis=1) / 1e9

# Process user query only if it exists
if user_query:
    parsed_data = parse_query_with_openai(user_query)
    
    if parsed_data:
        countries = parsed_data.get("countries", [])
        start_year = parsed_data.get("start_year")
        end_year = parsed_data.get("end_year")

        if countries:
            country_list = [c.lower() for c in countries]
            df = df[df["Country Name"].str.lower().isin(country_list)]

        if start_year and end_year:
            selected_years = [col for col in year_columns if start_year <= int(col) <= end_year]
            df = df[["Country Name"] + selected_years]

        graph_type = st.selectbox("📊 Choose graph type", ["Bar Chart", "Line Chart", "Pie Chart", "Choropleth Map"])
        
        if graph_type == "Bar Chart":
            fig = px.bar(df.melt(id_vars=["Country Name"], var_name="Year", value_name="Population"),
                         x="Country Name", y="Population", color="Year", title="📊 Population by Country and Year")
        elif graph_type == "Line Chart":
            fig = px.line(df.melt(id_vars=["Country Name"], var_name="Year", value_name="Population"),
                          x="Year", y="Population", color="Country Name", title="📈 Population Trend")
        elif graph_type == "Pie Chart":
            if len(countries) == 1 and selected_years:
                country = countries[0]
                df_country = df[df["Country Name"].str.lower() == country.lower()]
                if not df_country.empty:
                    df_pie = df_country.melt(id_vars=["Country Name"], var_name="Year", value_name="Population")
                    df_pie = df_pie[df_pie["Year"].astype(int).between(start_year, end_year)]
                    fig = px.pie(df_pie, names="Year", values="Population",
                                 title=f"🍕 Population Distribution in {country} ({start_year}-{end_year})")
                else:
                    st.warning("⚠️ No population data available for the selected range.")
                    fig = None
            else:
                st.warning("⚠️ Please select exactly one country and a valid year range.")
                fig = None
        elif graph_type == "Choropleth Map":
            latest_year = selected_years[-1] if selected_years else None
            if latest_year:
                fig = px.choropleth(df, locations="Country Name", locationmode="country names",
                                    color=latest_year, title=f"🗺️ Population Map for {latest_year}",
                                    color_continuous_scale="Viridis",
                                    range_color=(df[latest_year].min(), df[latest_year].max()))
            else:
                st.warning("⚠️ No data available for selected years.")
                fig = None

        if fig:
            st.plotly_chart(fig, use_container_width=True)
