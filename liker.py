import asyncio
import logging
from telethon import TelegramClient
from telethon.errors import RPCError
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji
import random
from datetime import datetime, timezone, timedelta
import os
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)

# Retrieve API credentials and channel username from Replit environment secrets
api_id = int(os.getenv('API_ID'))  # Ensure this is an integer
api_hash = os.getenv('API_HASH')
session_b64 = os.getenv('SESSION_B64')  # Base64-encoded session file content
channel_username = os.getenv('CHANNEL_USERNAME')  # Channel username as a secret

# Decode the base64-encoded session and save it as a file
session_name = 'decoded_session'
with open(f"{session_name}.session", "wb") as session_file:
    session_file.write(base64.b64decode(session_b64))

# List of possible reactions
reactions = ['👍', '❤', '🔥']

# Define the main asynchronous function
async def main():
    # Initialize the client with the existing session file
    client = TelegramClient(session_name, api_id, api_hash)

    # Start the client
    await client.start()

    while True:
        try:
            # Get the current time in Moscow time zone (UTC+3)
            moscow_tz = timezone(timedelta(hours=3))
            current_time = datetime.now(moscow_tz)
            current_hour = current_time.hour
            current_minute = current_time.minute

            # Check if the current time is outside of the restricted hours (10:20 PM to 6:40 AM)
            if not (current_hour == 22 and current_minute >= 20 or 23 <= current_hour or current_hour < 6 or (current_hour == 6 and current_minute < 40)):
                # Get the channel entity
                channel = await client.get_entity(channel_username)

                # Get the last message from the channel
                messages = await client.get_messages(channel, limit=1)
                message = messages[0]

                # Randomly select a reaction
                reaction_choice = random.choice(reactions)

                # Add a reaction to the message
                result = await client(SendReactionRequest(
                    peer=channel,
                    msg_id=message.id,
                    reaction=[ReactionEmoji(reaction_choice)],
                ))

                logging.info(f"Reaction '{reaction_choice}' added successfully to message ID {message.id}!")

        except RPCError as e:
            logging.error(f"An RPC error occurred: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

        # Wait for a while before checking again
        await asyncio.sleep(1080)  # Check every 18 minutes

    # Stop the client after completing the action
    await client.disconnect()

# Run the main function
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Script interrupted by user.")
