from datetime import datetime
from elasticsearch import Elasticsearch
import re
import json
from os import path

# TODO:
# - auf 2 arten transformieren
# - schauen, ob files schon existieren
# - daten an javascript übergeben
# - die transformierten Daten sollen da liegen, wo auch die logs liegen, also muss ich nach path suchen



def main():
    print("start transforming data")
    es = Elasticsearch()



    #workdir = "/Users/markusstroh/Desktop/Uni/Informatik/bachelorarbeit/"


    indexFilter = 'generated-logs-*'

   #hier erstelle ich erstmal den index für die association rules
    try:
        es.cat.indices(index="session-entities")
        print("Index available")
        #print(es.cat.indices(index="sessionEntity"))
    except:
        print("No index for Session Entites exist. Create Index")
        mapping = open("../json/mappingForSessionEntity.json", "r")
        content = mapping.read()
        es.indices.create(index="session-entities",body=content)


    #hier bekomme ich eine list mit den logfiles
    catString = es.cat.indices(index=indexFilter).split()
    regex = re.compile(indexFilter)

    indicies = []
    for s in catString:
        if regex.match(s):
            indicies.append(s)

#aprint(indicies[0])
    #workdir = path.realpath('.')
    transformFile = open('../json/transform_vorschlag2.json','r')

    content = ""
    if transformFile.mode == 'r':
        content = transformFile.read()

    workdir = ""
    if len(indicies) > 0:
        filePathJsonContent = open("../json/filePath.json", "r").read()
        workdir = es.search(index=indicies[0],body=filePathJsonContent)["aggregations"]["workdir"]["buckets"][0]["key"]
        workdir = workdir[0:workdir.rindex("/")+1]

    #print(content)
    for index in indicies:
        if not path.exists(index+"transformed.json"):
            res = es.search(index=index,body=content)
            print("transforming " + index)

            transformedLog = open(workdir + index + "transformed.json","w")
            transformedLog.write(json.dumps(res,indent=2))
            transformedLog.write("\n")
            transformedLog.close()
        else:
            print(index + " is already transformed")

    transformFile.close()

    print("done transforming data")

    #return "JAWOLL ALDER"


if __name__ == "__main__":
    main()

