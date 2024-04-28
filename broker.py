from flask import Flask, make_response, request, jsonify
import socket
import threading
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

topic_queue = {}
devices_connections_air = []
devices_connections_rgb = []
devices_connections_door = []

class TCP_SEND:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.connected = False


    def connect(self):
        if not self.connected:
            try:
                self.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket_tcp.connect((self.host, self.port))
                self.connected = True
                print("Conectado ao servidor de dispositivos")
            except Exception as e:
                print("Erro ao conectar: ", str(e))

    def send_request(self,message):
        if self.connected:
            self.socket_tcp.sendall(message.encode())

def udp_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
        udp.bind((host, port))

        print(f"Conexão temporaria estabelecida com: {host}:{port}")
        while True:
            device_info, device_server_adress = udp.recvfrom(1024)
            if device_info:
                return device_info.decode()
                
def connect_continuos(host, port):
    global devices_connections_air
    global devices_connections_door
    global devices_connections_rgb
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
        udp.bind((host, port))

        print(f"Conexão temporaria estabelecida com: {host}:{port}")
        while True:
            device_info, device_server_adress = udp.recvfrom(1024)
            if device_info:
                string = device_info.decode().split("/")
                match string[0]:
                    case "air":
                        global devices_connections_air
                        DB_refactor(string, devices_connections_air)
                    case "RGBlight":
                        global devices_connections_door
                        DB_refactor(string, devices_connections_rgb)
                    case "door":
                        global devices_connections_door
                        DB_refactor(string, devices_connections_door)
                    case _:
                        pass   
                dados = {
                    "air": devices_connections_air,
                    "RGBlight": devices_connections_rgb,
                    "door": devices_connections_door
                }

                with open("connections.json", "w") as file:
                     json.dump(dados, file)
               




def DB_refactor(lt, devices_connections):
    if len(devices_connections) != 0:
        match lt[0]:
            case "air":
                for i in devices_connections:
                    if i[1] == lt[1]:
                        return
                    devices_connections.append(lt)
                        
            case "RGBlight":
                for i in devices_connections:
                    if i[1] == lt[1]:
                        return
                    devices_connections.append(lt)
            case "door":
                for i in devices_connections:
                    if i[1] == lt[1]:
                        return
                    devices_connections.append(lt) 
            case _:
                pass
    else:
        devices_connections.append(lt)




def get_port_by_id(type, id, dev):
    ip = []
    print(dev)
    match type:
        case "air":
            for i in dev:
                if i[1] == id:
                    ip.append(i[2])
                    ip.append(int(i[3]))
                    return ip
             
        case "RGBlight":
            for i in dev:
                if i[1] == id:
                    ip.append(i[2])
                    ip.append(int(i[3]))
                    return ip

        case "door":
            for i in dev:
                print(i)
                if i[1] == id:
                    ip.append(i[2])
                    ip.append(int(i[3]))
                    return ip
        case _:
            print("dsfs")

def ler_json():
    with open('connections.json', 'r') as file:
    # Carregar o conteúdo do arquivo em uma lista Python
        lista_rgb = json.load(file)
    
    return lista_rgb


def success_response(data=None):
    if data:
        return jsonify({"status": "success", "data": data}), 200
    else:
        return jsonify({"status": "success"}), 200

def error_response(message):
    return jsonify({"status": "error", "message": message}), 400



@app.route("/<string:topic>", methods=['PUT', 'GET'])
def request_received(topic):
    if topic not in topic_queue:
        topic_queue[topic]  = []

    topic_queue[topic].append(request.json)
    print(topic_queue[topic])

    return jsonify({"mensagem" : "Solicitação recebida com sucesso"}), 200



@app.route("/RGBlight/<id>/color", methods=['GET'])
def get_rgb_id(id):
    v = []
    try:
        vector = ler_json()
        v = get_port_by_id("RGBlight", str(id), vector["RGBlight"])
        tcp = TCP_SEND(v[0], v[1])
        tcp.connect()
        tcp.send_request("RGBlight/"+str(id))
        try:
            udp_message = udp_server("127.0.0.1", 54310)
            return success_response(udp_message)
        except:
            return error_response()
    except IndexError:
        return error_response("ID do dispositivo inválido")

@app.route("/door/<id>", methods=['GET'])
def get_door_id(id):
    try:
        vector = ler_json()
        v = get_port_by_id("door", str(id), vector["door"])
        tcp = TCP_SEND(v[0], v[1])
        tcp.connect()
        tcp.send_request("door/"+str(id))
        try:
            udp_message = udp_server("127.0.0.1", 54310)
            return success_response(udp_message)
        except:
            return error_response()
    except IndexError:
        return error_response("ID do dispositivo inválido")

@app.route("/air/<id>/temperature", methods=['GET'])
def get_air_id(id):
    try:
        vector = ler_json()
        v = get_port_by_id("air", str(id), vector["air"])
        tcp = TCP_SEND(v[0], v[1])
        tcp.connect()
        tcp.send_request("air/"+str(id))
        try:
            udp_message = udp_server("127.0.0.1", 54310)
            return success_response(udp_message)
        except:
            return error_response()
    except IndexError:
        return error_response("ID do dispositivo inválido")

@app.route("/RGBlight", methods=['GET'])
def get_rgb():
    try:
        vector = ler_json()
        v = get_port_by_id("RGBlight", str(id), vector["RGBlight"])
        tcp = TCP_SEND(v[0], v[1])
        tcp.connect()
        tcp.send_request("RGBlight")
        try:
            udp_message = udp_server("127.0.0.1", 54310)
            return success_response(udp_message)
        except:
            return error_response()
    except IndexError:
        return error_response("ID do dispositivo inválido")

