from brwne_cli.commands.auth import get_valid_token
import requests
import json
import os


class RealtimeDBEngine:
    FIREBASE_PROJECT_ID = "oakk-74eb8"  # Replace with your Firebase project ID
    FIREBASE_API_BASE_URL = f"https://oakk-74eb8-default-rtdb.asia-southeast1.firebasedatabase.app"
    FIREBASE_WEB_API_KEY = "AIzaSyDTZGU3yS94z5XBsScVarrkRhzq9vttTdg"  # Replace with your Firebase Web API Key

    def __init__(self):
        self.auth_token = get_valid_token()
        if not self.auth_token:
            raise ValueError("Authentication token not found. Please sign in.")
        
    def get_branch_type(self, repo_id, branch_name):
        if data := self.read_data(f"repo_branches/{repo_id}/{branch_name}"):
            return data.get("type", None)
        return None
    
    def get_UID(self):
        # refresh token
        self.auth_token = get_valid_token()
        if not self.auth_token:
            raise ValueError("Authentication token not found. Please sign in.")
        
        url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup"
        headers = {"Content-Type": "application/json"}
        payload = {
            "idToken": self.auth_token
        }

        response = requests.post(f"{url}?key={self.FIREBASE_WEB_API_KEY}", headers=headers, json=payload)
        
        if response.status_code == 200:
            user_info = response.json()
            uid = user_info['users'][0]['localId']  # The UID of the user
            return uid
        else:
            print("Error retrieving UID:", response.json())
            return None
    
    def write_data(self, path, data):
        # refresh token
        self.auth_token = get_valid_token()
        if not self.auth_token:
            raise ValueError("Authentication token not found. Please sign in.")

        url = f"{self.FIREBASE_API_BASE_URL}/{path}.json?auth={self.auth_token}"
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.put(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to write data: {response.status_code} {response.text}")

    def read_data(self, path):
        # refresh token
        self.auth_token = get_valid_token()
        if not self.auth_token:
            raise ValueError("Authentication token not found. Please sign in.")
        
        url = f"{self.FIREBASE_API_BASE_URL}/{path}.json?auth={self.auth_token}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to read data: {response.status_code} {response.text}")
        
    def delete_data(self, path):
        # refresh token
        self.auth_token = get_valid_token()
        if not self.auth_token:
            raise ValueError("Authentication token not found. Please sign in.")

        url = f"{self.FIREBASE_API_BASE_URL}/{path}.json?auth={self.auth_token}"
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Typically returns `null` when the deletion is successful
        else:
            raise Exception(f"Failed to delete data: {response.status_code} {response.text}")

