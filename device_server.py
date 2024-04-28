import socket
import devices
import json



class device:
    def __init__(self,type, id, host, port) -> None:
        self.type = type
        self.id = id
        self.host = host
        self.port = port

    def initial_sendo(self):
        string = self.type+"/"+str(self.id)+"/"+self.host+"/"+str(self.port) 
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            udp_socket.sendto(string.encode(), ("0.0.0.0", 54020))
            udp_socket.close()



def handle_tcp_received(conn, adrr):
    with conn:
        print(f"Conexão estabelecida com: {adrr}")


        while True:
            message = conn.recv(1024)
            if not message:
                break
            request_list = message.decode().split("/")
            #print("solicitação TCP recebida TCP recebida: ", message.decode())
            return request_list


def midleware_tcp_udp(tcp_host, tcp_port, udp_host, udp_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.bind((tcp_host,tcp_port))
        tcp_socket.listen(5)
        print(f"Aguardando conexões TCP em {tcp_host}:{tcp_port}...")

        while True:
            conn, addr = tcp_socket.accept()
            acess_data = handle_tcp_received(conn, addr)
            s = acess_data_base(acess_data)
            udp_return = json.dumps(s)
            if udp_return != []:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
                        udp_socket.sendto(udp_return.encode(), (udp_host, udp_port))
                        udp_socket.close()
                except socket.error as e:
                    try:
                        string = "Erro de soquete: "+str(e)
                        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
                            udp_socket.sendto(string.encode(), (udp_host, udp_port))
                            udp_socket.close()
                    except:
                        print("Erro de soquete:", e)
                except TimeoutError as e:
                    try:
                        string = "Erro de tempo: "+str(e)
                        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
                            udp_socket.sendto(string.encode(), (udp_host, udp_port))
                            udp_socket.close()
                    except:
                        print("Erro de tempo:", e)
                except OSError as e:
                    try:
                        string = "Erro de sistema operacional: "+str(e)
                        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
                            udp_socket.sendto(string.encode(), (udp_host, udp_port))
                            udp_socket.close()
                    except:
                        print("Erro de sistema operacional:", e)
                except Exception as e:
                    try:
                        string = "Outro erro: "+str(e)
                        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
                            udp_socket.sendto(string.encode(), (udp_host, udp_port))
                            udp_socket.close()
                    except:
                        print("Outro erro:", e)
                


    



def acess_data_base(data):
    dev = []
    match len(data):
        case 1:
            if data[0] == "air":
                dev = devices.air
            elif data[0] == "RGBlight":
                dev = devices.RGBlight
            elif data[0] == "door":
                dev = devices.door
            else:
                pass
        case 2:
            if data[0] == "air":
                dev = devices.air[int(data[1])-1]
            elif data[0] == "RGBlight":
                dev = devices.RGBlight[int(data[1])-1]
            elif data[0] == "door":
                dev = devices.door[int(data[1])-1]
            else:
                pass
        case 3:
            if data[0] == "air":
                devices.air[int(data[1])-1]['state'] = data[2]
                dev = devices.air[int(data[1])-1]
                DB_refactor()
            elif data[0] == "RGBlight":
                devices.RGBlight[int(data[1])-1]['state'] = data[2]
                dev = devices.RGBlight[int(data[1])-1]
                DB_refactor()
            elif data[0] == "door":
                devices.door[int(data[1])-1]['state'] = data[2]
                dev = devices.door[int(data[1])-1]
                DB_refactor()
                
            else:
                pass
        case 4:
            if data[0] == "air":
                if data[2] == "temperature":
                    devices.air[int(data[1])-1]['temperature'] = data[3]
                    dev = devices.air[int(data[1])-1]
                    DB_refactor()
                else:
                    pass
            elif data[0] == "RGBlight":
                if data[2] == "color":
                    devices.RGBlight[int(data[1])-1]['color'] = data[3]
                    dev = devices.RGBlight[int(data[1])-1]
                    DB_refactor()
                else:
                    pass    
            else:
                pass
    return dev
            
                
def DB_refactor():
    with open("devices.py", "w") as file:
        file.write("air = " + repr(devices.air) + "\n")
        file.write("RGBlight = " + repr(devices.RGBlight) + "\n")
        file.write("door = " + repr(devices.door) + "\n")

if __name__ == "__main__":
    TCP_HOST = '0.0.0.0'
    TCP_PORT = int(input("digite a porta TCP que deseja conectar"))

    UDP_HOST = '0.0.0.0'
    UDP_PORT = 54310
    
    type = str(input("Digite o tipo de dispositivo: "))
    id = int(input("digite o ID: "))
   
    d = device(type, id, TCP_HOST, TCP_PORT)
    d.initial_sendo()
    midleware_tcp_udp(TCP_HOST, TCP_PORT, UDP_HOST, UDP_PORT)