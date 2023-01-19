import netmiko

class NetworkSwitch:
    mCiscoSwitch = None
    mCORE_SWITCH = "192.168.19.5"
    mCiscoSwitch = {
    "ip": "",
    "device_type": "cisco_ios",
    "username": "lidladm",
    "password": "lidladm"
    }

    def updateCiscoSwitch(self,ip):
        NetworkSwitch.mCiscoSwitch.update({"ip":f"{ip}"})
        NetworkSwitch.mConn = netmiko.ConnectHandler(**NetworkSwitch.mCiscoSwitch)

    def searchMacOnPort():
        pass

    def getIp(self):
        return NetworkSwitch.mConn.send_command("show version | include switch")

