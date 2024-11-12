import socketserver

CHUNK_SIZE = 1024
SERVER_ADDRESS = ("localhost", 8081)


class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(CHUNK_SIZE)
        cli = self.client_address
        msg = f"got request from {cli}: {len(data)}"
        print(msg)
        print(f"data: {data}")
        self.request.sendall(bytes(msg, "utf-8"))


class FileHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("server about to start receiving")
        data = bytes()
        while True:
            latest = self.request.recv(CHUNK_SIZE)
            print(f"...server received {len(latest)} bytes")
            data += latest
            if len(latest) < CHUNK_SIZE:
                print(f"...server breaking")
                break
        print(f"server finished received, about to reply")
        self.request.sendall(bytes(f"{data}", "utf-8"))


if __name__ == "__main__":
    server = socketserver.TCPServer(SERVER_ADDRESS, FileHandler)
    server.allow_reuse_address = True
    server.serve_forever()        
