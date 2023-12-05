def armAll(udpout_connection_list):
    for connection in udpout_connection_list:
        connection.mav.sys_status_send(11, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

def disarmAll(udpout_connection_list):
    for connection in udpout_connection_list:
        connection.mav.sys_status_send(12, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

def takeOffAll(udpout_connection_list):
    for connection in udpout_connection_list:
        connection.mav.sys_status_send(13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

def landAll(udpout_connection_list):
    for connection in udpout_connection_list:
        connection.mav.sys_status_send(14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

def rtlAll(udpout_connection_list):
    for connection in udpout_connection_list:
        connection.mav.sys_status_send(15, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

def showAll(udpout_connection_list):
    for connection in udpout_connection_list:
        connection.mav.sys_status_send(16, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

def lightsAll(udpout_connection_list):
    for connection in udpout_connection_list:
        connection.mav.sys_status_send(17, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)



