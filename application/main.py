import mac_reboot_algorithm
import data_collecter

input = "host01"

# print(data_collecter.getValue(input, "deviceMac"))

switch = mac_reboot_algorithm.NetworkSwitch()

switch.updateCiscoSwitch("192.168.19.8")

print(switch.getIp())