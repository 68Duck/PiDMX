import sqlite3 as lite
from os import path
import os

from errorWindow import ErrorWindow
from dict_factory import dict_factory

class DataBaseManager():
    def __init__(self,db):
        if not path.exists("databases"):
            os.makedirs("databases")
            self.errorWindow = ErrorWindow("Database folder does not exist. A new database folder had been created.")
            self.db = path.join(os.path.join("databases","dmx.db")) #as this is the first dmx database
            self.con = lite.connect(self.db)
            self.con.execute("PRAGMA foreign_keys = 1")
            self.createInitialTables()
        else:
            self.db = path.join(os.path.join("databases",db))
            self.con = lite.connect(self.db)
            self.con.execute("PRAGMA foreign_keys = 1")
            if db == "logon.db":
                if not path.isfile(path.join("databases","logon.db")):
                    self.createLogonTable()
                if not self.checkIfTableExisits("logon"):
                    self.createLogonTable()
            elif db == "universeValues.db":
                if not path.isfile(path.join("databases","universeValues.db")):
                    self.createUniverseTable()
                if not self.checkIfTableExisits("universe"):
                    self.createUniverseTable()
            elif db == "lightTypes.db":
                if not path.isfile(path.join("databases","lightTypes.db")):
                    self.createLightPlaybacksTable()
                if not self.checkIfTableExisits("lightTypes"):
                    self.createLightPlaybacksTable()
            elif db == "bars.db":
                if not path.isfile(path.join("databases","bars.db")):
                    self.createLocationsTable()
                if not self.checkIfTableExisits("locations"):
                    self.createLocationsTable()


    def createInitialTables(self):
        self.createLogonTable()
        self.createUniverseTable()
        self.createLightingRigsTable()
        self.createMainSequenceTable()
        self.createMainPlaybackTable()
        self.createLightPlaybacksTable()

    def createLocationsTable(self):
        db = path.join(os.path.join("databases","bars.db"))
        con = lite.connect(db)
        cur = con.cursor()
        cur.execute('CREATE TABLE "locations" ("id" INTEGER NOT NULL UNIQUE,"locationName" TEXT NOT NULL,"barsTableName" TEXT NOT NULL, "squaresTableName" TEXT NOT NULL, PRIMARY KEY("id" AUTOINCREMENT));')
        con.commit()
        record = [None,"default","defaultBars","defaultSquares"]#none is for the id
        self.insertRecord("locations",record)

        self.createBarsTable("defaultBars")
        self.createSquaresTable("defaultSquares")

        bars = [[1,1,900,25,"A",500,700],[2,1,900,25,"B",500,900],[3,1,900,25,"F",500,500],[4,1,900,25,"M",500,300],[5,1,900,25,"C",500,100],[6,0,25,400,"L",200,570],[7,0,25,400,"L",1700,570]]
        for bar in bars:
            self.insertRecord("defaultBars",bar)

        squares = [[1,350,50,1550,600]]
        for square in squares:
            self.insertRecord("defaultSquares",square)

    def createBarsTable(self,tableName):
        cur = self.con.cursor()
        cur.execute(f'CREATE TABLE "{tableName}" ("id" INTEGER NOT NULL UNIQUE,"isHorizontal" INTEGER NOT NULL,"width" INTEGER NOT NULL,"height" INTEGER NOT NULL,"barName" TEXT NOT NULL,"xPos" INTEGER NOT NULL,"yPos" INTEGER NOT NULL, PRIMARY KEY("id" AUTOINCREMENT))')
        self.con.commit()

    def createSquaresTable(self,tableName):
        cur = self.con.cursor()
        cur.execute(f'CREATE TABLE "{tableName}" ("id" INTEGER NOT NULL UNIQUE,"x0" INTEGER NOT NULL,"y0" INTEGER NOT NULL,"x1" INTEGER NOT NULL,"y1" INTEGER NOT NULL, PRIMARY KEY("id" AUTOINCREMENT))')
        self.con.commit()


    def createLightPlaybacksTable(self):
        db = path.join(os.path.join("databases","lightTypes.db"))
        con = lite.connect(db)
        cur = con.cursor()
        cur.execute('CREATE TABLE "lightTypes" ("id" INTEGER NOT NULL UNIQUE,"lightName" TEXT NOT NULL,"imageName" TEXT NOT NULL,"isRGB" TEXT NOT NULL,"hasPanTilt" TEXT NOT NULL,"indicatorsTableID" INTEGER, "channelNamesTableID" INTEGER, PRIMARY KEY("id" AUTOINCREMENT));')
        con.commit()

    def createChannelsTable(self,tableNumber):
        cur = self.con.cursor()
        cur.execute(f'CREATE TABLE "channels{tableNumber}" ("channelNumber" INTEGER NOT NULL UNIQUE,"channelName" INTEGER NOT NULL, "channelStartValue" INTEGER NOT NULL, "channelInformation" TEXT, PRIMARY KEY("channelNumber" AUTOINCREMENT));')
        self.con.commit()

    def createIndicatorsTable(self,tableNumber):
        cur = self.con.cursor()
        cur.execute(f'CREATE TABLE "indicators{tableNumber}"("id" INTEGER NOT NULL UNIQUE, "x"	INTEGER NOT NULL, "y" INTEGER NOT NULL, "width" INTEGER NOT NULL, "height" INTEGER NOT NULL, "type" INTEGER NOT NULL, PRIMARY KEY("id" AUTOINCREMENT));')
        self.con.commit()

    def createUniverseTable(self):
        db = path.join(os.path.join("databases","universeValues.db"))
        con = lite.connect(db)
        cur = con.cursor()
        cur.execute('CREATE TABLE "universe" ("id"	INTEGER NOT NULL UNIQUE,"channelNumber"	INTEGER NOT NULL,"channelValue"	INTEGER NOT NULL,PRIMARY KEY("id" AUTOINCREMENT));')
        con.commit()

    def createLogonTable(self):
        db = path.join(os.path.join("databases","logon.db"))
        con = lite.connect(db)
        cur = con.cursor()
        cur.execute(f'CREATE TABLE "logon" ("id" INTEGER UNIQUE,"username" TEXT NOT NULL,"password" TEXT,"databaseID" INTEGER NOT NULL,PRIMARY KEY("id" AUTOINCREMENT));')
        con.commit()

    def createLightingRigsTable(self):  #for creating database
        cur = self.con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS LightingRigs")
        cur.execute(f'CREATE TABLE LightingRigs("ID" INTEGER NOT NULL UNIQUE, "name" TEXT NOT NULL UNIQUE, "lightsTableID" INTEGER NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        self.con.commit()

    def createMainPlaybackTable(self):  #for creating database
        cur = self.con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS Playbacks")
        cur.execute(f'CREATE TABLE Playbacks("ID" INTEGER NOT NULL UNIQUE, "PlaybackID" INTEGER NOT NULL UNIQUE, "rigID" INTEGER, "Name" TEXT NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        self.con.commit()

    def createMainSequenceTable(self):  #for creating database
        cur = self.con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS Sequences")
        cur.execute(f'CREATE TABLE Sequences("ID" INTEGER NOT NULL UNIQUE, "sequenceID" INTEGER NOT NULL UNIQUE, "sequenceName" TEXT NOT NULL UNIQUE, "sequenceCreatorID" INTEGER NOT NULL, "rigID" INTEGER NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        self.con.commit()

    def createPlaybackTable(self,playbackID):
        cur = self.con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS playback{playbackID}")
        cur.execute(f'CREATE TABLE playback{playbackID}("ID" INTEGER NOT NULL UNIQUE, "channelNumber" TEXT NOT NULL, "channelValue" INTEGER NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        self.con.commit()

    def createRigTable(self,rigID):
        cur = self.con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS rig{rigID}")
        cur.execute(f'CREATE TABLE rig{rigID}("ID" INTEGER NOT NULL UNIQUE, "lightType" TEXT NOT NULL,"xPos" INTEGER NOT NULL, "yPos" INTEGER NOT NULL, "startChannel" INTEGER NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        self.con.commit()

    def createSequenceTable(self,sequenceID):
        cur = self.con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS sequence{sequenceID}")
        cur.execute(f'CREATE TABLE sequence{sequenceID}("ID" INTEGER NOT NULL UNIQUE, "playbackID" TEXT NOT NULL,"timeDelay" REAL NOT NULL,"playbackName" TEXT NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        self.con.commit()

    def createSequenceCreatorTable(self,sequenceCreatorID):
        cur = self.con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS sequenceCreator{sequenceCreatorID}")
        cur.execute(f'CREATE TABLE sequenceCreator{sequenceCreatorID}("ID" INTEGER NOT NULL UNIQUE, "lightName" TEXT NOT NULL, "lightType" TEXT NOT NULL,"xPos" INTEGER NOT NULL, "yPos" INTEGER NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        self.con.commit()

    def createSequencePlaybackTable(self,playbackID):
        cur = self.con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS sequencePlayback{playbackID}")
        cur.execute(f'CREATE TABLE sequencePlayback{playbackID}("ID" INTEGER NOT NULL UNIQUE, "channelNumber" TEXT NOT NULL, "channelValue" INTEGER NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        self.con.commit()

    def dropRigTable(self,rigID):
        cur = self.con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS rig{rigID}")
        self.con.commit()

    def dropPlaybackTable(self,rigID,playbackName):
        cur = self.con.cursor()
        cur.execute(f'SELECT PlaybackID FROM Playbacks WHERE RigID="{rigID}" AND Name="{playbackName}"')
        results = cur.fetchall()
        cur.execute(f"DROP TABLE IF EXISTS playback{results[0][0]}")
        self.con.commit()

    def deleteBarsAndSquaresTable(self,barTableName,squaresTable):
        cur = self.con.cursor()
        cur.execute(f'DELETE FROM Locations WHERE barsTableName="{barTableName}"')
        cur.execute(f'DROP TABLE {barTableName}')
        cur.execute(f'DROP TABLE {squaresTable}')
        self.con.commit()

    def deleteSequenceFromSequences(self,tableName):
        cur = self.con.cursor()
        cur.execute(f'DELETE FROM Sequences WHERE sequenceName="{tableName}"')
        self.con.commit()

    def dropSequenceTable(self,sequenceID):
        cur = self.con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS sequence{sequenceID}")
        self.con.commit()

    def dropSequenceCreatorTable(self,sequenceID):
        cur = self.con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS sequenceCreator{sequenceID}")
        self.con.commit()

    def deleteRigFromLightingRigs(self,tableName):
        cur = self.con.cursor()
        cur.execute(f'DELETE FROM LightingRigs WHERE name="{tableName}"')
        self.con.commit()

    def deletePlaybackFromPlaybacksTable(self,rigID,playbackName):
        cur = self.con.cursor()
        cur.execute(f'DELETE FROM Playbacks WHERE name="{playbackName}" AND RigID="{rigID}"')
        self.con.commit()

    def getAllData(self,table):
        exisits = self.checkIfTableExisits(table)
        if exisits == False:
            return False
        cur = self.con.cursor()
        cur.row_factory = dict_factory
        sql1 = (f'SELECT * FROM {table} ')
        cur.execute(sql1)
        results = cur.fetchall()
        return results

    def getCurrentRigsPlaybacks(self,rigID):
        cur = self.con.cursor()
        cur.row_factory = dict_factory
        sql1 = (f'SELECT * FROM Playbacks WHERE RigId="{rigID}" ')
        cur.execute(sql1)
        results = cur.fetchall()
        return results

    def checkIfTableExisits(self,tableName):  #returns true or false if exisits or not
        cur = self.con.cursor()
        sql1 = (f'SELECT name FROM sqlite_master WHERE type="table" AND name="{tableName}";')
        cur.execute(sql1)
        results = cur.fetchall()
        if len(results)==1:
            return True
        else:
            return False

    def checkIfPlaybackNameExistsInRig(self,rigID,playbackName):
        cur = self.con.cursor()
        cur.execute(f'SELECT * FROM Playbacks WHERE rigID="{rigID}" AND Name="{playbackName}"')
        results = cur.fetchall()
        if len(results)==1:
            return True
        else:
            return False


    def checkIfTableNameAlreadyUsed(self,tableName):
        cur = self.con.cursor()
        sql1 = (f'SELECT name FROM LightingRigs WHERE name="{tableName}";')
        cur.execute(sql1)
        results = cur.fetchall()
        if len(results)==1:
            return True
        else:
            return False

    def checkIfSequenceTableNameExists(self,tableName):
        cur = self.con.cursor()
        sql1 = (f'SELECT sequenceName FROM Sequences WHERE sequenceName="{tableName}";')
        cur.execute(sql1)
        results = cur.fetchall()
        if len(results)==1:
            return True
        else:
            return False

    def insertMultipleRecords(self,table,records):
        cur = self.con.cursor()
        splitValue = 333  #as 999 is the maximum allowed so 333*3
        if len(records) > splitValue:
            self.insertMultipleRecords(table,records[0:splitValue])
            self.insertMultipleRecords(table,records[splitValue:len(records)])
            return
        overallColumns = ""
        for record in records:
            columns = "?"
            for i in range(len(record)-1):
                columns = columns + ",?"
            overallColumns = overallColumns + "(" + columns + "),"
        overallColumns = overallColumns[0:len(overallColumns)-1]

        sql1 = f'INSERT INTO {table} VALUES{overallColumns}'
        # print(sql1)
        splitRecords = []
        for record in records:
            for column in record:
                splitRecords.append(column)
        cur.execute(sql1,splitRecords)
        self.con.commit()

    def insertRecord(self,table,record):
        cur = self.con.cursor()
        columns = "?"
        for i in range(len(record)-1):
            columns = columns + ",?"
        sql1 = f'INSERT INTO {table} VALUES({columns})'
        cur.execute(sql1,record)
        self.con.commit()

    def deleteAllRows(self,table):
        cur = self.con.cursor()
        sql1 = (f'DELETE FROM {table}')
        cur.execute(sql1)
        sql1 = (f'DELETE FROM sqlite_sequence WHERE name="{table}";')
        cur.execute(sql1)
        self.con.commit()
