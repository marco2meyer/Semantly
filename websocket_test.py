import streamlit as st
import asyncio
import websockets
import json
import ssl
import requests
import pandas as pd
import threading

# WebSocket URL and API settings
websocket_url = "wss://semantlyapi-352e1ba2b5fd.herokuapp.com/ws/testgame5"
api_url = "https://semantlyapi-352e1ba2b5fd.herokuapp.com"
api_key = "my_semantly_api_password"

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Initialize Streamlit session state
if 'guesses' not in st.session_state:
    st.session_state['guesses'] = []

# Function to fetch guesses from the API
def fetch_guesses():
    headers = {"x-api-key": api_key}
    response = requests.get(f"{api_url}/game/testgame5/guesses", headers=headers)
    if response.status_code == 200:
        st.session_state['guesses'] = response.json()["user_guesses"]
    else:
        st.error(f"Error fetching guesses: {response.status_code}")

# Function to handle WebSocket messages and trigger data refresh
async def websocket_handler():
    async with websockets.connect(websocket_url, ssl=ssl_context) as websocket:
        while True:
            message = await websocket.recv()
            guess_data = json.loads(message)
            #fetch_guesses()  # Refresh the data from the API
            st.rerun()

# Function to send a guess via HTTP POST request
def send_guess():
    guess_data = {"player": "player1", "guess": "testguess"}
    headers = {"x-api-key": api_key}
    response = requests.post(f"{api_url}/game/testgame5/guess", json=guess_data, headers=headers)
    if response.status_code == 200:
        st.success("Guess added successfully")
    else:
        st.error(f"Error adding guess: {response.status_code}")

# Start the WebSocket listener in a separate asyncio loop
async def start_websocket_listener():
    await websocket_handler()

def run_websocket_listener():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_websocket_listener())

# Ensure the WebSocket listener runs in a separate thread
if 'websocket_thread' not in st.session_state:
    websocket_thread = threading.Thread(target=run_websocket_listener, daemon=True)
    websocket_thread.start()
    st.session_state['websocket_thread'] = websocket_thread

# Streamlit UI
st.title("Semantly Guessing Game")

if st.button("Add Guess"):
    send_guess()

# Fetch guesses and display in table
fetch_guesses()
if st.session_state['guesses']:
    df = pd.DataFrame(st.session_state['guesses'])
    st.table(df)