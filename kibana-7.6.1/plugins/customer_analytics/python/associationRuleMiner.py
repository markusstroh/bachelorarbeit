from elasticsearch import Elasticsearch
import json
import argparse
import itertools as it
''' These import are used to analyse the runtime and memory usage of the script. They are not necessary for finding 
    association rules
'''
import timeit
from memory_profiler import profile


def getFileContent(filePath):
    with open(filePath, "r") as file:
        content = file.read()

    return content


def getItemList(index, requestBody):
    """ Get a list of widgets that are stored in the elasticsearch database.
    Args:
        index (str): Specifies the index that should be searched.
        requestBody (str): Request body for the search query.
    Returns:
            widgetList: List of widgets.
    """
    widgetList = []
    response = es.search(index=index, body=requestBody)
    for widget in response["aggregations"]["widgetList"]["widgetID"]["buckets"]:
        widgetList.append(widget["key"])
    return widgetList


def prepareSearchQuery(itemSet):
    """ Prepares the request body for a search query that will be send to elasticsearch. The request body is in
    JSON format. This method is written for dealing with frozensets so if the passed argument is not already a
    frozenset, it will be converted. Then we iterate through the set and the item names in the right positions.
    The semantic of the search query should be specified in a JSON file, e.g. widgetCount.json. In this particular
    case the semantic is like 'Search for widget1 and widget2 and ... and widgetN'.

    Args:
        itemSet (frozenset): A set of items that will be searched.

    Returns:
        body (str): Request body

    """
    if not isinstance(itemSet, frozenset):
        itemSet = frozenset([itemSet])

    queryBody = getFileContent("../json/widgetCount.json")
    body = json.loads(queryBody)
    setIterator = iter(itemSet)

    while True:
        try:
            item = next(setIterator)
            body["query"]["bool"]["filter"][0]["nested"]["query"]["bool"]["should"][0]["match_phrase"][
                "user.sessions.widget.url.keyword"] = item
            while True:
                item = next(setIterator)
                body["query"]["bool"]["filter"].append({"nested": {"path": "user.sessions.widget", "query": {"bool":
                        {"should": [{"match_phrase": {"user.sessions.widget.url.keyword": item}}]}}}})
        except StopIteration:
            break

    return body


def getCount(item):
    """ Sends a search query to elasticsearch and returns the number of hits. Depending on the item(s) the
    request body has to be created before.

    Args:
        item (set): Set of items that should be searched.

    Returns:
        amount of hits in the response of the search query

    """
    body = prepareSearchQuery(item)
    return es.count(index=indexName, body=body)["count"]


def joinSets(frequentItems):
    """ Generates new candidate itemsets by joining the elements in frequentItems. It iterates through the itemset and
        joins itemsets that have k-1 equal elements where k is the length of the itemsets. The result is a new
        candidate set with k + 1 elements

    Args:
        frequentItems (set): itemset from which candidates are generated

    Returns:
          newCandidatesSet (set): Set of newly generated candidates

    """
    newCandidatesSet = set()

    while True:
        setIterator = iter(frequentItems)
        try:
            startItem = next(setIterator)
            while True:
                try:
                    nextItem = next(setIterator)
                    if len(startItem.intersection(nextItem)) == len(startItem) - 1:
                        newCandidatesSet.add(startItem.union(nextItem))
                except StopIteration:
                    frequentItems.remove(startItem)
                    break
        except StopIteration:
            break

    return newCandidatesSet


def pruneItemset(candidateSet, frequentItems):
    """ Removes itemsets that can not be considered as candidates if not every subset of the candidate set is in the
        already found frequent itemsets.

    Args:
        candidateSet (set): Set with candidates
        frequentItems (set): Set with items that are frequent

    """
    for candidate in candidateSet.copy():
        for item in it.combinations(candidate, len(candidate) - 1):
            if not frozenset(item) in frequentItems:
                candidateSet.remove(candidate)
                break


def getFrequentItemset(items):
    """ This function is actually a implementation of the apriori algorithm. It calculates the support of the
        candidates passed as argument and generates new candidates that satisfy the minsupport until a empty set is
        generated. In that case the itemsets found in the previous iteration are frequent and will be returned.
        The minsupport needs to be passed by the command line (or whatever executes the script) with -minsupport=[value]
        
    Args:
        items (set): Set of from which this function calculates frequent itemsets

    Returns:
        frequentItems (set): Set of all frequent items
    
    """
    frequentItems = set()

    while len(items) > 0:
        for item in items.copy():
            hits = getCount(item)
            supp = hits / dbsize
            if supp < float(args.minsupport):
                items.remove(item)

        if len(items) > 0:
            frequentItems = items.copy()

        items = joinSets(items)
        pruneItemset(items, frequentItems)

    return frequentItems


def generateRules(freqItems, antecedenceItems, resultSet):
    """ This function generates all possible association rules that can be found in the frequent itemsets that satisfy
        the minconf. Like the minsupport the minconf need to be passed by the command line using -minconf=[value].
        The confidence of a rule A => X - A is calculated as support(X) / support(A). If this rule satisfies the
        minconf it will check if A' also satisfies the minconf where A' is a subset of A. This is done recursively
        at the end of the function.

    Args:
        freqItems (set): Set of frequent items in which association rules should be found
        antecedenceItems (set): Set of items that are a a subset of the itemset of the left side of an association rule
        resultSet (set): Set of found association rules

    """
    for item in antecedenceItems:
        item = antecedenceItems.difference(frozenset([item]))

        supportItemset = getCount(freqItems) / dbsize
        supportItem = getCount(item) / dbsize

        confidence = supportItemset / supportItem

        if confidence >= float(args.minconf):
            consequence = freqItems.difference(item)
            result_str = f'{list(item)} -> {list(consequence)}, ' \
                         f'support: {format(supportItemset, ".4f")}, confidence: {format(confidence, ".4f")}'
            resultSet.add(result_str)
            if len(item) > 1:
                generateRules(freqItems, item, resultSet)


def getWidgets():
    """ Gets a set of all widgets that are going to be analyzed in the association rule mining process

    Returns:
        widgetSet (set): set of all widgets that occur in sessions

    """
    widgetListJSONContent = getFileContent("../json/widgetList.json")
    widgets = getItemList(indexName, widgetListJSONContent)
    widgetSet = set()

    for widget in widgets:
        widgetSet.add(frozenset([widget]))

    return widgetSet


def getDatabaseSize():
    sessionIDCountJSONContent = getFileContent("../json/sessionIDCount.json")
    return es.search(index=indexName, body=sessionIDCountJSONContent)["hits"]["total"]["value"]


es = Elasticsearch()
indexName = "session-entities"

parser = argparse.ArgumentParser()
parser.add_argument("-minsupport")
parser.add_argument("-minconf")
args = parser.parse_args()

dbsize = getDatabaseSize()


#@profile
def main():
    """ This function is the entry point of the script. Before anything else is executed some necessary values are set
        such as the database size or arguments passed by the command line. There is a argument passed to this function
        that controls the output of the script if the user wants to make some benchmark tests such as execution time
        or memory usage. This argument should be removed later on.

    Args:
        printBool (bool): True, if association rules should be printed. False otherwise.

    """
    candidates = getWidgets()

    freqItems = getFrequentItemset(candidates)

    rule_set = set()
    for freqItem in freqItems:
        generateRules(freqItem, freqItem, rule_set)

    for rule in sorted(rule_set):
        print(rule)


if __name__ == "__main__":
    if args.minsupport and args.minconf:
        main()
    else:
        print("Please provide values for minsupp and minconf")
