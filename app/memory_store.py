import sqlite3
import json

class MemoryStore:
    def __init__(self, db_path="memory_logs.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            # Table for metadata logs.
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS metadata_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metadata TEXT
                )
            ''')
            # Table for agent outputs.
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS agent_output (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_type TEXT,
                    output TEXT
                )
            ''')
            # Table for alerts.
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT,
                    alert TEXT
                )
            ''')

    def log_metadata(self, metadata):
        print("[Metadata]", metadata)
        with self.conn:
            self.conn.execute('INSERT INTO metadata_log (metadata) VALUES (?)', (json.dumps(metadata),))
    
    def log_agent_output(self, agent_type, output):
        print(f"[{agent_type.capitalize()} Agent Output]", output)
        with self.conn:
            self.conn.execute('INSERT INTO agent_output (agent_type, output) VALUES (?, ?)', (agent_type, json.dumps(output)))
    
    def log_alert(self, source, alert):
        print(f"[ALERT from {source}]", alert)
        with self.conn:
            alert_text = json.dumps(alert) if isinstance(alert, (list, dict)) else str(alert)
            self.conn.execute('INSERT INTO alerts (source, alert) VALUES (?, ?)', (source, alert_text))
