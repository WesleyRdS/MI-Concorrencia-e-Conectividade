import socket

def handle_tcp_received(conn, adrr):
    with conn:
        print(f"Conexão estabelecida com: {adrr}")


        while True:
            message = conn.recv(1024)
            if not message:
                break
            print("Menssagem TCP recebida: ", message.decode())


def midleware_tcp_udp(tcp_host, tcp_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.bind((tcp_host,tcp_port))
        tcp_socket.listen(5)
        print(f"Aguardando conexões TCP em {tcp_host}:{tcp_port}...")

        while True:
            conn, addr = tcp_socket.accept()
            handle_tcp_received(conn, addr)

if __name__ == "__main__":
    TCP_HOST = '127.0.0.1'
    TCP_PORT = 3000

    midleware_tcp_udp(TCP_HOST, TCP_PORT)