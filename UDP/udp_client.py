import socket
import pygame
import io

def main():
    host = input("Enter the server IP address: ")
    port = int(input("Enter the server port number: "))
    song_name = input("Enter the name of the song you want to request: ")

    print(f"Requesting '{song_name}' from server {host}:{port}...")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(song_name.encode(), (host, port))

    print("Request sent to server.")

    audio_data = bytearray()

    while True:
        data, _ = client_socket.recvfrom(1024)
        audio_data.extend(data)
        if len(data) < 1024:
            break

    print("Audio data received from server.")

    pygame.mixer.init()
    audio_stream = io.BytesIO(audio_data)
    sound = pygame.mixer.Sound(audio_stream)

    print("Playing the audio stream...")

    sound.play()

    print("Press Ctrl+C to exit.")

    while pygame.mixer.get_busy():
        continue

    client_socket.close()

if __name__ == "__main__":
    main()
