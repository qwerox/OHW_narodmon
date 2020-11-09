
from datetime import datetime
import socket
import wmi
import json


NAME = socket.gethostname().replace('-', '_')

login_in_narodmon = 'you_login' #укажите свой логин на сайте narodmon.ru
#NAME = 'One' # тут можно указать имя компьютера вручную
now = str(datetime.now())
hwmon = wmi.WMI(namespace="root\OpenHardwareMonitor")

sensors_t = hwmon.Sensor()
sensor_list = []
data_dict = {}
json_send_narodmon = {}
#data_dict['time'] = str(datetime.utcnow())
for sensor in sensors_t:

    k = sensor.Identifier.split('/')
    #print(k)
    if 'intelcpu'  in k and 'temperature'  in k and k[-1] == '0' in k:
        data_dict[sensor.Identifier] = round(float(sensor.Value), 2)
    if 'intelcpu'  in k and 'load'  in k and k[-1] == '0' in k:
        data_dict[sensor.Identifier] = round(float(sensor.Value), 2)
    if 'amdcpu'  in k and 'temperature'  in k and k[-1] == '0' in k:
        data_dict[sensor.Identifier] = round(float(sensor.Value), 2)
    if 'amdcpu'  in k and 'load'  in k and k[-1] == '0' in k:
        data_dict[sensor.Identifier] = round(float(sensor.Value), 2)
    if 'nvidiagpu'  in k and 'temperature'  in k and k[-1] == '0' in k:
        data_dict[sensor.Identifier] = round(float(sensor.Value), 2)
    if 'ram' in k and 'data' in k:
        data_dict[sensor.Identifier] = round(float(sensor.Value), 2)
    if 'atigpu'  in k and 'temperature'  in k and k[-1] == '0' in k:
        data_dict[sensor.Identifier] = round(float(sensor.Value), 2)



# удаляем ненужные 0 в пакете заголовков
metrics = list(data_dict.keys())
for key in metrics:
    data = data_dict[key]
    data_dict.pop(key)
    key = key.replace('/', '_')
    key = key.replace('temperature', 't')
    key = key[key.find('_') + 1:]
    data_dict[key] = data
# формируем пакет для отправки
data_send = {}
data_send['owner'] = login_in_narodmon
data_send['mac'] = NAME + '_telemetry_narodmon'
#data_send['key'] = 'mt123'
for key in data_dict:
    sensor_list.append({"id": key, "value": data_dict[key]})
data_send['sensors'] = sensor_list

json_send_narodmon['devices'] = [data_send]
json_send = json.dumps(json_send_narodmon, sort_keys=True) + "\n"
print(json_send)

#exit()
# работа с сокетом

conn = socket.socket()
conn.settimeout(10)
serv_addr = "narodmon.com"
conn.connect((serv_addr, 8283))
conn.send(json_send.encode('utf-8'))
tmp = conn.recv(1024)
data = b''
while tmp:
    data += tmp
    tmp = conn.recv(1024)
print(data.decode("utf-8"))
conn.close()





