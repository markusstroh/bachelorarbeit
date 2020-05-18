# Bachelorarbeit
In diesem Repository befindet sich der Source Code zu der Bachelorarbeit "Analyse des Kundenverhaltens durch Mustererkennung in Logfiles" von Markus Stroh.
## Voraussetzungen
#### ELK Version
Für den ELK sollten die folgenden Versionen benutzt werden:
- Elasticsearch: 7.6.1
- Kibana: 7.6.1 (https://github.com/elastic/kibana/tree/7.6)
- Logstash: 7.6.1
- Filebeat: 7.6.1

Es ist wichtig, dass die Kibana von dem angegebenen Repository geklont wird, da im Rahmen der Bachelorarbeit ein Custom Plugin entwickelt wurde, welches noch in der Entwicklungsphase ist.

#### Sonstige Software
Des weiteren wird:
- python3.7
- yarn version 1.22.4
- node.js version 10.19.0
- Python Elasticsearch Client (https://elasticsearch-py.readthedocs.io/en/master/)
- Itertools (https://docs.python.org/3/library/itertools.html)
- argparse (https://docs.python.org/3/library/argparse.html)
- JSON encoder and decoder (https://docs.python.org/3/library/json.html)
- Regular expressions operator (https://docs.python.org/3/library/re.html)
- datetime (https://docs.python.org/3/library/datetime.html)
- sys (https://docs.python.org/3/library/sys.html)
- os (https://docs.python.org/3/library/os.html)
benutzt.

## Benutzung
In diesem Repository liegen generierte logfiles, mit denen das System getestet werden kann. Möchte man selber neue Daten generieren, kann man das Bash Skript generateLogFiles.sh ausführen. Dieses Skript ruft das Python Skript logEntryGenerator.py auf, welches Logfiles generiert. Diese Logfiles liegen in dem Ordner multiversa-/

Bevor das System gestartet werden können müssen folgende Vorbereitungen getroffen werden:
- die Datei filebiat-7.6.1/filebeat.yml muss in den entsprechenden Filebeat Ordner auf dem verwendeten System kopiert werden
- die Dateien logstash-7.6.1/bin/pipeline.conf und logstash-7.6.1/bin/script.rb müssen in den entsprechenden Logstash Ordner auf dem verwendeten System kopiert werden
- der Ordner kibana-7.6.1/plugins/customer_analytics muss in den entsprechenden Kibana Ordner auf dem System kopiert werden

Mit den Befehlen
````
./elasticseach
./logstash -f pipeline.conf --config.reload.automatic
./filebeat -e -c filebeat.yml -d "publish"
````
können drei der Komponenten des ELKs gestartet werden.
Um Kibana zu starten muss man in den Plugin Ordner navigieren und 
`````
yarn start
``````
ausführen.

Möchte man die Python Skripte ohne Kibana testen, kann man dies mit 
`````
cd python
python3.7 transform.py
python3.7 associationRuleMiner.py -minsupport=[value] -minconf=[value]
`````
ausführen.



