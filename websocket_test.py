
import streamlit as st
import asyncio
import socketio
import requests
import pandas as pd

# WebSocket URL and API settings
websocket_url = "wss://semantlyapi-352e1ba2b5fd.herokuapp.com/ws/testgame5"
api_url = "https://semantlyapi-352e1ba2b5fd.herokuapp.com"
api_key = "my_semantly_api_password"

# Initialize SocketIO client
sio = socketio.AsyncClient()

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

# SocketIO event handler for receiving new guesses
@sio.event
async def connect():
    print("Connected to the WebSocket server")

@sio.event
async def new_guess(data):
    guess_data = data["guess"]
    st.session_state['guesses'].append(guess_data)
    st.experimental_rerun()

@sio.event
async def disconnect():
    print("Disconnected from the WebSocket server")

# Function to send a guess via HTTP POST request
def send_guess():
    guess_data = {"player": "player1", "guess": "testguess"}
    headers = {"x-api-key": api_key}
    response = requests.post(f"{api_url}/game/testgame5/guess", json=guess_data, headers=headers)
    if response.status_code == 200:
        st.success("Guess added successfully")
    else:
        st.error(f"Error adding guess: {response.status_code}")

# Function to start the SocketIO client
async def start_socketio_client():
    await sio.connect(websocket_url)
    await sio.wait()

# Start the SocketIO client
if 'sio_running' not in st.session_state:
    asyncio.run(start_socketio_client())
    st.session_state['sio_running'] = True

# Streamlit UI
st.title("Semantly Guessing Game")

if st.button("Add Guess"):
    send_guess()

# Fetch guesses and display in table
fetch_guesses()
if st.session_state['guesses']:
    df = pd.DataFrame(st.session_state['guesses'])
    st.table(df)