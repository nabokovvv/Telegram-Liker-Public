import os

# Retrieve API credentials and check for their presence
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
session_b64 = os.getenv('SESSION_B64')
channel_username = os.getenv('CHANNEL_USERNAME')
session_name = os.getenv('SESSION_NAME')

print(f"API_ID: {api_id}")
print(f"API_HASH: {api_hash}")
print(f"SESSION_B64: {(session_b64) if session_b64 else 'Not set'}")
print(f"CHANNEL_USERNAME: {channel_username}")
print(f"SESSION_NAME: {session_name}")