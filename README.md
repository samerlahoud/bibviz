bibviz
=======

Bibviz is an automatic tool that enables to visualise co-authorship relations in a bibliography file. 
Starting from a bibliography file in BibTex format, the tool transforms it into a graph, where nodes represent authors and links the co-authorship relations.
What you need is simply a clean installation of some python tools:
- biblio-py
- networkx
- matplotlib
and my source code available on this page !

Take a look on this blog post for details:
http://addroute.lahoud.fr/2012/10/bibliography-visualisation/

Example
=======
python bib-graph.py input_file.bib min_year max_year
