import requests

base_url = "http://localhost:5000"

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
        

if __name__ == "__main__":
    while True:
        app_machine()