import argparse
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from utils import Config

def search_papers(search_phrase):
  es = Elasticsearch([{
    'host': Config.host,
    'port': Config.port,
    'use_ssl': True,
    'http_auth': Config.http_auth
  }])

  query = {
    "query": {
      "match_phrase": {
        "_all": search_phrase
      }
    },
    "_source": {
          "includes": [ "metadata" ]
    },
  }

  search_scanner = scan(es, query=query, index='papers', doc_type='paper')
  hits = [hit['_source']['metadata'] for hit in search_scanner]
  with open(search_phrase + '-results', 'w') as f:
    json.dump(hits, f)

  print('Found %d matches.' % (len(hits)))

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--search-phrase', type=str, required=True, help='string phrase to search for')
  args = parser.parse_args()
  search_papers(args.search_phrase)
