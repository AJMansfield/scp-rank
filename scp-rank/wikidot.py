#!/usr/bin/python3

import pyscp
import itertools
import pickle
from tqdm import tqdm
import requests

# from joblib import Parallel, delayed
# import concurrent.futures as cf
import multiprocessing as mp






def all_vote_data(pages):
	for page in tqdm(pages):
		for vote in vote_data(page):
			yield vote

def vote_data(page):
	try:
		for vote in page.votes:
			yield(page.name, vote.user, vote.value)
	except:
	 	pass

def vote_data_array(page):
	return [v for v in vote_data(page)]




def get_control(source, default):
	import pyparsing as pp

	d = default.copy()

	def add_item(i):
		d[i[0].lower()] = i[1].lower()

	start = pp.CaselessLiteral("[!--").suppress()
	idTag = pp.CaselessLiteral("scprank").suppress()
	end = pp.CaselessLiteral("--]").suppress()
	item = pp.Word(pp.alphanums) + pp.CaselessLiteral(":").suppress() + pp.Word(pp.alphanums)
	item = item.setParseAction(add_item)

	section = start + idTag + pp.ZeroOrMore(item) + end

	section.scanString(source)

	return d

def all_aux_data(pages):
	for page in tqdm(pages):
		yield aux_data(page)

def aux_data(page):
	try:
		return (page.name, page.title, page.tags, page.text, get_control(page.source))
	except:
	 	pass




if __name__ == '__main__':
	wiki = pyscp.wikidot.Wiki('www.scp-wiki.net')
	wiki.req = requests.Session()
	# pages = [p for p in tqdm(wiki.list_pages(), total=7000)]
	with open('pages.pkl', 'rb') as input:
		pages = pickle.load(input)

	tc = 16

	with mp.Pool(tc) as p:
		votes = [ v for v in itertools.chain(*p.map(vote_data_array, tqdm(pages), chunksize=10)) ]
	with open('votes.pkl', 'wb') as output:
		pickle.dump(votes, output, protocol=2)

	with mp.Pool(tc) as p:
		aux = p.map(aux_data, tqdm(pages), chunksize=10)
	with open('aux.pkl', 'wb') as output:
		pickle.dump(aux, output, protocol=2)

