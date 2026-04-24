"""
Configuration management for ListSync (patched for Seer support).
"""

import base64
import getpass
import json
import os
import sqlite3
import time
from typing import Optional, Tuple

import requests
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from halo import Halo

from .utils.helpers import custom_input, color_gradient
from .utils.logger import DATA_DIR

CONFIG_FILE = os.path.join(DATA_DIR, "config.enc")


# ========================
# Encryption helpers
# ========================

def encrypt_config(data, password):
    key = base64.urlsafe_b64encode(password.encode().ljust(32)[:32])
    fernet = Fernet(key)
    return fernet.encrypt(json.dumps(data).encode())


def decrypt_config(encrypted_data, password):
    key = base64.urlsafe_b64encode(password.encode().ljust(32)[:32])
    fernet = Fernet(key)
    return json.loads(fernet.decrypt(encrypted_data).decode())


# ========================
# Save / Load config
# ========================

def save_config(overseerr_url, api_key, requester_user_id):
    config = {
        "overseerr_url": overseerr_url,
        "api_key": api_key,
        "requester_user_id": requester_user_id
    }

    print(color_gradient("🔐  Enter a password to encrypt your API details: ", "#ff0000", "#aa0000"), end="")
    password = getpass.getpass("")
    encrypted_config = encrypt_config(config, password)

    with open(CONFIG_FILE, "wb") as f:
        f.write(encrypted_config)

    print(color_gradient("\n✅  Details encrypted. Remember your password!\n", "#00ff00", "#00aa00"))


def load_config() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "rb") as f:
            encrypted_config = f.read()

        for _ in range(3):
            password = getpass.getpass(color_gradient("🔑  Enter your password: ", "#ff0000", "#aa0000"))
            try:
                config = decrypt_config(encrypted_config, password)
                return config["overseerr_url"], config["api_key"], config["requester_user_id"]
            except Exception:
                print(color_gradient("❌  Incorrect password.", "#ff0000", "#aa0000"))

        return None, None, None

    return None, None, None


# ========================
# 🔥 PATCHED: Seer test
# ========================

def test_overseerr_api(overseerr_url, api_key=None):
    spinner = Halo(text=color_gradient("🔍  Testing connection...", "#ffaa00", "#ff5500"), spinner="dots")
    spinner.start()

    try:
        session = requests.Session()

        email = os.getenv("SEER_EMAIL")
        password = os.getenv("SEER_PASSWORD")

        if email and password:
            # 🔥 Seer login
            login = session.post(
                f"{overseerr_url}/api/v1/auth/login",
                json={"email": email, "password": password}
            )

            if login.status_code != 200:
                raise Exception(f"Login failed: {login.text}")

            response = session.get(f"{overseerr_url}/api/v1/status")
        else:
            # fallback API key
            headers = {"X-Api-Key": api_key}
            response = requests.get(f"{overseerr_url}/api/v1/status", headers=headers)

        response.raise_for_status()

        spinner.succeed(color_gradient("🎉  Connection successful!", "#00ff00", "#00aa00"))

    except Exception as e:
        spinner.fail(color_gradient(f"❌  Connection failed: {str(e)}", "#ff0000", "#aa0000"))
        raise


# ========================
# 🔥 PATCHED loader
# ========================

def load_env_config() -> Tuple[Optional[str], Optional[str], Optional[str], float, bool, bool]:
    if os.path.exists('.env'):
        load_dotenv()

    url = os.getenv('OVERSEERR_URL')
    api_key = os.getenv('OVERSEERR_API_KEY')
    email = os.getenv('SEER_EMAIL')
    password = os.getenv('SEER_PASSWORD')

    user_id = os.getenv('OVERSEERR_USER_ID', '1')
    sync_interval = float(os.getenv('SYNC_INTERVAL', '12'))
    automated_mode = os.getenv('AUTOMATED_MODE', 'true').lower() == 'true'
    is_4k = os.getenv('OVERSEERR_4K', 'false').lower() == 'true'

    # 🔥 allow either API key OR login
    if url and (api_key or (email and password)):
        test_overseerr_api(url, api_key)
        return url, api_key, user_id, sync_interval, automated_mode, is_4k

    return None, None, None, 0.0, False, False


# ========================
# Other helpers (unchanged)
# ========================

def get_tmdb_api_key():
    if os.path.exists('.env'):
        load_dotenv()
    return os.getenv('TMDB_KEY')


def get_tvdb_api_key():
    if os.path.exists('.env'):
        load_dotenv()
    return os.getenv('TVDB_KEY')


def get_trakt_client_id():
    if os.path.exists('.env'):
        load_dotenv()
    return os.getenv('TRAKT_CLIENT_ID')
