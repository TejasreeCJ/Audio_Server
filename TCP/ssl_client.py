import socket
import ssl
import pygame

def receive_audio(connection, song_name):
    with open(song_name, 'wb') as f:
        while True:
            audio_data = connection.recv(4096)
            if not audio_data:
                break
            f.write(audio_data)

def main():
    pygame.mixer.init()
    host = input("Enter the server IP address: ")
    port = int(input("Enter the server port number: "))
    song_name = input("Enter the name of the song you want to request: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False  # Disable check_hostname
    context.verify_mode = ssl.CERT_NONE  # Adjust the verification mode accordingly
    client_socket = context.wrap_socket(client_socket, server_hostname=host)
    client_socket.connect((host, port))

    client_socket.send(song_name.encode())
    receive_audio(client_socket, "temp_audio.mp3")

    pygame.mixer.music.load("temp_audio.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    client_socket.close()

if __name__ == "__main__":
    main()
