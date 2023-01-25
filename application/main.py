import mac_reboot_algorithm
import data_collecter

# object instances
switch = mac_reboot_algorithm.NetworkSwitch()
switch2 = mac_reboot_algorithm.NetworkSwitch()
database = data_collecter.DatabaseConection()

input = "host01"

mac = database.getValue(input, "deviceMac")
ip = database.getValue(input, "switchIp")
port = database.getValue(input, "devicePort")

if(switch.searchMacOnPort(ip, mac, port) or switch.searchMacOnNet(ip, mac)):
       database.updateValue(input, switch.tPort, switch.tSwitchName, switch.tSwitchIp)
else:
    switch.tPort = port
    switch.tSwitch = ip

switch.restartDevice()

if(mac_reboot_algorithm.isAlive(database.getValue(input, "deviceIp"))):
         print("success")