@app.route("/door", methods=['GET'])
def get_door():
    try:
        vector = ler_json()
        v = get_port_by_id("door", str(id), vector["door"])
        tcp = TCP_SEND(v[0], v[1])
        tcp.connect()
        tcp.send_request("door")
        try:
            udp_message = udp_server("127.0.0.1", 54310)
            return success_response(udp_message)
        except:
            return error_response()
    except IndexError:
        return error_response("ID do dispositivo inválido")

@app.route("/air", methods=['GET'])
def get_air():
    try:
        vector = ler_json()
        v = get_port_by_id("air", str(id), vector["air"])
        tcp = TCP_SEND(v[0], v[1])
        tcp.connect()
        tcp.send_request("air")
        try:
            udp_message = udp_server("127.0.0.1", 54310)
            return success_response(udp_message)
        except:
            return error_response()
    except IndexError:
        return error_response("ID do dispositivo inválido")


@app.route("/air/<id>/<on>", methods=['PATCH'])
def patch_air_on(id,on):
    try:
        vector = ler_json()
        v = get_port_by_id("air", str(id), vector["air"])
        tcp = TCP_SEND(v[0], v[1])
        tcp.connect()
        tcp.send_request("air/"+str(id)+"/"+str(on))

        try:
            udp_message = udp_server("127.0.0.1", 54310)
            return success_response(udp_message)
        except:
            return error_response()
    except IndexError:
        return error_response("ID do dispositivo inválido")

@app.route("/air/<id>/<off>", methods=['PATCH'])
def patch_air_off(id,off):
    try:
        vector = ler_json()
        v = get_port_by_id("air", str(id), vector["air"])
        tcp = TCP_SEND(v[0], v[1])
        tcp.connect()
        tcp.send_request("air/"+str(id)+"/"+str(off))

        try:
            udp_message = udp_server("127.0.0.1", 54310)
            return success_response(udp_message)
        except:
            return error_response()
    except IndexError:
        return error_response("ID do dispositivo inválido")


@app.route("/air/<id>/temperature/<temperature>", methods=['PATCH'])
def patch_air_change_temperature(id,temperature):
    try:
        vector = ler_json()
        v = get_port_by_id("air", str(id), vector["air"])
        tcp = TCP_SEND(v[0], v[1])
        tcp.connect()
        tcp.send_request("air/"+str(id)+"/temperature/"+str(temperature))

        try:
            udp_message = udp_server("127.0.0.1", 54310)
            return success_response(udp_message)
        except:
            return error_response()
    except IndexError:
        return error_response("ID do dispositivo inválido")


@app.route("/RGBlight/<id>/<on>", methods=['PATCH'])
def patch_RGB_on(id,on):
    try:
        vector = ler_json()
        v = get_port_by_id("RGBlight", str(id), vector["RGBlight"])
        tcp = TCP_SEND(v[0], v[1])
        tcp.connect()
        tcp.send_request("RGBlight/"+str(id)+"/"+str(on))

        try:
            udp_message = udp_server("127.0.0.1", 54310)
            return success_response(udp_message)
        except:
            return error_response()
    except IndexError:
        return error_response("ID do dispositivo inválido")
        


@app.route("/RGBlight/<id>/<off>", methods=['PATCH'])
def patch_RGB_off(id,off):
    try:
        vector = ler_json()
        v = get_port_by_id("RGBlight", str(id), vector["RGBlight"])
        tcp = TCP_SEND(v[0], v[1])
        tcp.connect()
        tcp.send_request("RGBlight/"+str(id)+"/"+str(off))

        try:
            udp_message = udp_server("127.0.0.1", 54310)
            return success_response(udp_message)
        except:
            return error_response()
    except IndexError:
        return error_response("ID do dispositivo inválido")


@app.route("/RGBlight/<id>/color/<color>", methods=['PATCH'])
def patch_change_RGBlight(id,color):
    try:
        vector = ler_json()
        v = get_port_by_id("RGBlight", str(id), vector["RGBlight"])
        tcp = TCP_SEND(v[0], v[1])
        tcp.connect()
        tcp.send_request("RGBlight/"+str(id)+"/color/"+str(color))

        try:
            udp_message = udp_server("127.0.0.1", 54310)
            return success_response(udp_message)
        except:
            return error_response()
    except IndexError:
        return error_response("ID do dispositivo inválido")


@app.route("/door/<id>/<op>", methods=['PATCH'])
def patch_open_door(id,op):
    try:
        vector = ler_json()
        v = get_port_by_id("door", str(id), vector["door"])
        tcp = TCP_SEND(v[0], v[1])
        tcp.connect()
        tcp.send_request("door/"+str(id)+"/"+str(op))

        try:
            udp_message = udp_server("127.0.0.1", 54310)
            return success_response(udp_message)
        except:
            return error_response()
    except IndexError:
        return error_response("ID do dispositivo inválido")

@app.route("/door/<id>/<cls>", methods=['PATCH'])
def patch_close_door(id,cls):
    try:
        vector = ler_json()
        v = get_port_by_id("door", str(id), vector["door"])
        tcp = TCP_SEND(v[0], v[1])
        tcp.connect()
        tcp.send_request("door/"+str(id)+"/"+str(cls))

        try:
            udp_message = udp_server("127.0.0.1", 54310)
            return success_response(udp_message)
        except:
            return error_response()
    except IndexError:
        return error_response("ID do dispositivo inválido")



def rout_request(topic, device_ip, device_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((device_ip,device_port))

        s.sendall(str(topic_queue[topic].encode('utf-8')))

        response = s.recv(1024).decode('utf-8')

        return response
    

if __name__ == "__main__":
    thr = threading.Thread(target=connect_continuos, args=("127.0.0.1", 54020))
    thr.start()
    app.run(debug=True)