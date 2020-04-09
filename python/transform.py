from datetime import datetime
from elasticsearch import Elasticsearch
import re
import json
from os import path

es = Elasticsearch()

    
indexFilter = 'generated-logs-*'
catString = es.cat.indices(index=indexFilter).split()
regex = re.compile(indexFilter)

indicies = []
for s in catString:
    if regex.match(s):
        indicies.append(s)

#aprint(indicies[0])

transformFile = open('../json/transform_vorschlag2.json','r')

content = ""
if transformFile.mode == 'r':
    content = transformFile.read()

#print(content)
for index in indicies:
    if not path.exists(index+"transformed.json"):
        res = es.search(index=index,body=content)
        print("transforming " + index)

        transformedLog = open("./" + index + "transformed.json","w")
        transformedLog.write(json.dumps(res,indent=2))
        transformedLog.write("\n")
        transformedLog.close()
    else:
        print(index + " is already transformed")

transformFile.close()
