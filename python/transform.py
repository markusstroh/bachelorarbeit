from elasticsearch import Elasticsearch, exceptions
import re
import json
import datetime
import sys
from os import path

es = Elasticsearch()
indexFilter = 'generated-logs-*'


def getFileContent(filePath):
    with open(filePath, "r") as file:
        content = file.read()

    return content


def createIndex():
    """ This mehtod checks if a index for session enteties exists. If not a index will be created with the mapping
        specified in mappingForSessionEntityQuery.json
    """
    try:
        es.cat.indices(index="session-entities")
        print("Index available")
    except exceptions.NotFoundError:
        print("No index for Session Entites exist. Create Index")
        queryBody = getFileContent("../json/mappingForSessionEntityQuery.json")
        es.indices.create(index="session-entities", body=queryBody)


def getIndexList():
    """ This method gets a list of indicies. It fetches all the indicies that contain a given index pattern.
        The response includes more data than just the index names, so the method getIndicies filters  just the names
        from the response
    """
    response = es.cat.indices(index=indexFilter).split()
    indiciesList = getIndicies(response)
    return indiciesList


def getIndicies(indexList):
    """ Filters the index names from the response
    Args:
        indexList (list): list that includes information from the unfiltered response

    Returns:
        indices (list): list of indices stored in elasticsearch
    """
    indices = []
    regex = re.compile(indexFilter)
    for index in indexList:
        if regex.match(index):
            indices.append(index)

    return indices


def getFileDir(index):
    """ Gets the directory where the logfiles are stored. In this directory the transformed data will be stored as
        JSON files. In order to achieve that a search query will be send to elasticsearch and gets the information
        where the logfile associated to the index is stored.
    Args:
        index (str): name of a index.

    Returns:
        workdir (str): Path to the directory

    """
    if len(index) > 0:
        filePathJsonContent = getFileContent("../json/getLogfileDirectoryQuery.json")
        workdir = es.search(index=index, body=filePathJsonContent)["aggregations"]["workdir"]["buckets"][0]["key"]
        workdir = workdir[0:workdir.rindex("/") + 1]

    return workdir


def writeTransformedData(index, query, directory):
    """ Writes transformed data of an index to a new file in the directory passed as argument. In order to avoid
        duplicates the function checks if a file with the transformed data is already present in the directory.

    Args:
        index (str): Index that should be transformed
        query (str): Query that is send to elasticsearch that transforms the data
        directory (str): Location where the transformed data will be safe as JSON file

    """
    if not path.exists(directory + index + "transformed.json"):
        res = es.search(index=index, body=query)
        print("transforming " + index)

        with open(directory + index + "transformed.json", "w") as transformedLog:
            transformedLog.write(json.dumps(res, indent=2))
            transformedLog.write("\n")
    else:
        print(index + " is already transformed")


def checkForTodaysLogfile(index):
    """ Checks if todays data is tried to be transformed. That should be avoided since the data for today may not be
        complete. If the data would be transformed too early not all data might be transformed so the database would
        be corrupted.

    Args:
        index (str): Index that is tried to be transformed

    Returns:
        (bool): True, if it is safe to transform the index

    """
    today = datetime.datetime.now().strftime("%Y.%m.%d")
    if index.find(today) > -1:
        print("Warning: you are trying to transform todays logfile."
              "This may corrupt the database since new data may come in. Transform today's data"
              " tomorrow", file=sys.stderr)
        return False
    else:
        return True


def main():
    print("Start transforming data")

    createIndex()
    indicies = getIndexList()

    transformQueryContent = getFileContent("../json/transformQuery.json")
    workdir = getFileDir(indicies[0])

    for index in indicies:
        if checkForTodaysLogfile(index):
            writeTransformedData(index, transformQueryContent, workdir)

    print("Done transforming data")


if __name__ == "__main__":
    main()

