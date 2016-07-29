#!//anaconda/bin/python
# python bib-graph.py input_file.bib min_year max_year
# Example: python bib-graph.py "../data/Biblio-perso-globale-fr.bib" 2005 2015

import sys
import yapbib.biblist as biblist
import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph
import os

bibfile_input=sys.argv[1]
min_year_input=int(sys.argv[2])
max_year_input=int(sys.argv[3])

bib_handle=biblist.BibList()
bib_handle.import_bibtex(bibfile_input, normalize=False)

items= bib_handle.List() # Shows the keys of all entries

for year_iter in range(max_year_input, min_year_input-1, -1):
	bib_graph=nx.Graph()
	pos=dict()
	for item_index in items:
		item_handle = bib_handle.get_item(item_index) 
		item_year = int(item_handle.get('year'))  

		if item_year > year_iter:
			continue
			
		for author_index, author_handle in enumerate(item_handle.get_authorsList()[:len(item_handle.get_authorsList())-1]):
			clean_author_handle = str(author_handle)
			for next_author_index, next_author_handle in enumerate(item_handle.get_authorsList()[author_index+1:]):
				clean_next_author_handle = str(next_author_handle)
				if bib_graph.get_edge_data(clean_author_handle, clean_next_author_handle, default=0):
					bib_graph[clean_author_handle][clean_next_author_handle]['weight'] = bib_graph[clean_author_handle][clean_next_author_handle]['weight'] + 1
				else:
					bib_graph.add_edge(clean_author_handle, clean_next_author_handle, weight = 1)
	
	# bib_graph is bidirectional but edge list of a node gives only one of the incident edges	
	for n in bib_graph:
		temp_node_weight = 0
		for e in bib_graph.edges_iter(n):
			if e in bib_graph.edges():
				temp_node_weight = temp_node_weight + nx.get_edge_attributes(bib_graph,'weight')[e]
			else:
				temp_node_weight = temp_node_weight + nx.get_edge_attributes(bib_graph,'weight')[e[1],e[0]]
		bib_graph.node[n]['weight'] = temp_node_weight
		
	node_weight=[data.values()[0]*2.5 for n,data in bib_graph.nodes(data=True)]
	edge_weight = [data.values()[0] for a,b,data in bib_graph.edges(data=True)] 
 
	data = json_graph.node_link_data(bib_graph)
	json_output_file = open("../output/json-graph%s.json" %year_iter, 'w')	
	json_output_file.write(str(data))
	
	fig = plt.figure(1, figsize=(8, 8))
	if year_iter == max_year_input:
		init_pos=nx.pydot_layout(bib_graph)
	for node in bib_graph:
		pos[node] = init_pos[node]
	nx.draw_networkx(bib_graph, pos, node_size=node_weight, node_color=node_weight, edge_color=edge_weight, cmap=plt.cm.OrRd, font_size=9)
	
	if year_iter == max_year_input:
		xmax=max(xx for xx,yy in pos.values())
		xmin=min(xx for xx,yy in pos.values())
		ymax=max(yy for xx,yy in pos.values())
		ymin=min(yy for xx,yy in pos.values())
		dx = xmax - xmin
		ddx=0.1*dx
		dy = ymax - ymin
		ddy=0.1*dy
	plt.hold(False)
	plt.xlim(xmin-ddx,xmax+ddx)
	plt.ylim(ymin-ddy,ymax+ddy)
	plt.title('Bibliography Graph %s' %year_iter)
	plt.axis('off')
	plt.savefig("../output/bib-graph%s.png" %year_iter)  # save as png
	
	# Uncomment for more output formats
	#nx.write_graphml(bib_graph, './output/biblio-perso-globale%s.graphml' %year_iter)
	#nx.write_gml(bib_graph, './output/biblio-perso-globale.gml')
	#nx.write_graphml(bib_graph, './output/biblio-perso-globale.graphml')
	#plt.show() # display
	
input = "../output/bib-graph????.png"
output = "../output/bib-animation.gif"
os.system("convert -delay 100 -loop 0 %s %s" % (input, output))