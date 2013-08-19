#!/usr/local/bin/python
# python bib-stat-v1.py "./data/Biblio-perso-globale.bib" 2005 2011

import sys
import yapbib.biblist as biblist
import matplotlib.pyplot as plt
import numpy as np

bibfile_input=sys.argv[1]
min_year_input=int(sys.argv[2])
max_year_input=int(sys.argv[3])
year_range=range(min_year_input, max_year_input+1)

bib_handle=biblist.BibList()
bib_handle.import_bibtex(bibfile_input, normalize=False)

nb_inproceedings={}
nb_article={}
nb_phdthesis={}
nb_inbook={}
nb_techreport={}
nb_misc={}

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%d'%int(height), ha='center', va='bottom')
                
for year_idx in year_range:
	nb_inproceedings[year_idx]=0
	nb_article[year_idx]=0
	nb_phdthesis[year_idx]=0
	nb_inbook[year_idx]=0
	nb_techreport[year_idx]=0
	nb_misc[year_idx]=0

items= bib_handle.List() # Shows the keys of all entries

for item_index in items:
	item_handle = bib_handle.get_item(item_index) 
	item_year = int(item_handle.get('year'))  
	if item_year not in year_range:
		continue
		
	if item_handle.get_type() == 'inproceedings':
		nb_inproceedings[item_year] = nb_inproceedings[item_year]+1
	if item_handle.get_type() == 'article':
		nb_article[item_year] = nb_article[item_year]+1
	if item_handle.get_type() == 'phdthesis':
		nb_phdthesis[item_year] = nb_phdthesis[item_year]+1
	if item_handle.get_type() == 'inbook':
		nb_inbook[item_year] = nb_inbook[item_year]+1
	if item_handle.get_type() == 'techreport':
		nb_techreport[item_year] = nb_techreport[item_year]+1		
	if item_handle.get_type() == 'misc':
		nb_misc[item_year] = nb_misc[item_year]+1
		
#print nb_inproceedings, nb_article, nb_phdthesis, nb_inbook, nb_techreport, nb_misc 

width = 0.2
ind = np.arange(len(year_range))  # the x locations for the groups

p1 = plt.bar(ind, nb_inproceedings.values(), width, color='r')
p2 = plt.bar(ind+width, nb_article.values(), width, color='g')
p3 = plt.bar(ind+width*2, nb_phdthesis.values(), width, color='b')
p4 = plt.bar(ind+width*3, nb_inbook.values(), width, color='y')

plt.ylabel('Number of publications')
plt.xlabel('Year')
plt.title('Bilbiometer - ATNET team')
plt.xticks(ind+width*2, year_range)
plt.yticks(range(0,30,2))
plt.legend((p1[0], p2[0], p3[0], p4[0]), ('In Proceedings', 'Article', 'PhD Thesis', 'Book Chapter'))

autolabel(p1)
autolabel(p2)
#autolabel(p3)
#autolabel(p4)
plt.show()		
 