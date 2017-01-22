#!/usr/bin/python2.7

import pickle
import graphlab
import os


print "Processing votes ..."
with open('votes.pkl', 'rb') as input:
	votedata = zip(* filter(None, pickle.load(input)) )

votedata[2] = map(lambda x:x if x!= -1 else 0, votedata[2])

votes = graphlab.SFrame({'item_id':votedata[0], 'user_id':votedata[1], 'rating':votedata[2]})
del votedata


print "Processing tags ..."
with open('aux.pkl', 'rb') as input:
	auxdata = zip(* filter(None, pickle.load(input)) )

aux = graphlab.SFrame(
	{'item_id':auxdata[0],
	'title':auxdata[1],
	'tags':auxdata[2],
	'text':auxdata[3],
	'options':auxdata[4]})
del auxdata

titles = aux[['item_id','title']].to_dataframe().set_index('item_id').to_dict(orient='dict')['title']

aux = aux.unpack('options')


aux = aux.filter_by(['all'], 'options.opt')
votes = votes.filter_by(aux['item_id'], 'item_id')


tags = graphlab.toolkits.feature_engineering.OneHotEncoder(features='tags').fit_transform(aux[['item_id','tags']])


print "Fitting model ..."
model =	graphlab.factorization_recommender.create(
		observation_data=votes, target='rating',
		item_data=tags, binary_target=True)


print "Generating recommendations ..."
links = model.get_similar_items(k=2)
links = links.groupby('item_id', {'similar': graphlab.aggregate.CONCAT('similar')})


print "Writing files ...."

template = u"""---
style: default
permalink: X{0}
title: {1}
---
You may also like:

[{3}](http://scp-wiki.net/{2})

[{5}](http://scp-wiki.net/{4})
"""

folder = 'recs/'
for the_file in os.listdir(folder):
	file_path = os.path.join(folder, the_file)
	try:
		if os.path.isfile(file_path):
			os.unlink(file_path)

	except Exception as e:
		print(e)


for link in links:
	with open('recs/{}.md'.format(link['item_id']), 'w') as out:
		try:
			out.write(template.format(link['item_id'], link['item_id'], 
				link['similar'][0], titles[link['similar'][0]],
				link['similar'][1], titles[link['similar'][1]]))
		except:
			os.unlink(out.name)

