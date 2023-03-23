import random
from flask import Flask, render_template, request, url_for, Response
import data_collecter
from threading import Thread, Lock
import mac_reboot_algorithm
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
socketio = SocketIO(app)
switch = mac_reboot_algorithm.NetworkSwitch()
database = data_collecter.DatabaseConection()
devices = database.getValues("deviceNagiosName")
reboot_object_list = []
reboot_process_list = []

def reboot(input):

    switch.tDeviceName = input

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
        switch.mProcessInfo = "success"
        time.sleep(2)
        switch.mProcessInfo = None


@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route('/submit', methods=['POST'])
def submit():
    return render_template('dashboard.html')

@app.route("/poe-reboot", methods=["POST", "GET"])
def poeReboot():
    if(request.method == "POST"):

        reboot_process = Thread(target=reboot, args=(request.form.get("devices"),))
        reboot_process.start()

        return render_template("poe-reboot.html", devices=devices, reboot_process_list=reboot_process_list)
    else:
        print()

        return render_template("poe-reboot.html", devices=devices, reboot_process_list=reboot_process_list)

@socketio.on('request_value')
def send_value():
    emit('value', switch.mProcessInfo) 

if __name__ == '__main__':
    socketio.run(app, port=55555, debug=True)