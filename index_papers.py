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
  fetch_papers.fetch_papers(search_query=search_query, start_index=start_index, max_index=max_index)
  download_pdfs.download_pdfs()
  parse_pdf_to_text.parse_pdf_to_text()

  es = Elasticsearch([{
    'host': Config.host,
    'port': Config.port,
    'use_ssl': True,
    'http_auth': Config.http_auth
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

        # Elasticsearch bulk index action
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
  print(bulk(es, bulk_actions, request_timeout=30)) # bulk index all docs
  os.system('rm %s' % (os.path.join(Config.txt_dir, '*'))) # delete the text files after indexing
  os.system('rm %s' % (Config.db_path)) # delete the database so we don't re-index the same PDFs next time

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--search-query', type=str,
                      default='cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML',
                      help='query used for arxiv API, e.g. "cat:cs.AI". Defaults to all CS papers.'
                           'See http://arxiv.org/help/api/user-manual#detailed_examples')
  parser.add_argument('--start-index', type=int, default=0, help='0 = most recent API result')
  parser.add_argument('--max-index', type=int, default=10000, help='upper bound on paper index we will fetch')
  args = parser.parse_args()
  index_papers(args.search_query, args.start_index, args.max_index)
