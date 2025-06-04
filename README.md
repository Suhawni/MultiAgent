**Multi-Format Autonomous AI System**

**Overview**

The Multi-Format Autonomous AI System processes files of different formats (emails, JSON, PDFs) and automatically classifies, extracts relevant details, and takes necessary actions, including triggering API calls based on tone and urgency. It maintains an audit trail using SQLite for logging all actions.

Features
File classification (Detect format: Email, JSON, PDF)

Email Processing (Tone detection, urgency classification, action routing)

JSON Validation (Schema enforcement, anomaly detection)

PDF Analysis (Extract invoices, compliance mentions)

Action Routing (Escalate complaints, send alerts, log transactions)

Database Logging (Persist audit logs in SQLite)

Streamlit UI (Upload files, view logs, inspect API actions)

Project Architecture

📦 Multi-Format Autonomous AI System

│
├── app/
│   ├── main.py               # FastAPI server, API endpoints, request handling

│   ├── classifier_agent.py   # Identifies file type and intent

│   ├── email_agent.py        # Processes email content (tone, urgency, keywords)

│   ├── json_agent.py         # Validates JSON schema, extracts anomalies

│   ├── pdf_agent.py          # Extracts PDF invoice total, detects compliance mentions

│   ├── action_router.py      # Routes actions (CRM escalation, compliance alerts)

│   ├── memory_store.py       # Persistent SQLite logging (metadata, agent outputs, alerts)

│   └── utils/

│       ├── file_parser.py    # Detects format and parses content

│       ├── tone_detector.py  # Identifies email tone (angry, polite, escalation)

│       ├── schema_validator.py  # Validates JSON schema

│       ├── pdf_utils.py      # Extracts relevant details from PDFs

│
├── data/                     # Sample files (emails, JSONs, PDFs)

│

├── requirements.txt          # Dependencies for installation

├── streamlit_app.py          # Streamlit UI interface

├── memory_logs.db            # SQLite database storing logs

└── README.md                 # Documentation

---

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python 3.7+ installed. Install required libraries:
```bash
pip install -r requirements.txt
2. Run FastAPI Backend
Start the FastAPI server using Uvicorn:

bash
uvicorn app.main:app --reload
The server will be available at http://127.0.0.1:8000

3. Start Streamlit UI
Run the Streamlit interface for file uploads and log display:

bash
streamlit run streamlit_app.py
Access the UI at http://localhost:8501

Using the Project
1. Uploading a File (Email, JSON, PDF)
Open the Streamlit UI (http://localhost:8501)

Select an email, JSON, or PDF file and upload it

The system will classify the file, extract details, and trigger actions if required

The response will show classification details, extracted content, and triggered API calls

2. Viewing Logs & API Calls
Open the sidebar in Streamlit and click Refresh Logs

You will see:

Metadata Logs (File type, business intent)

Agent Outputs (Processed file details)

Alerts (Anomalies detected, escalations triggered)

3. API Reference
/upload
POST Uploads a file (Email, JSON, PDF)

Returns processed content, classification, and actions taken

/crm/escalate
POST Simulates an API call to escalate a complaint to CRM

/logs/metadata
GET Retrieves metadata logs from SQLite

/logs/agent
GET Retrieves agent processing outputs

/logs/alerts
GET Retrieves alerts recorded in the database
