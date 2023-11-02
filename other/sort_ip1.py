# source_ip_list = ['192.168.123.51', '192.168.123.50', '192.168.123.53', '192.168.123.52']
# print(source_ip_list)

# def sort(source_ip_list):    
#     source_ip_list = sorted(source_ip_list, key=lambda x: (int(x.split('.')[-1]), x))
#     print(source_ip_list)

# sort(source_ip_list)
# print(source_ip_list)

source_ip_list = ['192.168.123.51', '192.168.123.50', '192.168.123.53', '192.168.123.52']
print(source_ip_list)

def sort_source_ip_list():
    global source_ip_list
    source_ip_list = sorted(source_ip_list, key=lambda x: (int(x.split('.')[-1]), x))
    print(source_ip_list)

sort_source_ip_list()
print(source_ip_list)
