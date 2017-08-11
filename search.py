import argparse
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan

MAX_SEARCHES = 10000
RESUlTS_SIZE = 1000

def search_papers(search_phrase):
  es = Elasticsearch([{
    'host': '09f7307feaa362c1f38dec4fc8a9f1c2.us-west-1.aws.found.io',
    'port': 9243,
    'use_ssl': True,
    'http_auth': 'elastic:NO69sWlVJi2VGje4OxIQLqMY'
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
