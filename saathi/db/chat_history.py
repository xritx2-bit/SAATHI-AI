"""
SAATHI AI - Persistent Chat History & Session Storage
Stores multi-session conversation history, message metadata, citations, 
and approved action records (like ChatGPT / Claude) with local SQLite and Firestore sync support.
"""
import sqlite3
import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

class ChatHistoryManager:
    def __init__(self, db_path: str = "data/saathi_chat_history.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initializes database tables for user sessions, messages, and action records."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                email TEXT UNIQUE,
                display_name TEXT,
                auth_provider TEXT DEFAULT 'email',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Chat sessions table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
            """)
            
            # Chat messages table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                message_id TEXT PRIMARY KEY,
                session_id TEXT,
                role TEXT,
                content TEXT,
                decision_json TEXT,
                citations_json TEXT,
                action_json TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_sessions (session_id)
            )
            """)
            
            # Approved actions audit table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS approved_actions (
                action_id TEXT PRIMARY KEY,
                user_id TEXT,
                session_id TEXT,
                action_type TEXT,
                title TEXT,
                final_content TEXT,
                approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()

    def create_or_get_user(self, user_id: str, email: str, display_name: str = "Citizen User", auth_provider: str = "email") -> Dict[str, Any]:
        """Creates or retrieves a user profile."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, email, display_name FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                cursor.execute(
                    "INSERT INTO users (user_id, email, display_name, auth_provider) VALUES (?, ?, ?, ?)",
                    (user_id, email, display_name, auth_provider)
                )
                conn.commit()
                return {"user_id": user_id, "email": email, "display_name": display_name}
            return {"user_id": row[0], "email": row[1], "display_name": row[2]}

    def create_session(self, user_id: str, title: str = "New Conversation") -> str:
        """Creates a new conversation thread for a user."""
        session_id = f"sess_{uuid.uuid4().hex[:12]}"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chat_sessions (session_id, user_id, title) VALUES (?, ?, ?)",
                (session_id, user_id, title)
            )
            conn.commit()
        return session_id

    def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieves all past conversation threads for a user sorted by most recent."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT session_id, user_id, title, created_at, updated_at FROM chat_sessions WHERE user_id = ? ORDER BY updated_at DESC",
                (user_id,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def update_session_title(self, session_id: str, title: str):
        """Updates the title of a conversation thread."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE chat_sessions SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE session_id = ?", (title, session_id))
            conn.commit()

    def delete_session(self, session_id: str):
        """Deletes a conversation session and all its messages."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
            cursor.execute("DELETE FROM chat_sessions WHERE session_id = ?", (session_id,))
            conn.commit()

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
        decision: Optional[Any] = None,
        citations: Optional[List[str]] = None,
        action: Optional[Any] = None
    ):
        """Saves a message to the database and updates session timestamp."""
        msg_id = f"msg_{uuid.uuid4().hex[:12]}"
        
        # Serialize Pydantic objects or dicts
        dec_dict = decision.model_dump(mode="json") if hasattr(decision, "model_dump") else decision
        dec_str = json.dumps(dec_dict, ensure_ascii=False) if decision else None
        cit_str = json.dumps(citations, ensure_ascii=False) if citations else None
        act_dict = action.model_dump(mode="json") if hasattr(action, "model_dump") else action
        act_str = json.dumps(act_dict, ensure_ascii=False) if action else None

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO chat_messages (message_id, session_id, role, content, decision_json, citations_json, action_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (msg_id, session_id, role, content, dec_str, cit_str, act_str)
            )
            cursor.execute("UPDATE chat_sessions SET updated_at = CURRENT_TIMESTAMP WHERE session_id = ?", (session_id,))
            conn.commit()

    def get_session_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """Loads full conversation history for a specific session."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT message_id, role, content, decision_json, citations_json, action_json, timestamp FROM chat_messages WHERE session_id = ? ORDER BY timestamp ASC",
                (session_id,)
            )
            rows = cursor.fetchall()
            messages = []
            for r in rows:
                dec = json.loads(r["decision_json"]) if r["decision_json"] else None
                cit = json.loads(r["citations_json"]) if r["citations_json"] else []
                act = json.loads(r["action_json"]) if r["action_json"] else None
                messages.append({
                    "role": r["role"],
                    "content": r["content"],
                    "decision": dec,
                    "citations": cit,
                    "action": act,
                    "timestamp": r["timestamp"]
                })
            return messages

    def save_approved_action(self, user_id: str, session_id: str, action_type: str, title: str, final_content: str):
        """Records an approved action for audit and user history."""
        act_id = f"aud_{uuid.uuid4().hex[:10]}"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO approved_actions (action_id, user_id, session_id, action_type, title, final_content) VALUES (?, ?, ?, ?, ?, ?)",
                (act_id, user_id, session_id, action_type, title, final_content)
            )
            conn.commit()

    def get_user_approved_actions(self, user_id: str) -> List[Dict[str, Any]]:
        """Fetches all past approved action drafts (letters, checklists) for a user."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT action_id, title, action_type, final_content, approved_at FROM approved_actions WHERE user_id = ? ORDER BY approved_at DESC",
                (user_id,)
            )
            return [dict(r) for r in cursor.fetchall()]
