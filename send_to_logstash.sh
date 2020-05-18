#!/bin/bash

# This script can be used to send queries to elasticsearch. The first argument should be the index that is going to be searched, the second shpuld be a .json
# file containing the search query
curl -X POST -H "Content-Type: application/json" -d @$1 http://localhost:9200/$2/_search?pretty


# curl -X GET -H "Content-Type: application/json" http://localhost:9200/_cat/indices
