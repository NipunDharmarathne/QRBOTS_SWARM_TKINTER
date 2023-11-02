source_ip_list = ['192.168.123.51', '192.168.123.50', '192.168.123.53', '192.168.123.52']
source_ip_list = sorted(source_ip_list, key=lambda x: (int(x.split('.')[-1]), x))
print(source_ip_list)