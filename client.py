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

    # Cetak isi HTML sebagai teks
    html = response.decode(errors="ignore")
    body = html.split("\r\n\r\n", 1)[-1]
    print("\n==== Isi Forum ====\n")
    print(body)

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

    print("\nPesan berhasil dikirim!")

# Menu tambahan buat cmd
if __name__ == "__main__":
    print("Client Forum Chat")
    print("=================\n")
    print("1. Kirim pesan")
    print("2. Lihat isi forum")
    choice = input("Pilih menu (1/2): ")

    if choice == "1":
        name = input("Nama: ")
        message = input("Pesan: ")
        send_post(name, message)
    elif choice == "2":
        send_get()
    else:
        print("Pilihan tidak valid.")
