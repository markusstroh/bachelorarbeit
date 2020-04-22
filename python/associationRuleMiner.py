#####################################
# TODO:                             #
# - präfix zu json dateien anpassen #
#####################################

from elasticsearch import Elasticsearch
import json

es = Elasticsearch()
indexName = "session-entities"


def get_file_content(file_path):
    json_file = open(file_path,"r")
    content = json_file.read()
    json_file.close()
    return content


def get_item_list(index, request_body):
    widget_list = []
    response = es.search(index=index, body=request_body)
    for widget in response["aggregations"]["widgetList"]["widgetID"]["buckets"]:
        widget_list.append(widget["key"])
    return widget_list


def get_hits(index, request_body):
    response = es.search(index=index, body=request_body)


def prepare_search_query(item_set):
    #das muss ich evtl fixen ODER in eine eine fkt auslagern
    if not isinstance(item_set, frozenset):
        item_set = frozenset([item_set])
        #print(True)

    query_body = get_file_content("../json/widgetCount.json")
    body = json.loads(query_body)
    set_iterator = iter(item_set)

    while True:
        try:
            item = next(set_iterator)
            body["query"]["bool"]["filter"][0]["nested"]["query"]["bool"]["should"][0]["match_phrase"][
                "user.sessions.widget.url.keyword"] = item
            #print(item)
            while True:
                item = next(set_iterator)
                body["query"]["bool"]["filter"].append({"nested": {"path": "user.sessions.widget", "query": {"bool":
                    {"should": [{"match_phrase": {"user.sessions.widget.url.keyword": item}}]}}}})
                #print(item)
        except StopIteration:
            break

    return body

def get_count(index,body):
    return es.count(index=index,body=body)["count"]

# der join ist falsch
def join_sets(itemset,set_len):
    set_iterator = iter(itemset)
    old_set = itemset.copy()
    length = len(old_set)
    new_set = set()

    while length > 0:
        set_iter = iter(old_set)
        while True:
            try:
                start_item = next(set_iter)
                while True:
                    next_item = next(set_iter)
                    debugger = len(start_item.intersection(next_item))
                    #das if muss wieder rein
                    if len(start_item.intersection(next_item)) == set_len-1:
                        new_set.add(start_item.union(next_item))
            except StopIteration:
                old_set.remove(start_item)
                length = len(old_set)
                break

    return new_set

#die funktion kann ich auch mit for-in schleifen & frequent items realisiern
def prune_itemset(superset,subset):
    # ich brauche eine bool variable z.B.:
    # remove_item = True
    #super_iterator = iter(superset)
    tmp_set = superset.copy()
    tmp_iterator = iter(tmp_set)
    sub_iterator = iter(subset)
    #i = 0
    j = 0

    while True:
        try:
            super_item = next(tmp_iterator)
            while True:
                try:
                    sub_item = next(sub_iterator)
                    if super_item.issuperset(sub_item):
                        # wenn mein aktuelles item aus der supermenge eine Obermenge für 1 item aus der submenge ist, setze ich remove item auf false und kann auch die aktuelle schleife verlassen
                        superset.remove(super_item)
                        super_item = next(tmp_iterator)
                    j = j+1
                except StopIteration:
                    # hier prüfe ich dann remove item. wenn true, mache ich es, wenn nicht gehe ich weiter zum nächsten item
                    #print(j)
                    break
        except StopIteration:
            break
    #print(j)


def frequent_itemset(candidates, dbsize, min_support):
    frequent_items = set()
    remove_items = set()
    cnt = 1

    while len(candidates) > 0:
        for item in candidates.copy():
            query = prepare_search_query(item)
            hits = get_count(indexName,query)
            supp = hits / dbsize
            if supp < min_support:
                remove_items.add(item)
                candidates.remove(item)

        #for item in remove_items:
            #candidates.remove(item)

        if len(candidates) > 0:
            frequent_items = candidates.copy()

        candidates = join_sets(candidates,cnt)
        prune_itemset(candidates,remove_items)
        cnt = cnt +1

    return frequent_items


def new_generate_rules(freq_items, ant_items, dbsize):
    sub_set = set()
    #result = []

    for item in ant_items:
        sub_set.add(ant_items.difference(frozenset([item])))

    for item in sub_set:
        query_oben = prepare_search_query(freq_items)
        hits_oben = get_count(indexName,query_oben)
        supp_oben = hits_oben / dbsize

        query_unten = prepare_search_query(item)
        hits_unten = get_count(indexName,query_unten)
        supp_unten = hits_unten / dbsize

        confidence = supp_oben / supp_unten

        if confidence >= 0.75:
            consequence = freq_items.difference(item)
            #result_str = list(item) + ' -> ' + list(consequence) + ' support: {}, confidence: {}'.format(supp_oben,confidence)
            result_str = '{} -> {}, support: {}, confidence: {}'.format(list(item),list(consequence),supp_oben,confidence)
            return result_str
        elif len(item) > 1:
            new_generate_rules(freq_items,item,dbsize)



def generate_rules(freq_item_set,dbsize):
    result = []

    for set in freq_item_set:
        for item in set:
            query = prepare_search_query(item)
            antecedent_hits = get_count(indexName, query)
            antecedent_supp = antecedent_hits / dbsize
            #diff_set = set.difference(item)
            query = prepare_search_query(set)
            consequence_hits = get_count(indexName, query)
            consequence_supp = consequence_hits / dbsize
            conf = consequence_supp / antecedent_supp

            result_str = build_result_string(item,set)
            result_str = result_str + ' confidence: {}'.format(conf)
            result.append(result_str)

    return result

def build_result_string(antecedence,consequence):
    str = ''
    for item in antecedence:
        str = str + item + ', '

    str = str + ' -> '
    #consequence = consequence.difference(frozenset([antecedence]))
    for item in consequence:
        str = str + item + ', '

    return str
########### hier gehts los

widget_list_json_content = get_file_content("../json/widgetList.json")
widgets = get_item_list(indexName, widget_list_json_content)
#print("list of all widgets:")
#print(widgets)

candidates = set()

for widget in widgets:
    candidates.add(frozenset([widget]))

#print(candidates)
#for set in candidates:
#    for item in set:
#        print(item)

# hier muss ich das noch ändern
sessionID_count_json_content = get_file_content("../json/sessionIDCount.json")
sessionID_count = es.search(index=indexName, body=sessionID_count_json_content)["hits"]["total"]["value"]
print("total number of sessions: {}".format(sessionID_count))
#####



#testSet = frozenset(["balancesByCurrencies", "LiquidityByAccountsWidgetContent","favouriteViews"]) # testset = frozenset({'widget1','widget2','widget3'})

#query = prepare_search_query(testSet)
#print(get_count(indexName,query))

freqItems = frequent_itemset(candidates, sessionID_count, 0.3)

#print(candidates)
#print(freqItems)
#print()



#rules = generate_rules(freqItems, sessionID_count)
#rules = new_generate_rules(freqItems, sessionID_count)
#print(len(rules))

#for rule in rules:
#    print(rule)

rules = []
for freqItem in freqItems:
    rules.append(new_generate_rules(freqItem,freqItem,sessionID_count))

for rule in rules:
    print(rule)
