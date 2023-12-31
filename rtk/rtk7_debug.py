import serial
from pymavlink import mavutil
from itertools import cycle

serial_port = serial.Serial('COM9', 57600)
the_connection_1 = mavutil.mavlink_connection('udpout:192.168.123.50:14555')

g_seq_no = cycle(range(32))
MAX_FRAGMENT_SIZE = 180

def encode(packet: bytes):
    if len(packet) > MAX_FRAGMENT_SIZE:
        
        # fragmented packet
        slices = [
            packet[i : (i + MAX_FRAGMENT_SIZE)]
            for i in range(0, len(packet), MAX_FRAGMENT_SIZE)
        ]

        # print(slices)

        if len(slices[-1]) == MAX_FRAGMENT_SIZE:
            # if the last fragment is full, we need to add an extra empty
            # one according to the protocol
            slices.append(b"")

        if len(slices) > 4:
            return

        seq_no = next(g_seq_no)

        for fragment_id, packet in enumerate(slices):
            flags = (seq_no << 3) + (fragment_id << 1) + 1
            the_connection_1.mav.gps_rtcm_data_send(flags, len(packet), packet.ljust(180, b"\x00"))
            
            # print(format(flags, '08b'))
            # print(packet)
            # combined_packet = b''
            # combined_packet += packet

        # print(combined_packet)


    else:
        # not fragmented packet
        the_connection_1.mav.gps_rtcm_data_send(0, len(packet), packet.ljust(180, b"\x00"))

while True:
    data = serial_port.readline()
    # print(data)
    encode(data)