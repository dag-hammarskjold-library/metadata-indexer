import boto3, elasticsearch

class Config(object):

    ssm = boto3.client('ssm')
    pp_api = ssm.get_parameter(Name='PoolPartyAPI')['Parameter']['Value']
    pp_project = ssm.get_parameter(Name='PoolPartyProjectID')['Parameter']['Value']
    pp_user = ssm.get_parameter(Name='PoolPartyUsername')['Parameter']['Value']
    pp_pass = ssm.get_parameter(Name='PoolPartyPassword')['Parameter']['Value']
    es_uri = ssm.get_parameter(Name='ElasticSearchEndpoint')['Parameter']['Value']

    index_name = 'unbis_thesaurus'

    languages = ['ar','zh','en','fr','ru','es']

    index_settings = {
        "settings": {
            "index": {
                "number_of_shards": 3
            },
            "analysis": {
                "analyzer": {
                    "autocomplete": {
                        "tokenizer": "autocomplete",
                        "filter": [
                            "lowercase"
                        ]
                    },
                    "autocomplete_search": {
                        "tokenizer": "lowercase"
                    }
                },
                "tokenizer": {
                    "autocomplete": {
                        "type": "edge_ngram",
                        "min_gram": 3,
                        "max_gram": 40,
                        "token_chars": [
                            "letter",
                            "digit"
                        ]
                    }
                }
            }
        }
    }

    index_mapping = {
        "properties": {
            "uri": {"type": "text", "index": "false"},
            "labels_ar": {"type": "text", "analyzer": "arabic"},
            "labels_zh": {"type": "text", "analyzer": "chinese"},
            "labels_en": {"type": "text", "analyzer": "autocomplete", "search_analyzer": "autocomplete_search"},
            "labels_fr": {"type": "text", "analyzer": "autocomplete", "search_analyzer": "autocomplete_search"},
            "labels_ru": {"type": "text", "analyzer": "russian"},
            "labels_es": {"type": "text", "analyzer": "autocomplete", "search_analyzer": "autocomplete_search"},
            "alt_labels_ar": {"type": "text", "analyzer": "arabic"},
            "alt_labels_zh": {"type": "text", "analyzer": "chinese"},
            "alt_labels_en": {"type": "text", "analyzer": "autocomplete", "search_analyzer": "autocomplete_search"},
            "alt_labels_fr": {"type": "text", "analyzer": "autocomplete", "search_analyzer": "autocomplete_search"},
            "alt_labels_ru": {"type": "text", "analyzer": "russian"},
            "alt_labels_es": {"type": "text", "analyzer": "autocomplete", "search_analyzer": "autocomplete_search"},
        }
    }

