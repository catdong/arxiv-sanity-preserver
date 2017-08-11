import json
import os
import pickle
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import fetch_papers
import download_pdfs
import parse_pdf_to_text
import argparse

from utils import Config

def index_papers(search_query, start_index, max_index):
  fetch_papers.fetch_papers(
    search_query=search_query,
    start_index=start_index,
    max_index=max_index
  )
  download_pdfs.download_pdfs()
  parse_pdf_to_text.parse_pdf_to_text()

  es = Elasticsearch([{
    'host': '09f7307feaa362c1f38dec4fc8a9f1c2.us-west-1.aws.found.io',
    'port': 9243,
    'use_ssl': True,
    'http_auth': 'elastic:NO69sWlVJi2VGje4OxIQLqMY'
  }])

  bulk_actions = []

  db = pickle.load(open(Config.db_path, 'rb'))
  for pid, metadata in db.items():
    doc = {}
    doc['metadata'] = metadata
    txt_path = os.path.join(Config.txt_dir, metadata['id'].split('/')[-1] + '.pdf.txt')
    if os.path.isfile(txt_path): # some pdfs dont translate to txt
      print("found %s." % (txt_path,))
      with open(txt_path, 'r') as f:
        txt = f.read()
        doc['full_text'] = txt

        action = {
          '_op_type': 'index',
          '_index': 'papers',
          '_type': 'paper',
          '_id': pid
        }
        action.update(doc)
        bulk_actions.append(action)

    else:
      print("could not find %s." % (txt_path, ))

  print('Bulk indexing...')
  print(bulk(es, bulk_actions, request_timeout=30))

if __name__ == "__main__":

  # parse input arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('--search_query', type=str,
                      default='cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML',
                      help='query used for arxiv API, e.g. "cat:cs.AI". Defaults to all CS papers.'
                           'See http://arxiv.org/help/api/user-manual#detailed_examples')
  parser.add_argument('--start-index', type=int, default=0, help='0 = most recent API result')
  parser.add_argument('--max-index', type=int, default=10000, help='upper bound on paper index we will fetch')
  args = parser.parse_args()
  index_papers(args.categories, args.start_index, args.max_index)
