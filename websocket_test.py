import websocket
import json
import threading
import ssl
import time

# URL of the deployed FastAPI WebSocket on Heroku
ws_url = "wss://semantlyapi-352e1ba2b5fd.herokuapp.com/ws/testgame5"

def on_message(ws, message):
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")
    print(f"Close status code: {close_status_code}")
    print(f"Close message: {close_msg}")

def on_open(ws):
    def run(*args):
        api_key = "my_semantly_api_password"  # Replace with your actual API password
        auth_data = {
            "x-api-key": api_key
        }
        
        # Sending the authentication header
        ws.send(json.dumps(auth_data))
        print("Sent authentication data")
        
        # Sending a guess to the game
        guess_data = {
            "player": "player1",
            "guess": "testguess"
        }
        ws.send(json.dumps(guess_data))
        print("Sent guess data")
        
        time.sleep(5)  # Wait to see if any messages are received
        ws.close()
        print("WebSocket connection closed")

    thread = threading.Thread(target=run)
    thread.start()

# Create a WebSocket app with SSL certificate verification disabled
ws = websocket.WebSocketApp(ws_url,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

# Run the WebSocket app with SSL certificate verification disabled
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})