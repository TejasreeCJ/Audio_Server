# 🎵 Audio Streaming Project (UDP + TCP/SSL)

A simple client–server audio streaming system implemented in Python, showcasing two transport modes:

- **UDP mode** — lightweight, low-latency datagram streaming (no reliability).
- **TCP (TLS) mode** — reliable, ordered, and encrypted streaming with multi-client support.

This README provides a single, consolidated guide covering **concepts, how it works, how to run, configuration, interview points, and improvements**.

---

## 📦 Requirements

- **Python 3.8+**
- **pip packages**: `pygame`
- **OpenSSL** (only for generating a self-signed certificate in TLS mode)

Install pygame:
```bash
pip install pygame
```

> **Note**: On some systems, `pygame` audio backends may require additional OS packages or drivers.

---

## 📂 Project Structure

```
├── udp_client.py        # UDP client: requests and plays audio
├── udp_server.py        # UDP server: sends audio files to clients
├── tcp_client.py        # TCP client (TLS): requests, downloads, plays
├── tcp_server.py        # TCP server (TLS): multi-client handler
├── songs/               # Directory containing audio files (e.g., .mp3, .wav)
├── cert.pem             # TLS certificate (server)
├── key.pem              # TLS private key (server)
└── README.md            # This file
```

---

## 🧠 High-Level Overview

### Why UDP?
- **Pros:** Minimal overhead, low latency; good for live/real-time media (VoIP, gaming).
- **Cons:** No guarantees—packets can be **lost**, **duplicated**, or **reordered**.

### Why TCP + TLS?
- **Pros:** Reliable and ordered delivery; **TLS** provides encryption and server authentication; easier application logic.
- **Cons:** More overhead and slightly higher latency; requires certificate management.

---

## ⚙️ How It Works

### UDP Mode (Connectionless Streaming)
- **Client** sends the **song name** as a single UDP datagram to the server.
- **Server** reads the requested file in **fixed-size chunks** (e.g., 1024 bytes) and sends each chunk using `sendto`.
- **Client** receives chunks and reconstructs the file in memory (or buffer), then plays via `pygame`.

> Current implementation waits for the entire file before playback. You can evolve it to *play while receiving* by buffering and feeding the mixer progressively.

### TCP (TLS) Mode (Reliable + Secure)
- **Server** listens on a TCP socket, wraps accepted connections with **TLS** (using `cert.pem` + `key.pem`).
- **Client** creates a TCP connection and wraps it in **TLS**.
- Client sends the song name; server streams the file using `sendall`.
- Client **saves to a temp file** (e.g., `temp_audio.mp3`) and then plays it with `pygame`.
- **Thread-per-connection** server model supports multiple concurrent clients.

> The sample `tcp_client.py` disables cert verification (`CERT_NONE`) for ease of testing. In production, enable verification and provide the CA/cert chain to the client.

---

## 🚀 Quickstart

### 0) Put Audio Files
Place your audio files in the server’s `songs/` directory.
- The provided code uses a hardcoded path in the server:  
  `SONGS_DIRECTORY = "C:/Users/tejuc/OneDrive/Desktop/songs"`  
  Update it (or make it relative) to match your environment.

### 1) Run in **UDP** Mode

**Server (example: port 9998):**
```bash
python udp_server.py
```
Expected:
```
Server is listening on <host>:9998...
Received request for '<song>.mp3' from <client-ip>:<port>
```

**Client:**
```bash
python udp_client.py
```
Input when prompted:
- Server IP (e.g., `192.168.19.74`)
- Port (e.g., `9998`)
- Song file name (e.g., `song.mp3`)

Playback should start after the file is fully received.

### 2) Run in **TCP (TLS)** Mode

**Generate a self-signed certificate** (for testing):
```bash
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
```
> For local testing, you can set common name (CN) to the server’s IP or hostname.

**Server (example: port 9999):**
```bash
python tcp_server.py
```
Expected:
```
Server listening on port: 9999
Connection from ('<client-ip>', <port>)
Requested song: <song>.mp3
```

**Client:**
```bash
python tcp_client.py
```
Input when prompted:
- Server IP (e.g., `192.168.19.74`)
- Port (e.g., `9999`)
- Song file name (e.g., `song.mp3`)

The client downloads `temp_audio.mp3` then plays it.

---

## 🔧 Configuration

- **Song Directory (Server):**
  - Update `SONGS_DIRECTORY` in `udp_server.py` and `tcp_server.py` to point to your audio folder.
- **Host & Port:**
  - TCP/UDP servers bind to `host` & `port` variables—modify as needed (e.g., bind to `0.0.0.0` to listen on all NICs).
- **Chunk Size:**
  - UDP: `1024` bytes; TCP: `1024`–`4096` bytes. Tune for your network.
- **TLS Verification (Client):**
  - Example client disables verification (`CERT_NONE`) and `check_hostname=False`—**only for testing**.
  - For production, provide CA or server certificate and set:
    ```python
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile="cert.pem")
    # or context.load_verify_locations("ca.pem")
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    ```

---

## 🆚 UDP vs TCP (TLS) — Side-by-Side

| Feature            | UDP (Datagrams)                            | TCP + TLS (Streams)                                   |
|-------------------|---------------------------------------------|-------------------------------------------------------|
| Connection        | Connectionless                              | Connection-oriented                                   |
| Reliability       | No (loss/reorder/duplication possible)      | Yes (ordered, reliable delivery)                      |
| Security          | None (in sample)                            | Encrypted (TLS), server authentication                |
| Latency           | Lower                                        | Higher (handshake, retransmissions, TLS)              |
| Complexity        | Simple                                       | Higher (TLS, threads, certs)                          |
| Scalability       | Basic (single-threaded in sample)           | Thread-per-connection (multi-client)                  |
| Best for          | Live/real-time tolerant streams              | File transfer / secure media streaming                |

---

## 🛡️ Security Notes

- The sample TCP client **disables certificate verification** for convenience. For real deployments:
  - Use a trusted CA or ship your own CA bundle.
  - Enable hostname verification and `CERT_REQUIRED`.
- Protect `key.pem` properly (file permissions).

---

## 🧪 Troubleshooting

- **Audio doesn’t play:** Ensure `pygame.mixer.init()` succeeds and audio backend is available; verify file format (MP3/WAV).
- **File not found:** Check `SONGS_DIRECTORY` path and filename.
- **Firewall/NAT issues:** Ensure ports (UDP/TCP) are open between client and server.
- **TLS handshake fails:** Verify `cert.pem`/`key.pem` and client’s verification settings.

---

## 📜 License

This project is provided as-is for educational purposes.
