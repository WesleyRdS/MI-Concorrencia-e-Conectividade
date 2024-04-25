from flask import Flask, make_response, request, jsonify
import socket
import devices
import socket

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

topic_queue = {}


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
    try:
        tcp = TCP_SEND("127.0.0.1", 3000)
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
        tcp = TCP_SEND("127.0.0.1", 3000)
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
        tcp = TCP_SEND("127.0.0.1", 3000)
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
        tcp = TCP_SEND("127.0.0.1", 3000)
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
        tcp = TCP_SEND("127.0.0.1", 3000)
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
        tcp = TCP_SEND("127.0.0.1", 3000)
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
        tcp = TCP_SEND("127.0.0.1", 3000)
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
        tcp = TCP_SEND("127.0.0.1", 3000)
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
        tcp = TCP_SEND("127.0.0.1", 3000)
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
        tcp = TCP_SEND("127.0.0.1", 3000)
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
        tcp = TCP_SEND("127.0.0.1", 3000)
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
        tcp = TCP_SEND("127.0.0.1", 3000)
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
        tcp = TCP_SEND("127.0.0.1", 3000)
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
        tcp = TCP_SEND("127.0.0.1", 3000)
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
    app.run(debug=True)