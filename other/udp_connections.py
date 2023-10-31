from pymavlink import mavutil

source_ip_list = ['192.168.123.51', '192.168.123.50']
connections = []

for source_ip in source_ip_list:
    connection = mavutil.mavlink_connection('udpout:' + source_ip + ':14555')
    connections.append(connection)
    print(f"Connected to {source_ip}")


for connection in connections:
    connection.mav.system_time_send(1, 1)
