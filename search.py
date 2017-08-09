import fetch_papers.py
import download_pdfs

fetch_papers.fetch_papers(max_index=100,search_query='cat:cs.AI')
download_pdfs.download_pdfs()
