"""
Social account provider configurations for allauth.

Contains settings for OAuth providers like Google.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env.dev file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env.dev")

# Configuration for social account providers
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
            "secret": os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
            "key": ""
        },
        # Request profile and email permissions
        "SCOPE": ["profile", "email"],
        # Online access type (no refresh token)
        "AUTH_PARAMS": {"access_type": "online"}
    },
}