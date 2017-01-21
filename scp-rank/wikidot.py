#!/usr/bin/python3

import pyscp
import itertools
import pickle
from tqdm import tqdm
from bs4 import BeautifulSoup

#wiki = pyscp.wikidot.Wiki('www.scp-wiki.net')

#pages = [p for p in tqdm(wiki.list_pages(), total=7000)]
with open('pages.pkl', 'rb') as input:
	pages = pickle.load(input)

# def vote_tuples(pages):
# 	for page in tqdm(pages):
# 		try:
# 			for vote in page.votes:
# 				yield (page.name, vote.user, vote.value)
# 		except:
# 			pass


# votes = [v for v in vote_tuples(pages)]

# with open('votes.pkl', 'wb') as output:
# 	pickle.dump(votes, output, protocol=2)



def page_tags(pages):
	for page in tqdm(pages):
		try:
			soup = BeautifulSoup(page.html, 'lxml')
			content = soup.find('div', id='page-content')
			content.find('div', class_='page-rate-widget-box').decompose()
			yield (page.name, page.title, page.tags, content.text)
		except:
			pass


tags = [t for t in page_tags(pages)]

with open('aux.pkl', 'wb') as output:
	pickle.dump(tags, output, protocol=2)