from elasticsearch import Elasticsearch
import re
import json

class ElasticHelper:
#    def __init__(self,workDir):
#        self.workDir = workDir

    es = Elasticsearch()

    def getAllIndicesByIndexPattern(indexPattern):
        indices = []
        catString = es.cat.indices(index=indexPattern).split()
        regex = re.compile(indexPattern)

        for s in catString:
            if regex.match(s):
                indices.append(s)

        return indices
    
    def getBodyByJsonFile(self,filePath):
        content = ""
        jsonFile = open(self.workDir + filePath, "r")
        content = jsonFile.read()
        
        return content



