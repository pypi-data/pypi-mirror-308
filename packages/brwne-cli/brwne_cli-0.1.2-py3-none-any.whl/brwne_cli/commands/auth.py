import requests
import click
import time
import keyring

FIREBASE_API_KEY = "AIzaSyDTZGU3yS94z5XBsScVarrkRhzq9vttTdg"  # Replace with your Firebase Web API Key
SERVICE_NAME = "brwne"  # Service name used for storing tokens in keyring

def login_command():
    """Login to the brwne CLI tool"""
    # Step 1: Get user credentials
    email = click.prompt("Please enter your email", type=str)
    password = click.prompt("Please enter your password", type=str, hide_input=True)

    # Step 2: Authenticate with Firebase Auth REST API
    firebase_auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(firebase_auth_url, json=payload)

    # Step 3: Handle response
    if response.status_code == 200:
        # Successful login
        response_data = response.json()
        id_token = response_data['idToken']
        refresh_token = response_data['refreshToken']
        expires_in = int(response_data['expiresIn'])  # Token validity duration in seconds
        expires_at = time.time() + expires_in

        # Save the tokens and expiry information in keyring
        print("Saving tokens in keyring...")
        print("id_token:", id_token)
        print("refresh_token:", refresh_token)
        print("expires_at:", expires_at)

        keyring.set_password(SERVICE_NAME, "id_token", id_token)
        keyring.set_password(SERVICE_NAME, "refresh_token", refresh_token)
        keyring.set_password(SERVICE_NAME, "expires_at", str(expires_at))

        click.echo("Login successful! 🎉")
    else:
        # Failed login
        error_message = response.json().get('error', {}).get('message', 'Unknown error')
        click.echo(f"Login failed: {error_message} 😔")

def logout_command():
    """Logout by removing tokens from keyring"""
    keyring.delete_password(SERVICE_NAME, "id_token")
    keyring.delete_password(SERVICE_NAME, "refresh_token")
    keyring.delete_password(SERVICE_NAME, "expires_at")
    click.echo("You have been logged out successfully. See you soon :)")

def get_valid_token():
    """Get a valid ID token, refreshing if necessary"""
    # Retrieve tokens and expiry information from keyring
    id_token = keyring.get_password(SERVICE_NAME, "id_token")
    refresh_token = keyring.get_password(SERVICE_NAME, "refresh_token")
    expires_at = keyring.get_password(SERVICE_NAME, "expires_at")

    if not id_token or not refresh_token or not expires_at:
        click.echo("No valid token found. Please log in first.")
        return None

    # Step 3: Check if the token is expired
    expires_at = float(expires_at)
    if time.time() > expires_at:
        # Token is expired, refresh it
        click.echo("Token expired, refreshing...")
        firebase_refresh_url = f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_API_KEY}"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }

        response = requests.post(firebase_refresh_url, data=payload)
        if response.status_code == 200:
            response_data = response.json()
            new_id_token = response_data['id_token']
            new_refresh_token = response_data['refresh_token']
            expires_in = int(response_data['expires_in'])
            new_expires_at = time.time() + expires_in

            # Update tokens in keyring
            keyring.set_password(SERVICE_NAME, "id_token", new_id_token)
            keyring.set_password(SERVICE_NAME, "refresh_token", new_refresh_token)
            keyring.set_password(SERVICE_NAME, "expires_at", str(new_expires_at))

            return new_id_token
        else:
            click.echo("Failed to refresh token.")
            return None
    else:
        # Token is still valid
        return id_token

def user_is_logged_in():
    """Check if the user is currently logged in"""
    id_token = get_valid_token()
    if id_token:
        return True
    else:
        return False