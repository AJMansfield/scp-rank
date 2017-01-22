#!/usr/bin/python2.7

import pickle
import graphlab
import os


print "Processing votes ..."
with open('votes.pkl', 'rb') as inpt:
	votedata = zip(* pickle.load(inpt) )

votedata[2] = map(lambda x:x if x!= -1 else 0, votedata[2])

votes = graphlab.SFrame({'item_id':votedata[0], 'user_id':votedata[1], 'rating':votedata[2]})
del votedata


print "Processing tags ..."
with open('aux.pkl', 'rb') as inpt:
	auxdata = zip(* pickle.load(inpt) )

aux = graphlab.SFrame(
	{'item_id':auxdata[0],
	'title':auxdata[1],
	'tags':auxdata[2],
	'text':auxdata[3],
	'options':auxdata[4]})
del auxdata

# tags = graphlab.SFrame({'item_id':auxdata[0], 'tags':auxdata[2]})
# tags_encoded = graphlab.toolkits.feature_engineering.OneHotEncoder(features='tags').fit_transform(tags)

# data = {a: b for a,b in zip(auxdata[0], auxdata[1])}

# print "Fitting model ..."
# rec = graphlab.factorization_recommender.create(
# 	observation_data=votes, target='rating',
# 	item_data=tags, binary_target=True,
# 	num_factors=30, max_iterations=100)



# print "Generating recommendations ..."
# links = rec.get_similar_items(k=2)
# links = links.groupby('item_id', {'similar': graphlab.aggregate.CONCAT('similar')})


# print "Writing files ...."
# template = u"""---
# style: default
# permalink: X{0}
# title: {1}
# ---
# You may also like:

# [{3}](http://scp-wiki.net/{2})

# [{5}](http://scp-wiki.net/{4})
# """

# for link in links:
# 	with open('recs/{}.md'.format(link['item_id']), 'w') as out:
# 		try:
# 			out.write(template.format(link['item_id'], link['item_id'], 
# 				link['similar'][0], titles[link['similar'][0]],
# 				link['similar'][1], titles[link['similar'][1]]))
# 		except:
# 			os.unlink(out.name)


