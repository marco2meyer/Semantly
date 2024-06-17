import asyncio
import websockets
import json
import ssl
import requests
import threading

# WebSocket URL and API settings
websocket_url = "wss://semantlyapi-352e1ba2b5fd.herokuapp.com/ws/testgame5"
api_url = "https://semantlyapi-352e1ba2b5fd.herokuapp.com"
api_key = "my_semantly_api_password"

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Function to handle WebSocket communication
async def websocket_handler():
    async with websockets.connect(websocket_url, ssl=ssl_context) as websocket:
        # Authenticate via WebSocket
        auth_data = {"x-api-key": api_key}
        await websocket.send(json.dumps(auth_data))
        print("Sent authentication data")

        try:
            while True:
                message = await websocket.recv()
                print(f"Received message: {message}")
        except websockets.ConnectionClosed:
            print("WebSocket connection closed")

# Function to send a guess via HTTP POST request
def send_guess():
    guess_data = {"player": "player1", "guess": "testguess"}
    headers = {"x-api-key": api_key}
    response = requests.post(f"{api_url}/game/testgame5/guess", json=guess_data, headers=headers)
    if response.status_code == 200:
        print("Guess added successfully2")
    else:
        print(f"Error adding guess: {response.status_code}")

# Run the WebSocket handler in a separate thread
threading.Thread(target=asyncio.run, args=(websocket_handler(),)).start()

# Wait a bit to ensure WebSocket connection is established
asyncio.run(asyncio.sleep(1))

# Send guesses
for _ in range(5):
    send_guess()
    asyncio.run(asyncio.sleep(2))