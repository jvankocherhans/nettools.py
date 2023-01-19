import netmiko

username = "lidladm"
password = "lidladm"
ip = "192.168.19.5"
device_type = "cisco_ios"
core_switch_ip = "192.168.19.5"

cmd = ["conf t", "int gig 2/0", "no shutdown"]

connection = netmiko.ConnectHandler(ip=ip, device_type=device_type, username=username, password=password)

a = connection.send_config_set(cmd)

