import requests
import os
import threading
import ast



def get_end_broker():
    try:
        h = str(input("Digite o endereço IP do broker: "))
        return h
    except:
        print("Endereço invalido")
        get_end_broker()
    
base_url = "http://"+get_end_broker()+":9985"

class app:
    def __init__(self):
        self.rgb_len = 0
        self.air_len = 0
        self.door_len = 0

    def get_rgb_len(self):
        return self.rgb_len
    def get_air_len(self):
        return self.air_len
    def get_door_len(self):
        return self.door_len
    
    def set_rgb_len(self, val):
        self.rgb_len = val
    def set_air_len(self,val):
        self.air_len = val
    def set_door_len(self, val):
        self.door_len = val

def device_connect(string, device):
    try:
        dictio = string["data"]
        dictionary = ast.literal_eval(dictio)
        if len(dictionary['air']) > device.get_air_len():
            device.set_air_len(len(dictionary['air']))
            return "Novo dispositivo conectado: " + str(dictionary["air"][len(dictionary['air'])-1])
        if len(dictionary['RGBlight']) > device.get_rgb_len():
            device.set_rgb_len(len(dictionary['RGBlight']))
            return "Novo dispositivo conectado: " + str(dictionary["RGBlight"][len(dictionary['RGBlight'])-1])
        if len(dictionary['door']) > device.get_door_len():
            device.set_door_len(len(dictionary['door']))
            return "Novo dispositivo conectado: " + str(dictionary["door"][len(dictionary['door'])-1])
    except:
        pass

def response_received(device):
    response = requests.get(f"{base_url}/response")
    string = response.json()
    resp = device_connect(string, device)
    if resp != None:
        print(resp)
    threading.Timer(10,response_received, args=[device]).start()
    

def turn_on_air(id,state):
    change = {"state" : state}
    response = requests.patch(f"{base_url}/air/"+str(id)+"/on", json=change)
    handle_response(response)

def turn_off_air(id,state):
    change = {"state" : state}
    response = requests.patch(f"{base_url}/air/"+str(id)+"/off", json=change)
    handle_response(response)

def get_temp(id):
    response = requests.get(f"{base_url}/air/"+str(id)+"/temperature")
    handle_response(response)


def change_temp(id,temperature):
    change = {"temperature" : temperature}
    response = requests.patch(f"{base_url}/air/"+str(id)+"/temperature/"+str(temperature), json=change)
    handle_response(response)

def turn_on_RGBlight(id,state):
    change = {"state" : state}
    response = requests.patch(f"{base_url}/RGBlight/"+str(id)+"/on", json=change)
    handle_response(response)

def turn_off_RGBlight(id,state):
    change = {"state" : state}
    response = requests.patch(f"{base_url}/RGBlight/"+str(id)+"/off", json=change)
    handle_response(response)

def get_RGBlight(id):
    response = requests.get(f"{base_url}/RGBlight/"+str(id)+"/color")
    handle_response(response)

def change_RGBlight(id,color):
    change = {"color" : color}
    response = requests.patch(f"{base_url}/RGBlight/"+str(id)+"/color/"+color, json=change)
    handle_response(response)

def open_door(id,state):
    change = {"state" : state}
    response = requests.patch(f"{base_url}/door/"+str(id)+"/open", json=change)
    handle_response(response)

def close_door(id,state):
    change = {"state" : state}
    response = requests.patch(f"{base_url}/door/"+str(id)+"/close", json=change)
    handle_response(response)


def handle_response(response):
    if response.status_code == 200:
        data = response.json()
        if "status" in data and data["status"] == "success":
            print("Operação bem-sucedida!")
            if "data" in data:
                print("Dados retornados:", data["data"])
        else:
            print("Falha na operação:", data["message"])
    else:
        print("Falha na requisição. Código de status:", response.status_code)


def app_machine():
    print("Controle IoT")
    print("Escolha o dispositivo:")
    print("1 - Ar condicionado")
    print("2 - Lampada RGB")
    print("3 - Porta")

    i = int(input("Digite o numero da opção que deseja selecionar: "))

    match i:
        case 1:
            print("1 - Ligar")
            print("2 - Desligar")
            print("3 - Obter temperatura")
            print("4 - Alterar temperatura")
            j = int(input("Digite o numero da opção que deseja selecionar: "))
            match j:
                case 1:
                    id = int(input("Digite o id do dispostivo: "))
                    turn_on_air(id,"on")
                    return
                case 2:
                    id = int(input("Digite o id do dispostivo: "))
                    turn_off_air(id,"off")
                    return
                case 3:
                    id = int(input("Digite o id do dispostivo: "))
                    get_temp(id)
                    return
                case 4:
                    id = int(input("Digite o id do dispostivo: "))
                    temp = int(input("Digite a temperatura: "))
                    change_temp(id,temp)
                    return
                case _:
                     print("Opção invalida")
                     return
        case 2:
            print("1 - Ligar")
            print("2 - Desligar")
            print("3 - Cor atual")
            print("4 - Alterar cor")
            j = int(input("Digite o numero da opção que deseja selecionar: "))
            match j:
                case 1:
                    id = int(input("Digite o id do dispostivo: "))
                    turn_on_RGBlight(id,"on")
                    return
                case 2:
                    id = int(input("Digite o id do dispostivo: "))
                    turn_off_RGBlight(id,"off")
                    return
                case 3:
                    id = int(input("Digite o id do dispostivo: "))
                    get_RGBlight(id)
                    return
                case 4:
                    id = int(input("Digite o id do dispostivo: "))
                    color = str(input("Digite a cor: "))
                    change_RGBlight(id,color)
                    return
                case _:
                     print("Opção invalida")
                     return
        case 3:
            print("1 - Abrir portão")
            print("2 - Fechar portão")
            j = int(input("Digite o numero da opção que deseja selecionar: "))
            match j:
                case 1:
                    id = int(input("Digite o id do dispostivo: "))
                    open_door(id,"open")
                    return
                case 2:
                    id = int(input("Digite o id do dispostivo: "))
                    close_door(id,"close")
                    return
                case _:
                     print("Opção invalida")
                     return
        case _:
            print("Opção invalida")
            return
        

def execute():
    try:
        while True:
            app_machine()
    except:
        print("A aplicação não conseguiu se conectar ao servidor. Reconete-se")
        print("Digite 1 para tentar a reconexão ou qualquer outra tecla para encerrar a aplicação") 
        x = int(input("Escolha a opção:"))
        if x == 1:
            return execute()
        else:
            print("Encerrando a aplicação....")
            os._exit()


if __name__ == "__main__":
    device = app()
    response_received(device)
    execute()
        
