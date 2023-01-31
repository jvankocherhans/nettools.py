import random
from flask import Flask, render_template, request, url_for
import data_collecter
from threading import Thread, Lock
import mac_reboot_algorithm

app = Flask(__name__)
database = data_collecter.DatabaseConection()
switch = mac_reboot_algorithm.NetworkSwitch()
devices = database.getValues("deviceNagiosName")
reboot_process_list = []

def reboot(input):

    mac = database.getValue(input, "deviceMac")
    ip = database.getValue(input, "switchIp")
    port = database.getValue(input, "devicePort")

    if (switch.searchMacOnPort(ip, mac, port) or switch.searchMacOnNet(ip, mac)):
        database.updateValue(input, switch.tPort,
        switch.tSwitchName, switch.tSwitchIp)
    else:
        switch.tPort = port
        switch.tSwitch = ip

    switch.restartDevice()

    if (mac_reboot_algorithm.isAlive(database.getValue(input, "deviceIp"))):
        print("success")

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/poe-reboot", methods=["POST", "GET"])
def poeReboot():
    if(request.method == "POST"):

        reboot_process = Thread(target=reboot, args=(request.form.get("devices"),))
        reboot_process.start()
        reboot_process_list.append(reboot_process)

        for i in reboot_process_list:
            if(not i.is_alive()):
                reboot_process_list.remove(i)

        return render_template("poe-reboot.html", devices=devices, reboot_process_list=reboot_process_list)
    else:

        for i in reboot_process_list:
            if(not i.is_alive()):
                reboot_process_list.remove(i)

        return render_template("poe-reboot.html", devices=devices, reboot_process_list=reboot_process_list)

if __name__ == "__main__":
    app.run(debug=True, port=55555)