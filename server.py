# server.py

import socket
import threading
import os
import json
from urllib.parse import parse_qs
import time
from datetime import datetime, timezone

HOST = '127.0.0.1'
PORT = 8080
DATA_FILE = 'posts.json'

def load_messages():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_messages(name, message):
    messages = load_messages()
    messages.append({
        "name": name, 
        "message": message, 
        "timestamp": time.time()
    })

    with open(DATA_FILE, 'w') as file:
        json.dump(messages, file, indent=4)

def render_forum_html():
    with open("forum.html", "r") as file:
        template = file.read()
    
    messages = load_messages()
    list_items = []

    for message in messages:
        # Convert timestamp biar human-readable
        timestamp = datetime.fromtimestamp(message["timestamp"], tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        list_items.append(f"""
            <li class="message">
                <div class="message-name">{message['name']}</div>
                <div>{message['message']}</div>
                <div class="message-time">Posted at {timestamp}</div>
            </li>
        """)

    list_items = "\n".join(list_items)
    return template.replace("{{messages}}", list_items)

def handle_client(connection, address):
    try:
        request = connection.recv(1024).decode()
        if not request:
            return
        
        lines = request.split("\r\n")
        method, path, _ = lines[0].split()

        # Cek if request header ada Content-Type
        headers = {line.split(": ")[0]: line.split(": ")[1] for line in lines[1:] if ": " in line}
        content_type = headers.get("Content-Type", "")

        # Ambil body request
        body = request.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in request else ""

        print(f"Received request: {method} {path}")
        if method == "GET" and path == "/forum.html":
            content = render_forum_html()
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(content)}\r\n"
                "Connection: close\r\n\r\n" +
                content
            )
            connection.sendall(response.encode())
        
        elif method == "POST" and path == "/post":
            if "application/json" in content_type:
                data = json.loads(body) # Parse JSON
                name = data.get("name", "Anonymous")
                message = data.get("message", "")
            elif "application/x-www-form-urlencoded" in content_type:
                data = parse_qs(body)  # Parse URL encoded form
                name = data.get("name", ["Anonymous"])[0]
                message = data.get("message", [""])[0]

            print(f"Received message from {name}: {message}")
            save_messages(name, message)

            response = (
                "HTTP/1.1 303 See Other\r\n"
                "Location: /forum.html\r\n"
                "Connection: close\r\n\r\n"
            )

            connection.sendall(response.encode())

        else:
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n"
                "Connection: close\r\n\r\n"
                "404 Not Found"
            )
            connection.sendall(response.encode())
    finally:
        connection.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5) # w
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            connection, address = s.accept()
            thread = threading.Thread(target=handle_client, args=(connection, address))
            thread.start()

if __name__ == "__main__":
    start_server()