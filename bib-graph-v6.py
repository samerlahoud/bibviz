#!//anaconda/bin/python
# python bib-graph.py input_file.bib
# Example: python bib-graph.py "../data/Biblio-perso-globale-fr.bib"

import sys
import yapbib.biblist as biblist
import networkx as nx
from networkx.readwrite import json_graph
import json

bibfile_input=sys.argv[1]

bib_handle=biblist.BibList()
bib_handle.import_bibtex(bibfile_input, normalize=False)

items= bib_handle.List() # Shows the keys of all entries

bib_graph=nx.Graph()
pos=dict()
for item_index in items:
	item_handle = bib_handle.get_item(item_index)

	for author_index, author_handle in enumerate(item_handle.get_authorsList()[:len(item_handle.get_authorsList())-1]):
		#print author_handle
		clean_author_handle = str(author_handle)
		firstname_initial = clean_author_handle.split()[0][0]
		lastname = clean_author_handle.split()[-1]
		clean_author_handle = firstname_initial+'. '+lastname
		for next_author_index, next_author_handle in enumerate(item_handle.get_authorsList()[author_index+1:]):
			clean_next_author_handle = str(next_author_handle)
			firstname_initial = clean_next_author_handle.split()[0][0]
			lastname = clean_next_author_handle.split()[-1]
			clean_next_author_handle = firstname_initial+'. '+lastname
			if bib_graph.get_edge_data(clean_author_handle, clean_next_author_handle, default=0):
				bib_graph[clean_author_handle][clean_next_author_handle]['weight'] = bib_graph[clean_author_handle][clean_next_author_handle]['weight'] + 1
			else:
				bib_graph.add_edge(clean_author_handle, clean_next_author_handle, weight = 1)

# for n in bib_graph.nodes():
#     bib_graph.node[n]['weight'] = 0
# 
# for n1,n2 in bib_graph.edges():
#     bib_graph.node[n1]['weight'] = bib_graph.node[n1]['weight'] + nx.get_edge_attributes(bib_graph,'weight')[n1,n2]
#     bib_graph.node[n2]['weight'] = bib_graph.node[n2]['weight'] + nx.get_edge_attributes(bib_graph,'weight')[n1,n2]
    
for n,deg in bib_graph.degree():
    bib_graph.node[n]['degree'] = deg

# node_weight=[data.values()[0]*2.5 for n,data in bib_graph.nodes(data=True)]
# edge_weight = [data.values()[0] for a,b,data in bib_graph.edges(data=True)]

for n in bib_graph:
	bib_graph.node[n]['name'] = n

data = nx.node_link_data(bib_graph)
with open('../output/bib-graph.json', 'w') as f:
    json.dump(data, f, indent=4)
