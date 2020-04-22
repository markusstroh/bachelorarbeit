#TODO:
# ich muss die zeitangaben noch ändern, sodass nur noch tage da stehen. tage wird nämlich die kleinste zeiteinheit sein
def register(params)
    @sessionObject = params["parsedJson"]
end


def filter(event)

    data = event.get(@sessionObject)

    numberOfUserIDs = data["aggregations"]["userid"]["buckets"].size
    #numberOfSessionIDs = data["aggregations"]["userid"]["buckets"][0]["sessionid"]["buckets"].size
    
    #data["aggregations"]["userid"]["buckets"]

    i = 0
    eventArray = Array.new
    while i < numberOfUserIDs do 
        numberOfSessionIDs = data["aggregations"]["userid"]["buckets"][i]["sessionid"]["buckets"].size
        j = 0
        userid = data["aggregations"]["userid"]["buckets"][i]["key"]
        while j < numberOfSessionIDs do
            k = 0
            numberOfURLs = data["aggregations"]["userid"]["buckets"][i]["sessionid"]["buckets"][j]["url"]["buckets"].size
            sessionid = data["aggregations"]["userid"]["buckets"][i]["sessionid"]["buckets"][j]["key"]
            startTime = data["aggregations"]["userid"]["buckets"][i]["sessionid"]["buckets"][j]["min-time"]["value_as_string"]
            endTime = data["aggregations"]["userid"]["buckets"][i]["sessionid"]["buckets"][j]["max-time"]["value_as_string"]
            #das brauche ich für association rules
            #urlArray = Array.new
            ###
            while k < numberOfURLs do
                url = data["aggregations"]["userid"]["buckets"][i]["sessionid"]["buckets"][j]["url"]["buckets"][k]["key"]
                widgetCounter = data["aggregations"]["userid"]["buckets"][i]["sessionid"]["buckets"][j]["url"]["buckets"][k]["doc_count"]
                
                #das brauche ich für association rules
                #urlArray.push("url" => url, "used" => widgetCounter)
                ###

                # das bruache ich für die visualisierung
                eventEntry = {"id" => userid, "sessions" => {"id" => sessionid, "sessionStart" => startTime, "sessionEnd" => endTime, "widget" => ["url" => url, "used" => widgetCounter] }}
                currentEvent = event.clone
                currentEvent.set("[user]",eventEntry)
                eventArray.push(currentEvent)
                ###
                k += 1
            end
            # das brauche ich für association rules
            #eventEntry = {"id" => userid, "sessions" => {"id" => sessionid, "sessionStart" => startTime, "sessionEnd" => endTime, "widget" => urlArray}}
            #currentEvent = event.clone
            #currentEvent.set("[user]",eventEntry)
            #eventArray.push(currentEvent)
            #####
            j += 1
        end
        i += 1
   end



    #f = printFactors(data)
#    puts f

#    event.remove("message")

#    a = {"id" => "schusterl", "sessions" => ["id" => "test","id" => "test2"]}
#    event.set("[user]", a)

#    x = Array.new
#    x.push(event)

#    y = event.clone
#    c = "stroh"
#    b = {"id" => c, "sessions" => {"id" => "tesdasdast","starttime" => "0","endtime" => "1","urls" => {} }}
#    y.set("[user]",b)
#    x.push(y)
#    test(y)
    
    #event.set("user", {"id" => "adler"})
    #puts event.to_hash.keys
    #puts event.get("message")



    #return x
    return eventArray
end

# hier mache ich eine funktion, die mit ein array oder eine map zurück gibt, die die url zu den sessions mappt
def test(event)
    puts "JAWOLL ALDER"
    puts event.get("user")
end

def printFactors(data)
    numberOfUserIDs = data["aggregations"]["userid"]["buckets"].size 
    numberOfSessionIDs = data["aggregations"]["userid"]["buckets"][0]["sessionid"]["buckets"].size
    numberOfURLs = data["aggregations"]["userid"]["buckets"][0]["sessionid"]["buckets"][0]["url"]["buckets"].size

    #puts "total number of userids #{numberOfUserIDs}"
    #puts "total number of sessionids for user #{numberOfSessionIDs}"
    #puts numberOfURLs
    startTime data["aggregations"]["userid"]["buckets"][0]["sessionid"]["buckets"][0]["max-time"]["value_as_string"]
    endTime = data["aggregations"]["userid"]["buckets"][0]["sessionid"]["buckets"][0]["min-time"]["value_as_string"]


    return 53
end