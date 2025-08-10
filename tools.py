# tools.py
from __future__ import print_function
import os.path
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scope for Gmail API.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# --- START OF CORRECTION ---
# Get the absolute path of the directory where this script is located.
# This makes sure we can always find our credential and token files.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(SCRIPT_DIR, 'credentials.json')
TOKEN_PATH = os.path.join(SCRIPT_DIR, 'token.json')
# --- END OF CORRECTION ---

class GmailTool:
    """A tool for interacting with the Gmail API."""

    def __init__(self):
        """
        Initializes the GmailTool, handling user authentication and
        building the Gmail API service object.
        """
        creds = None
        # Look for token.json at the absolute path.
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Look for credentials.json at the absolute path.
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run at the absolute path.
            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())

        self.creds = creds
        self.service = build('gmail', 'v1', credentials=self.creds)
        
        # Print the email address being used for confirmation
        profile = self.service.users().getProfile(userId='me').execute()
        print(f"Authenticated as: {profile['emailAddress']}")

    def create_draft(self, to: str, subject: str, body: str) -> str:
        """
        Creates a draft email in the user's Gmail account.
        """
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {'message': {'raw': encoded_message}}
            draft = self.service.users().drafts().create(userId='me', body=create_message).execute()
            return f"Draft created successfully for {to} with subject '{subject}'."
        except HttpError as error:
            return f"Failed to create draft. Error: {error}"

    def send_email(self, to: str, subject:str, body: str) -> str:
        """
        Creates and immediately sends an email from the user's Gmail account.
        """
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {'raw': encoded_message}
            send_message = self.service.users().messages().send(userId='me', body=create_message).execute()
            return f"Email sent successfully to {to} with subject '{subject}'."
        except HttpError as error:
            return f"Failed to send email. Error: {error}"
