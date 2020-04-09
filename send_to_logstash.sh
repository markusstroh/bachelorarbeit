#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d @$1 http://localhost:9200/generated-logs/_search?pretty


# curl -X GET -H "Content-Type: application/json" http://localhost:9200/_cat/indices
