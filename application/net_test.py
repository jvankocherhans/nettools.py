import time
import netmiko
import os

username = "lidladm"
password = "lidladm"
ip = "192.168.19.8"
device_type = "cisco_ios"
core_switch_ip = "192.168.19.5"

cmd = ["conf t", "int gig 2/0", "no shutdown"]

connection = netmiko.ConnectHandler(ip=ip, device_type=device_type, username=username, password=password)

a = connection.send_config_set(cmd)


output = connection.send_command("show cdp neighbors Gi 0/0 detail | inc IP")

print(output.splitlines()[0].split()[2])
