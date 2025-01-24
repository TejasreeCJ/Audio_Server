import socket
import os

# Define the directory where the songs are located
SONGS_DIRECTORY = "C:/Users/tejuc/OneDrive/Desktop/songs"

def send_audio(connection, address, song_name):
    song_path = os.path.join(SONGS_DIRECTORY, song_name)
    with open(song_path, 'rb') as f:
        while True:
            audio_data = f.read(1024)
            if not audio_data:
                break
            connection.sendto(audio_data, address)

def main():
    host = "192.168.19.74"
    port = 9998

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"Server is listening on {host}:{port}...")

    while True:
        data, addr = server_socket.recvfrom(1024)
        song_name = data.decode()

        print(f"Received request for '{song_name}' from {addr[0]}:{addr[1]}")

        # Send the requested audio file to the client
        send_audio(server_socket, addr, song_name)

    server_socket.close()

if __name__ == "__main__":
    main()
