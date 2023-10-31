source_ip_list = ['192.168.123.51', '192.168.123.50']
label_text = ""

for ip in source_ip_list:
    label_text += ip + "\n"

# Remove the trailing space if needed
label_text = label_text.strip()

print(label_text)