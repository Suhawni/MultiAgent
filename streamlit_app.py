import streamlit as st
import requests
import sqlite3
import pandas as pd
import json

API_UPLOAD = "http://127.0.0.1:8000/upload"

@st.cache_data(ttl=5)  
def get_logs(query):
    conn = sqlite3.connect("memory_logs.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


st.sidebar.header("Audit Logs (SQLite Database)")
if st.sidebar.button("Refresh Logs"):
    metadata_logs = get_logs("SELECT * FROM metadata_log")
    agent_logs = get_logs("SELECT * FROM agent_output")
    alerts = get_logs("SELECT * FROM alerts")

    st.sidebar.subheader("Metadata Logs")
    st.sidebar.dataframe(metadata_logs)

    st.sidebar.subheader("Agent Outputs")
    st.sidebar.dataframe(agent_logs)

    st.sidebar.subheader("Alerts")
    st.sidebar.dataframe(alerts)
else:
    st.sidebar.info("Click 'Refresh Logs' to view the latest database records.")

st.title("Multi-Format Autonomous AI System")
st.write("Upload an email, JSON, or PDF file to trigger the processing and API calls.")

uploaded_file = st.file_uploader("Choose a file", type=["eml", "json", "pdf"])

if uploaded_file is not None:
    st.write("**Filename:**", uploaded_file.name)
    st.write("**File type:**", uploaded_file.type)
 
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    st.info("Sending file to the backend...")
    try:
        response = requests.post(API_UPLOAD, files=files)
        if response.status_code == 200:
            result = response.json()
            st.subheader("Processing Output:")
            st.json(result)
        else:
            st.error(f"Error: Received status code {response.status_code}")
    except Exception as e:
        st.error(f"An exception occurred while uploading: {e}")

st.markdown("---")
st.write("This application uses the backend API to classify the input file, trigger actions (such as notifying CRM via a simulated API call), and logs all steps in a SQLite database. Use the sidebar to inspect these audit logs.")
