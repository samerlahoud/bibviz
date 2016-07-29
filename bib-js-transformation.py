#!//anaconda/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 13:21:12 2015

@author: Samer Lahoud
"""

import networkx as nx



affiliation=dict()

affiliation['M. Molnar']=1
affiliation['D. Mezher']=2
affiliation['G. Bergmann']=3
affiliation['B. Cousin']=1
affiliation['G. Bertrand']=4
affiliation['M. Ibrahim']=2
affiliation['A. Frikha']=1
affiliation['S. Tohme']=5
affiliation['S. Said']=1
affiliation['R. Douville']=6
affiliation['A. Adouane']=5
affiliation['L. Gonczy']=3
affiliation['S. Jawhar']=1
affiliation['A. Bellabas']=1
affiliation['H. Drid']=1
affiliation['A. Belghith']=1
affiliation['N. Sauze']=6
affiliation['E. Salhi']=1
affiliation['M. Helou']=2
affiliation['M. Yassin']=1
affiliation['G. Texier']=4
affiliation['H. Pouyllau']=6
affiliation['Y. Dirani']=2
affiliation['P. Muhlethaler']=7
affiliation['K. Khawam']=5
affiliation['E. Sourour']=8
affiliation['S. Farhat']=9
affiliation['F. Moety']=1
affiliation['A. Samhat']=9
affiliation['A. Najah']=10
affiliation['L. Toutain']=4
affiliation['N. Djarallah']=6
affiliation['S. Lahoud']=1
affiliation['J. Cohen']=5
affiliation['M. AboulHassan']=8

bib_graph=nx.read_gml("../output/gml-graph2015.gml")

for n in bib_graph.nodes():
	#print bib_graph.node[n]['label']
	print '{{id:{}, label: "{}", value:{}, group:{}}},'.format(n, bib_graph.node[n]['label'], bib_graph.node[n]['weight'], affiliation[bib_graph.node[n]['label']])

for (u,v,d) in bib_graph.edges(data=True):
	print '{{from: {}, to: {}, "value": {}, dashes:true}},'.format(u, v, d['weight'])