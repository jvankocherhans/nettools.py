import time
import netmiko
import os

class NetworkSwitch:
    mCiscoSwitch = None
    mConn = None

    mCiscoSwitch = {
        "ip": "",
        "device_type": "cisco_ios",
        "username": "lidladm",
        "password": "lidladm"
    }

    # target attributes
    tSwitch = None
    tPort = None

    def updateCiscoSwitch(self,ip):
        self.mCiscoSwitch.update({"ip":f"{ip}"})
        self.mConn = netmiko.ConnectHandler(**self.mCiscoSwitch)

    def searchMacOnPort(self, ip, mac, port):
        if(self.mCiscoSwitch["ip"] != ip):
            self.updateCiscoSwitch(ip)

        output = self.mConn.send_command(f"show mac address-table interface {port} | include {mac}")
        
        if(len(output) > 0):

            if(output.split()[1] == mac):
                self.tSwitch = ip
                self.tPort = port
                return True
        
        return False
    
    def searchMacOnNet(self, mac):
        loop = True
        while(loop):
            mac_output = self.mConn.send_command(f"show mac address-table | inc {mac}")
            if(len(mac_output) > 0):
                if(mac_output != None):
                    print("yaa...")
                    cdp_output = self.mConn.send_command(f"show cdp neighbors {mac_output.split()[3]} | include Gig")
                    if(mac_output.split()[3] == ("".join(cdp_output.split()[0:2])).replace("g","")):
                        cdp_output = self.mConn.send_command(f"show cdp neighbors {mac_output.split()[3]} detail | include IP")
                        print(cdp_output)
                        self.updateCiscoSwitch(cdp_output.splitlines()[0].split()[2])
                    else:
                        print("YAAAAAA!!!")
                        print(("".join(cdp_output.split()[0:2])).replace("g",""))
                        print(mac_output.split()[3])
                        self.tPort = mac_output.split()[3]
                        loop = False
            else:
                loop = False

    def restartDevice(self):
        self.mConn.send_config_set([f"int {self.tPort}", "shut"])
        time.sleep(2)
        self.mConn.send_config_set([f"int {self.tPort}", "no shut"])

def isAlive(ip):
    for i in range(15):
        if(os.system(f"ping -c 1 {ip} > /dev/null") == 0):
            return True
    return False