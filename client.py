import socket
import urllib.parse

HOST = '127.0.0.1'
PORT = 8080

def send_get():
    request = (
        "GET /forum.html HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        "Connection: close\r\n\r\n"
    )

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(request.encode())
        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data

    print(response.decode(errors="ignore"))

def send_post(name, message):
    form_data = urllib.parse.urlencode({
        "name": name,
        "message": message
    })
    content_length = len(form_data)

    request = (
        "POST /post HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {content_length}\r\n"
        "Connection: close\r\n\r\n"
        f"{form_data}"
    )

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(request.encode())
        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data

    print(response.decode(errors="ignore"))
