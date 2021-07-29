from os import system
from hcfg.exceptions import *
import json
import ast

class hcfgdb():
    def __init__(self,fileName):
        self.file = fileName
        if not open(fileName):
            raise hypFileError("[Errno 1] File does not exist.")
            return
        if not fileName.endswith(".hcfg"):
            raise hypFileError("[Errno 0] This is a not .hcfg file.")
            return
    
    def getValue(self,variableName):
        return hcfg.getValue(self.file,variableName)

    def setValue(self,variableName,newValue):
        hcfg.changeValue(self.file,variableName,newValue)
    
    def addValue(self,variableName,_value):
        hcfg.addValue(self.file,variableName,_value)

    def getObjects(self,variableID):
        object = hcfg.readFile(self.file)
        b = []
        for i in object:
            a = self.getValue(i)
            if not a[f'{variableID}'] in a:
                value = hcfg.assignValue(a[variableID])
                b.append({f'{variableID}' : value})
        return b 
                



class hcfg():


    def __init__(self) -> None:
        pass
    

    @staticmethod
    def readFile(fileName):
        buffer = {}
        if not fileName.endswith(".hcfg"):
            raise hypFileError("[Errno 0] This is a not .hcfg file.")
            return
            

        if not (open(fileName,"r")):
            raise hypFileError("[Errno 1] File does not exist.")
            return

        with open(fileName,"r",encoding="utf8") as file:
            i = 0
            for line in file:
                i += 1
                object = line.split(":",1)
                if len(object) <= 1:
                    raise hypSyntaxError(f"[Errno 2] Syntax error [Line:{i}].")
                    return
                name = object[0].strip(" ")
                value = hcfg.assignValue(object[1])
                if(value.startswith("{")):
                    value = value.replace("'",'"')
                    dict = json.loads(value)
                    buffer[name] = dict
                else:
                    buffer[name] = value
            return buffer

    @staticmethod
    def saveFile(filename,object):
        if not filename.endswith(".hcfg"):
            raise hypFileError("[Errno 0] This is a not .hcfg file.")
            return
        with open(filename, "w",encoding="utf8") as file:
            for i in object:
                string = f"{i} : {object[i]}\n"
                file.writelines(string)


    @staticmethod
    def changeValue(filename,variableName,_value):
        if not filename.endswith(".hcfg"):
            raise hypFileError("[Errno 0] This is a not .hcfg file.")
            return
        if not open(filename):
            raise hypFileError("[Errno 1] File does not exist.")
            return
        object = hcfg.readFile(filename)
        if not variableName in object:
            raise hypObjectError("[Errno 4] Variable does not exist.")
        else:
            object[variableName] = _value
            hcfg.saveFile(filename,object)

    @staticmethod
    def getValue(filename,variableName):
        if not filename.endswith(".hcfg"):
            raise hypFileError("[Errno 0] This is a not .hcfg file.")
            return
        if not open(filename):
            raise hypFileError("[Errno 1] File does not exist.")
            return
        object = hcfg.readFile(filename)
        if not variableName in object:
            raise hypObjectError("[Errno 4] Variable does not exist.")
        else:
            return hcfg.assignValue(object[variableName])

    
    @staticmethod
    def addValue(filename,variableName,value):
        if not filename.endswith(".hcfg"):
            raise hypFileError("[Errno 0] This is a not .hcfg file.")
            return
        if not open(filename):
            raise hypFileError("[Errno 1] File does not exist.")
            return
        object = hcfg.readFile(filename)
        if variableName in object:
            raise hypObjectError("[Errno 5] Variable already exist.")
        else:
            with open(filename,"a+",encoding="utf8") as file:
                newVal = hcfg.assignValue(value)
                file.writelines(f"{variableName} : {newVal}\n")
                
                
            
        

    @staticmethod
    def assignValue(value):

        if(type(value) == dict):
            return value

        boolVal = ""
        try:
            boolVal = value.strip().strip('"')
        except:
            None
        if(boolVal == "True"):
            return True
        if (boolVal == "False"):
            return False
        try:
            val = int(value)
            return val
        except:
            None
        try:
            val = str(value).strip().strip('"')
            val = f'{val}'
            return val
        except:
            None
        try:
            val = bool(value)
            return val
        except:
            None    