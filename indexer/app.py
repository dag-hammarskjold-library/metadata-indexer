from flask import Flask, request, jsonify, abort
from elasticsearch import Elasticsearch
from indexer.config import Config
import requests, json

app = Flask(__name__)
#app.config.from_object(Config)



@app.route('/')
def index():
    history_service = Config.pp_api + 'history/' + Config.pp_project
    es_conn = Elasticsearch(Config.es_uri)
    print(history_service)
    jsresponse = requests.get(history_service, auth=(Config.pp_user, Config.pp_pass), timeout=15)
    if jsresponse.status_code == 200:
        jsdata = json.loads(jsresponse.text)
        return_data = []
        for event in jsdata:
            # Find out if this is already in the ES index
            doc = {
                'size' : 1,
                'query': {
                    'match' : {
                        'uri': event['subjectOfChange']
                    }
                }
            }
            res = es_conn.search(index=Config.index_name, body=doc)
            print(res)
            
            # setup the return data
            return_data.append({
                'uri': event['subjectOfChange'],
                'date': event['createdDate']
            })
        return jsonify(return_data)
    else:
        abort(404)