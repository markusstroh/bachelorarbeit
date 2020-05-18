# Get date from logstash
def register(params)
    @sessionObject = params["parsedJson"]
end


def filter(event)

    data = event.get(@sessionObject)

    numberOfUserIDs = data["aggregations"]["userid"]["buckets"].size

    i = 0
    eventArray = Array.new
    # Iterate through the JSON data that is passed by logstash. Read the information that is needed for the session
    # entities and store them in given fields. These field are later stored in the eventArray which will be returned
    # to logstash. The execution of this script creates one session entity at a time.
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

            # This array stores the widget name and number of usages per session
            urlArray = Array.new

            while k < numberOfURLs do
                url = data["aggregations"]["userid"]["buckets"][i]["sessionid"]["buckets"][j]["url"]["buckets"][k]["key"]
                widgetCounter = data["aggregations"]["userid"]["buckets"][i]["sessionid"]["buckets"][j]["url"]["buckets"][k]["doc_count"]
                
                urlArray.push("url" => url, "used" => widgetCounter)

                #### This part is necessary to store the session entity in a slightly different way for the
                # visualizations in kibana.
                eventEntry = {"id" => userid, "sessions" => {"id" => sessionid, "sessionStart" => startTime, "sessionEnd" => endTime, "widget" => ["url" => url, "used" => widgetCounter]},"tags" => "vis"}
                currentEvent = event.clone
                currentEvent.set("[user]",eventEntry)
                eventArray.push(currentEvent)
                ####

                k += 1
            end

            # Send transformed data back to logstash
            eventEntry = {"id" => userid, "sessions" => {"id" => sessionid, "sessionStart" => startTime, "sessionEnd" => endTime, "widget" => urlArray}, "tags" => "nested"}
            currentEvent = event.clone
            currentEvent.set("[user]",eventEntry)
            eventArray.push(currentEvent)
            j += 1
        end
        i += 1
   end

    return eventArray
end
