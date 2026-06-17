"""
Gmail Channel Handler — Production
Handles OAuth2 auth and Gmail API interactions.
"""

import os
import base64
import re
import json
import logging
from email.mime.text import MIMEText
from datetime import datetime, timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

class GmailHandler:
    def __init__(self):
        self.credentials_file = os.getenv('GMAIL_CREDENTIALS_FILE', 'credentials.json')
        self.token_file = os.getenv('GMAIL_TOKEN_FILE', 'token.json')
        self.service = None

    def authenticate(self):
        """Authenticate with Gmail API using OAuth2."""
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    logger.warning("Gmail credentials.json not found.")
                    return
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)

    async def get_message(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Fetch and normalize a Gmail message."""
        if not self.service: self.authenticate()
        if not self.service: return None

        try:
            msg = self.service.users().messages().get(userId='me', id=message_id, format='full').execute()
            headers = {h['name']: h['value'] for h in msg['payload']['headers']}
            
            return {
                'channel': 'email',
                'channel_message_id': message_id,
                'customer_email': self._extract_email(headers.get('From', '')),
                'customer_name': self._extract_name(headers.get('From', '')),
                'subject': headers.get('Subject', 'No Subject'),
                'content': self._extract_body(msg['payload']),
                'received_at': datetime.now(timezone.utc).isoformat(),
                'metadata': {'thread_id': msg.get('threadId')}
            }
        except Exception as e:
            logger.error(f"Gmail fetch failed: {e}")
            return None

    async def send_reply(self, to_email: str, subject: str, body: str, thread_id: str = None) -> Dict[str, Any]:
        """Send email reply via Gmail API."""
        if not self.service: self.authenticate()
        if not self.service: return {'delivery_status': 'failed'}

        try:
            message = MIMEText(body)
            message['to'] = to_email
            message['subject'] = f"Re: {subject}" if not subject.startswith('Re:') else subject
            
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            send_body = {'raw': raw}
            if thread_id: send_body['threadId'] = thread_id

            result = self.service.users().messages().send(userId='me', body=send_body).execute()
            return {'channel_message_id': result['id'], 'delivery_status': 'sent'}
        except Exception as e:
            logger.error(f"Gmail send failed: {e}")
            return {'delivery_status': 'failed'}

    def _extract_body(self, payload: Dict[str, Any]) -> str:
        """Helper to extract body text from MIME payload."""
        if 'body' in payload and payload['body'].get('data'):
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    return self._extract_body(part)
        return ""

    def _extract_email(self, from_header: str) -> str:
        match = re.search(r'<(.+?)>', from_header)
        return match.group(1) if match else from_header.strip()

    def _extract_name(self, from_header: str) -> str:
        match = re.search(r'^(.+?)\s*<', from_header)
        return match.group(1).strip().strip('"') if match else ""
