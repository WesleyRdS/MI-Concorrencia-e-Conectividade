import socket


import threading
import random
import os
import sys

UDP_HOST = os.getenv("UDP_HOST")
TCP_HOST = os.getenv("TCP_HOST")

class device:
    def __init__(self,type, id, host, port) -> None:
        self.type = type
        self.id = id
        self.host = host
        self.port = port
        self.status = ""
        self.data = None
        self.par = ""
    
    def set_initial_params(self):
        if self.type == "air" or self.type == "RGBlight":
            l = ['on', "off"]
            self.status = random.choice(l)
        else:
            l = ['open', "close"]
            self.status = random.choice(l)
        
        if self.type == "air":
            self.data = random.randint(10,35)
            self.par = "Temperatura"
        else:
            l = ['azul', "vermelho","amarelo","verde","branca","violeta","ametista","laranja","azul"]
            self.data = random.choice(l)
            self.par = "Cor da luz"

    def get_par(self):
        return self.par
    
    def set_par(self, i):
        self.par = i
    
    def get_status(self):
        return self.status
    
    def set_status(self, i):
        self.status = i
    
    def get_data(self):
        return self.data

    def set_data(self, i):
        if self.type == "air":
            self.data = i   
        elif self.type == "RGBlight":
            self.data = i 
        else:
            pass

    def initial_sendo(self,s):
        string = self.type+"/"+str(self.id)+"/"+self.host+"/"+str(self.port) 
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            udp_socket.sendto(string.encode(), (s, 54020))
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


def midleware_tcp_udp(tcp_host, tcp_port, udp_host, udp_port, device):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        try:
            tcp_socket.bind((tcp_host,tcp_port))
            tcp_socket.listen(5)
            print(f"Aguardando conexões TCP em {tcp_host}:{tcp_port}...")

            while True:
                conn, addr = tcp_socket.accept()
                acess_data = handle_tcp_received(conn, addr)
                s = acess_data_base(acess_data,device)
                udp_return = str(s)
                if s != []:
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
        except:
            string = "O dispositivo falhou em se conectar. A porta informada ja esta sendo ultilizada"
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
                udp_socket.sendto(string.encode(), (udp_host, udp_port))
                udp_socket.close()
                


    



def acess_data_base(data,device):
    dev = []
    match len(data):
        case 1:
            if device.get_status() != "off":
                dev = device.get_data()
            else:
                dev = "Dispositivo desligado"
        case 2:
            if device.get_status() != "off":
                dev = device.get_data()
            else:
                dev = "Dispositivo desligado"
        case 3:
            device.set_status(data[2])
            if device.get_status() == data[2]:
                dev = "Status do dispositivo: " + device.get_status()
            else:
                dev = "Falha na operação."
        case 4:
            if device.get_status() != "off":
                aux = str(device.get_data())
                device.set_data(data[3])
                if str(device.get_data()) == str(data[3]):
                    dev = "Alteração do parâmetro -" + device.get_par() + "- de: " + aux + " - Para: " + str(device.get_data())
                else:
                    dev = "Falha na operação."
            else:
                dev = "Dispositivo desligado"        
        case _:
            dev = "A função passada não esta definida no sitema"
    return dev

def interface(device):
    print("1 - Para mudar o status do dispositivo")
    print("2 - Para mudar seus dados")
    j = int(input("Digite o numero da opção que deseja selecionar: "))
    match j:
        case 1:
            if device.get_status() == "on":
                device.set_status("off")
                print("Status: "+device.get_status())
            elif device.get_status() == "off":
                device.set_status("on")
                print("Status: "+device.get_status())
            elif device.get_status() == "open":
                device.set_status("close")
                print("Status: "+device.get_status())
            elif device.get_status() == "close":
                device.set_status("open")
                print("Status: "+device.get_status())
            else:
                pass
            return
        case 2:
            if device.type == "air":
                i = int(input("Digite a temperatura desejada: "))
                device.set_data(str(i))
            elif device.type == "RGBlight":
                i = str(input("Digite a cor desejada: "))
                device.set_data(i)
            else:
                pass
            return
        case _:
            return
    
def restart():
    exe = sys.executable
    os.execl(exe, exe, *sys.argv)

if __name__ == "__main__":
    try:
        TCP_PORT = int(input("digite a porta TCP que deseja conectar: "))
    except:
        print("Porta invalida. Reiniciando a aplicação....")
        restart()

    UDP_PORT = 54310
    t_devices = ["air", "RGBlight", "door"]
    type = str(input("Digite o tipo de dispositivo: "))
    if type in t_devices:
        try:
            id = int(input("digite o ID: "))
        except:
            print("ID invalido. Reiniciando a aplicação..")
            restart()
    
        d = device(type, id, TCP_HOST, TCP_PORT)
        d.set_initial_params()
        d.initial_sendo(UDP_HOST)
        thr = threading.Thread(target=midleware_tcp_udp, args=(TCP_HOST, TCP_PORT, UDP_HOST, UDP_PORT,d))
        thr.start()
        while True:
            interface(d)
    else:
        string = "Dispositivo invalido"
        print(string)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            udp_socket.sendto(string.encode(), (UDP_HOST, UDP_PORT))
            udp_socket.close()
     
        