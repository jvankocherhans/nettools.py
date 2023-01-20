import sqlite3

class DatabaseConection(object):

    __instance = None

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

    mConn = sqlite3.connect(mDBName)
    mCursor = mConn.cursor()
    
    def __new__(cls):
        if (cls.__instance is None):
            cls.__instance = super(DatabaseConection, cls).__new__(cls)
            cls.mCursor = cls.mConn.cursor()
            cls.__instance.__intialized = False
        return cls.__instance
        
    def getValue(self, deviceNagiosName, attribute):
        self.mCursor.execute(f"select {self.mDBAttributesDict[attribute]} from {self.mTableName} where {self.mDBAttributesDict['deviceNagiosName']} = '{deviceNagiosName}';")
        return self.mCursor.fetchone()[0]
    
    def closeConn(self):
        self.mConn.close()
        