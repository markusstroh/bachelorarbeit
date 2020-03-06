#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d @$1 http://localhost:9200/logstash/_search?pretty
