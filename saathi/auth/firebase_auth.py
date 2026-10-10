"""
SAATHI AI - Firebase Authentication Engine
Supports Email/Password Login, Sign Up, and Google OAuth flow via Firebase REST API
with local fallback session management.
"""
import os
import requests
import json
from typing import Dict, Any, Optional, Tuple

class FirebaseAuthService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("FIREBASE_API_KEY", "")
        self.auth_url = "https://identitytoolkit.googleapis.com/v1/accounts"

    def is_firebase_configured(self) -> bool:
        """Checks whether a valid Firebase Web API key is configured."""
        return bool(self.api_key and len(self.api_key) > 20)

    def sign_up_with_email(self, email: str, password: str, display_name: str = "") -> Tuple[bool, Dict[str, Any], str]:
        """
        Registers a new user via Firebase Auth.
        Returns: (success: bool, user_data: dict, error_message: str)
        """
        if not self.is_firebase_configured():
            # Local Offline / Demo Registration
            user_id = f"user_{abs(hash(email)) % 10000000}"
            return True, {
                "localId": user_id,
                "email": email,
                "displayName": display_name or email.split("@")[0].title(),
                "idToken": f"local_token_{user_id}"
            }, ""

        endpoint = f"{self.auth_url}:signUp?key={self.api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        try:
            res = requests.post(endpoint, json=payload, timeout=10)
            data = res.json()
            if res.status_code == 200:
                return True, data, ""
            else:
                err_msg = data.get("error", {}).get("message", "Registration failed")
                return False, {}, err_msg
        except Exception as e:
            return False, {}, str(e)

    def sign_in_with_email(self, email: str, password: str) -> Tuple[bool, Dict[str, Any], str]:
        """
        Signs in an existing user with Email & Password.
        """
        if not self.is_firebase_configured():
            # Local Offline / Demo Login
            user_id = f"user_{abs(hash(email)) % 10000000}"
            return True, {
                "localId": user_id,
                "email": email,
                "displayName": email.split("@")[0].title(),
                "idToken": f"local_token_{user_id}"
            }, ""

        endpoint = f"{self.auth_url}:signInWithPassword?key={self.api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        try:
            res = requests.post(endpoint, json=payload, timeout=10)
            data = res.json()
            if res.status_code == 200:
                return True, data, ""
            else:
                err_msg = data.get("error", {}).get("message", "Invalid email or password")
                return False, {}, err_msg
        except Exception as e:
            return False, {}, str(e)

    def sign_in_with_google_id_token(self, id_token: str) -> Tuple[bool, Dict[str, Any], str]:
        """
        Verifies and signs in with a Google OAuth ID Token.
        """
        if not self.is_firebase_configured():
            user_id = "google_user_demo"
            return True, {
                "localId": user_id,
                "email": "google.user@gmail.com",
                "displayName": "Google Verified User",
                "idToken": id_token
            }, ""

        endpoint = f"{self.auth_url}:signInWithIdp?key={self.api_key}"
        payload = {
            "postBody": f"id_token={id_token}&providerId=google.com",
            "requestUri": "http://localhost",
            "returnSecureToken": True
        }
        try:
            res = requests.post(endpoint, json=payload, timeout=10)
            data = res.json()
            if res.status_code == 200:
                return True, data, ""
            else:
                err = data.get("error", {}).get("message", "Google sign-in failed")
                return False, {}, err
        except Exception as e:
            return False, {}, str(e)
