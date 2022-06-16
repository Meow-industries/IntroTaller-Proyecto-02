import json


class JsonManager:

    def readJson(self, pPath):
        result = {}
        with open(pPath, 'r') as openfile:

            # Reading from json file
            result = json.load(openfile)
        return result

    def writeJson(self, pPath, pContent):
        with open(pPath, "w") as outfile:
            json.dump(pContent, outfile)
    
