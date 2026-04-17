import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================
# Config
# =========================
DB_PATH = Path(__file__).parent.parent / "data" / "lakehouse.duckdb"

st.set_page_config(
    page_title="Procurement Lakehouse",
    page_icon="🏗️",
    layout="wide"
)

# =========================
# Load Data
# =========================
@st.cache_data
def load_data():
    con = duckdb.connect(str(DB_PATH), read_only=True)
    by_region = con.execute("SELECT * FROM gold_contracts_by_region").df()
    by_project = con.execute("SELECT * FROM gold_project_summary").df()
    silver = con.execute("SELECT * FROM silver_contracts").df()
    con.close()
    return by_region, by_project, silver

by_region, by_project, silver = load_data()

# =========================
# Header
# =========================
st.title("🏗️ Procurement Lakehouse Dashboard")
st.caption("World Bank Documents — powered by DuckDB + dbt")

# =========================
# KPIs
# =========================
col1, col2, col3, col4 = st.columns(4)
col1.metric("📄 Total Documents", len(silver))
col2.metric("🌍 Regions", silver['region'].nunique())
col3.metric("📁 Projects", silver['project_id'].nunique())
col4.metric("📋 Doc Types", silver['document_type'].nunique())

st.divider()

# =========================
# Charts
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Documents by Region")
    region_data = by_region.groupby('region')['total_documents'].sum().reset_index()
    region_data = region_data.sort_values('total_documents', ascending=False).head(10)
    fig = px.bar(region_data, x='region', y='total_documents',
                 color='total_documents', color_continuous_scale='Blues')
    fig.update_layout(showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📋 Documents by Type")
    type_data = silver['document_type'].value_counts().head(8).reset_index()
    type_data.columns = ['document_type', 'count']
    fig = px.pie(type_data, names='document_type', values='count',
                 color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Documents by Year")
    year_data = by_region.groupby('document_year')['total_documents'].sum().reset_index()
    year_data = year_data.sort_values('document_year')
    fig = px.line(year_data, x='document_year', y='total_documents',
                  markers=True, color_discrete_sequence=['#1f77b4'])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏆 Top Projects by Documents")
    top_projects = by_project.head(10)
    fig = px.bar(top_projects, x='project_id', y='total_documents',
                 color='total_documents', color_continuous_scale='Blues')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# =========================
# Raw Data
# =========================
st.subheader("🔍 Browse Documents")
search = st.text_input("Search by title...")
filtered = silver[silver['title'].str.contains(search, case=False, na=False)] if search else silver
st.dataframe(filtered[['id','title','document_type','document_year','region','project_id']],
             use_container_width=True)
