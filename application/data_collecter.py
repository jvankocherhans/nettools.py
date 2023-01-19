import sqlite3

# member variables
mDBName = "poe-reboot.db"
mTableName = "device"

mDBAttributesDict = {
    "deviceNagiosName" : "lidl_deviceNagiosName",
    "deviceIp" : "lidl_deviceIp",
    "deviceMac" : "lidl_deviceMac",
    "deviceLocation" : "lidl_deviceLocation",
    "devicePort" : "lidl_devicePort",
    "switchNagiosName" : "lidl_switchNagiosName",
    "switchIp" : "lidl_switchIp"
}

# initialize db connection and create cursor
mConn = sqlite3.connect(mDBName)
mCursor = mConn.cursor()

def getValue(deviceNagiosName, attribute):
    mCursor.execute(f"select {mDBAttributesDict[attribute]} from {mTableName} where {mDBAttributesDict['deviceNagiosName']} = '{deviceNagiosName}';")
    return mCursor.fetchone()[0]

# mConn.close()
