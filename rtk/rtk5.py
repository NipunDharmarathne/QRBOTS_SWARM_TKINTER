from pymavlink import mavutil

the_connection_1 = mavutil.mavlink_connection('udpout:192.168.123.50:14555')

raw_data = b'\x01\x02\x03\x04'
raw_data_len = len(raw_data)
raw_data = raw_data + b'\x00' * (180 - raw_data_len)

# print(len(gps_data))
# print(gps_data)
# the_connection_1.mav.gps_inject_data_send(1, 1, len(gps_data), gps_data)
the_connection_1.mav.gps_rtcm_data_send(0, raw_data_len, raw_data)

# # Example RTK data (replace with your own RTK data)
# rtk_data = b'\x01\x02\x03\x04'  # Replace with your RTCM data

# # Send the GPS_RTCM_DATA message
# the_connection_1.mav.gps_rtcm_data_send(1, rtk_data)



# connection_string = '/dev/ttyUSB0'  # or 'udp:127.0.0.1:14550' for example
# baud_rate = 57600

# # Create a MAVLink connection
# master = mavutil.mavlink_connection(connection_string, baud=baud_rate)

# # Example GPS data (replace this with your actual data)
# gps_data = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x10'

# # Send the GPS_INJECT_DATA message
# master.mav.gps_inject_data_send(1, mavutil.mavlink.MAV_COMP_ID_GPS, len(gps_data), gps_data)

# # Close the MAVLink connection
# master.close()
