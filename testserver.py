import socket
from json import load as load_json
from time import sleep

with open('config.json') as cf:
    config = load_json(cf)

HOST = config["socket"]["host"]
PORT2SERVER = config["socket"]["port1"]
PORT2DATA = config["socket"]["port2"]
s_new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s_new.connect((HOST, PORT2DATA))
    except ConnectionRefusedError:
        # wait till controller is ready
        sleep( 1 )
        continue
    else:
        break

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT2SERVER))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('1 Connected by', addr)
            data = conn.recv(config["socket"]["buffer_size"])
            print(data)
            r_data = data.split(b' ')
            #print(r_data)
            if r_data[0] == b'addDevice':
                req = (b'addDeviceResponse ' + r_data[1] + b';OK')
            else:
                req = (b'addDeviceResponse ' + r_data[1] + b';ERROR')
            s_new.sendall(req)

            sleep(2)

            setupinforeq = (b'deviceSetupInfo ' + r_data[1] + b';BRIGHTNESS')
            s_new.sendall(setupinforeq)
            print("GESENDET ALTER")

            sleep(2)

            for i in range(5):
                deviceData = (b'deviceData ' + r_data[1] + b';134')
                s_new.sendall(deviceData)
                print("Device Data sent")
                sleep(1)




