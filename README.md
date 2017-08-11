# arXiv searcher
This is an extension of arXiv-sanity that allows you to index the metadata and full text of arXiv papers in Elastic Cloud and search them using Elasticsearch.

### Usage

1. Run `python3 index_papers.py --search_query cat:cs.AI` to index all arXiv papers in the category cs.AI.
2. Run 'python3 search.py --search-phrase "deep learning"` to search all papers that include the phrase "deep learning" (exact matches). It will save the metadata of matched papers as a json list to the file "deep learning.json".