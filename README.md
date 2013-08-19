biblio-viz
==========

Bibviz is an automatic tool that enables to visualise co-authorship relations in a bibliography file. 
Starting from a bibliography file in BibTex format, the tool transforms it into a graph, where nodes represent authors and links the co-authorship relations.
What you need is simply a clean installation of some python tools:
- biblio-py
- networkx
- matplotlib
and my source code available on GitHub !
You can see in Figure 1 a dynamic view of my bibliography file. Node size represents connectivity and link colour represents the number of co-authorships (scaling from light blue to red). Figure 2 represents another sample output processed by Gephi.

A bibliography visualisation tool
# python bib-graph.py input_file.bib min_year max_year