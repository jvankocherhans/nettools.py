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
    tSwitchIp = None
    tSwitchName = None
    tPort = None

    def updateCiscoSwitch(self):
        self.mCiscoSwitch.update({"ip":f"{self.tSwitchIp}"})
        self.mConn = netmiko.ConnectHandler(**self.mCiscoSwitch)

    def searchMacOnPort(self, ip, mac, port):
        if(self.mCiscoSwitch["ip"] != ip):
            self.tSwitchIp = ip
            self.updateCiscoSwitch()

        mac_output = self.mConn.send_command(f"show mac address-table interface {port} | include {mac}")
        
        if(len(mac_output) > 0):

            if(mac_output.split()[1] == mac):
                self.tSwitchName = self.getHostname()
                self.tPort = port
                return True
        
        return False
    
    def searchMacOnNet(self, ip, mac):
        loop = True

        if(self.mCiscoSwitch["ip"] != ip):
            self.tSwitchIp = ip
            self.updateCiscoSwitch()

        while(loop):
            mac_output = self.mConn.send_command(f"show mac address-table | inc {mac}")
            if(len(mac_output) > 0):
                self.tPort = mac_output.split()[3]
                if(mac_output != None):
                    cdp_output = self.mConn.send_command(f"show cdp neighbors {self.tPort} | inc Gig")
                    if(self.tPort == ("".join(cdp_output.split()[0:2])).replace("g","")):
                        cdp_output = self.mConn.send_command(f"show cdp neighbors {self.tPort} detail | inc IP")
                        self.tSwitchIp = cdp_output.splitlines()[0].split()[2]
                        self.updateCiscoSwitch()
                    else:
                        self.tSwitchName = self.getHostname()
                        loop = False
                        return True
            else:
                loop = False
                return False
            
    def getHostname(self):
        hostname_output = self.mConn.send_command("show running-config | inc hostname")
        return hostname_output.split()[1]

    def restartDevice(self):
        self.mConn.send_config_set([f"int {self.tPort}", "shut"])
        time.sleep(2)
        self.mConn.send_config_set([f"int {self.tPort}", "no shut"])

def isAlive(ip):
    for i in range(15):
        time.sleep(2)
        if(os.system(f"ping -c 1 {ip} > /dev/null") == 0):
            return True
    return False