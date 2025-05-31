import socket
import urllib.parse
import threading
import argparse
import sys

HOST = '127.0.0.1'
PORT = 8080

def send_get(f):
    request = (
        f"GET /{f} HTTP/1.1\r\n"
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

def threaded_post():
    name = input("Nama: ")
    message = input("Pesan: ")
    thread = threading.Thread(target=send_post, args=(name, message))
    thread.start()

def threaded_get(f):
    thread = threading.Thread(target=send_get, args=(f, ))
    thread.start()
    
def default_mode():
    print("Client Forum Chat")
    print("=================\n")
    print("1. Kirim pesan")
    print("2. Lihat isi forum")
    choice = input("Pilih menu (1/2): ")

    if choice == "1":
        threaded_post()
    elif choice == "2":
        f = input("Nama file? ")
        threaded_get(f) 
    else:
        print("Pilihan tidak valid.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client Forum Chat")

    parser.add_argument("server_host", nargs="?", help="Server host to untuk connect")
    parser.add_argument("server_port", nargs="?", type=int, help="Port number server")
    parser.add_argument("file_name", nargs="?", help="File yang mau diminta")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        default_mode() # Yang dikerjain sudes beni kemarin
    elif args.server_host and args.server_port and args.file_name:
        print(f"Membuat koneksi ke {args.server_host}:{args.server_port}, meminta {args.file_name}")
        threaded_get(args.file_name)
    else:
        print("Penggunaan invalid. Coba --help buat liat instruksi.")
