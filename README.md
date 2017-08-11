# arXiv searcher
This is an extension of arXiv-sanity that allows you to index the metadata and full text of arXiv papers in Elastic Cloud and search them using Elasticsearch.

### Usage

1. Run `python3 index_papers.py --search-query cat:cs.AI` to index all arXiv papers in the category cs.AI. You can use the --start-index (default 0) and --max-index flags (default 10,000) to index in batches, as the arXiv API may rate limit you. Relies on `fetch_papers.py` from arXiv-sanity, so see https://github.com/karpathy/arxiv-sanity-preserver#processing-pipeline for more information.
2. Run 'python3 search.py --search-phrase "deep learning"` to search all papers that include the phrase "deep learning" (exact matches). It will save the metadata of matched papers as a json list to the file "deep learning.json".