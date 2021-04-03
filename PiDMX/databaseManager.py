import sqlite3 as lite
from os import path
import os

class DataBaseManager():
    def __init__(self,db):
        self.db = path.join(os.path.join("databases",db))
        con = lite.connect(self.db)

    def createLightingRigsTable(self):  #for creating database
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS LightingRigs")
        cur.execute(f'CREATE TABLE LightingRigs("ID" INTEGER NOT NULL UNIQUE, "name" TEXT NOT NULL UNIQUE, "lightsTableID" INTEGER NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        con.commit()

    def createMainPlaybackTable(self):  #for creating database
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS Playbacks")
        cur.execute(f'CREATE TABLE Playbacks("ID" INTEGER NOT NULL UNIQUE, "PlaybackID" INTEGER NOT NULL UNIQUE, "rigID" INTEGER, "Name" TEXT NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        con.commit()

    def createMainSequenceTable(self):  #for creating database
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS Sequences")
        cur.execute(f'CREATE TABLE Sequences("ID" INTEGER NOT NULL UNIQUE, "sequenceID" INTEGER NOT NULL UNIQUE, "sequenceName" TEXT NOT NULL UNIQUE, "sequenceCreatorID" INTEGER NOT NULL, "rigID" INTEGER NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        con.commit()

    def createPlaybackTable(self,playbackID):
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS playback{playbackID}")
        cur.execute(f'CREATE TABLE playback{playbackID}("ID" INTEGER NOT NULL UNIQUE, "channelNumber" TEXT NOT NULL, "channelValue" INTEGER NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        con.commit()

    def createRigTable(self,rigID):
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS rig{rigID}")
        cur.execute(f'CREATE TABLE rig{rigID}("ID" INTEGER NOT NULL UNIQUE, "lightType" TEXT NOT NULL,"xPos" INTEGER NOT NULL, "yPos" INTEGER NOT NULL, "startChannel" INTEGER NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        con.commit()

    def createSequenceTable(self,sequenceID):
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS sequence{sequenceID}")
        cur.execute(f'CREATE TABLE sequence{sequenceID}("ID" INTEGER NOT NULL UNIQUE, "playbackID" TEXT NOT NULL,"timeDelay" REAL NOT NULL,"playbackName" TEXT NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        con.commit()

    def createSequenceCreatorTable(self,sequenceCreatorID):
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS sequenceCreator{sequenceCreatorID}")
        cur.execute(f'CREATE TABLE sequenceCreator{sequenceCreatorID}("ID" INTEGER NOT NULL UNIQUE, "lightName" TEXT NOT NULL, "lightType" TEXT NOT NULL,"xPos" INTEGER NOT NULL, "yPos" INTEGER NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        con.commit()

    def createSequencePlaybackTable(self,playbackID):
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS sequencePlayback{playbackID}")
        cur.execute(f'CREATE TABLE sequencePlayback{playbackID}("ID" INTEGER NOT NULL UNIQUE, "channelNumber" TEXT NOT NULL, "channelValue" INTEGER NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT));')
        con.commit()


    def dropRigTable(self,rigID):
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS rig{rigID}")
        con.commit()

    def dropPlaybackTable(self,rigID,playbackName):
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f'SELECT PlaybackID FROM Playbacks WHERE RigID="{rigID}" AND Name="{playbackName}"')
        results = cur.fetchall()
        cur.execute(f"DROP TABLE IF EXISTS playback{results[0][0]}")
        con.commit()

    def deleteSequenceFromSequences(self,tableName):
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f'DELETE FROM Sequences WHERE sequenceName="{tableName}"')
        con.commit()

    def dropSequenceTable(self,sequenceID):
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS sequence{sequenceID}")
        con.commit()

    def dropSequenceCreatorTable(self,sequenceID):
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS sequenceCreator{sequenceID}")
        con.commit()

    def deleteRigFromLightingRigs(self,tableName):
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f'DELETE FROM LightingRigs WHERE name="{tableName}"')
        con.commit()

    def deletePlaybackFromPlaybacksTable(self,rigID,playbackName):
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f'DELETE FROM Playbacks WHERE name="{playbackName}" AND RigID="{rigID}"')
        con.commit()

    def getAllData(self,table):
        exisits = self.checkIfTableExisits(table)
        if exisits == False:
            return False
        con = lite.connect(self.db)
        cur = con.cursor()
        sql1 = (f'SELECT * FROM {table} ')
        cur.execute(sql1)
        results = cur.fetchall()
        return results

    def getCurrentRigsPlaybacks(self,rigID):
        con = lite.connect(self.db)
        cur = con.cursor()
        sql1 = (f'SELECT * FROM Playbacks WHERE RigId="{rigID}" ')
        cur.execute(sql1)
        results = cur.fetchall()
        return results


    def checkIfTableExisits(self,tableName):  #returns true or false if exisits or not
        con = lite.connect(self.db)
        cur = con.cursor()
        sql1 = (f'SELECT name FROM sqlite_master WHERE type="table" AND name="{tableName}";')
        cur.execute(sql1)
        results = cur.fetchall()
        if len(results)==1:
            return True
        else:
            return False

    def checkIfPlaybackNameExistsInRig(self,rigID,playbackName):
        con = lite.connect(self.db)
        cur = con.cursor()
        cur.execute(f'SELECT * FROM Playbacks WHERE rigID="{rigID}" AND Name="{playbackName}"')
        results = cur.fetchall()
        if len(results)==1:
            return True
        else:
            return False


    def checkIfTableNameAlreadyUsed(self,tableName):
        con = lite.connect(self.db)
        cur = con.cursor()
        sql1 = (f'SELECT name FROM LightingRigs WHERE name="{tableName}";')
        cur.execute(sql1)
        results = cur.fetchall()
        if len(results)==1:
            return True
        else:
            return False

    def checkIfSequenceTableNameExists(self,tableName):
        con = lite.connect(self.db)
        cur = con.cursor()
        sql1 = (f'SELECT sequenceName FROM Sequences WHERE sequenceName="{tableName}";')
        cur.execute(sql1)
        results = cur.fetchall()
        if len(results)==1:
            return True
        else:
            return False

    def insertMultipleRecords(self,table,records):
        con = lite.connect(self.db)
        cur = con.cursor()
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
        con.commit()

    def insertRecord(self,table,record):
        con = lite.connect(self.db)
        cur = con.cursor()
        columns = "?"
        for i in range(len(record)-1):
            columns = columns + ",?"
        sql1 = f'INSERT INTO {table} VALUES({columns})'
        cur.execute(sql1,record)
        con.commit()

    def deleteAllRows(self,table):
        con = lite.connect(self.db)
        cur = con.cursor()
        sql1 = (f'DELETE FROM {table}')
        cur.execute(sql1)
        sql1 = (f'DELETE FROM sqlite_sequence WHERE name="{table}";')
        cur.execute(sql1)
        con.commit()
