import socket
import os
import threading
import ssl

SONGS_DIRECTORY = "C:/Users/tejuc/OneDrive/Desktop/songs"

def send_audio(connection, address, song_name):
    song_path = os.path.join(SONGS_DIRECTORY, song_name)
    with open(song_path, 'rb') as f:
        while True:
            audio_data = f.read(1024)
            if not audio_data:
                break
            connection.sendall(audio_data)

def handle_client(conn, addr):
    print(f"Connection from {addr}")
    song_name = conn.recv(1024).decode()
    print(f"Requested song: {song_name}")
    if os.path.exists(os.path.join(SONGS_DIRECTORY, song_name)):
        send_audio(conn, addr, song_name)
    else:
        print("Error: File not found")
    conn.close()

def main():
    host = "192.168.19.74"
    port = 9999

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server listening on port:", port)

    while True:
        conn, addr = server_socket.accept()
        conn = ssl.wrap_socket(conn, server_side=True, certfile="cert.pem", keyfile="key.pem", ssl_version=ssl.PROTOCOL_TLS)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
