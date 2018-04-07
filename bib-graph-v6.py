#!//anaconda/bin/python
# python bib-graph.py input_file.bib
# Example: python bib-graph.py "../data/Biblio-perso-globale-fr.bib"

import sys
import yapbib.biblist as biblist
import networkx as nx
from networkx.readwrite import json_graph
import json

from itertools import chain, count
from networkx.utils import make_str

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
#edge_weight = [data.values()[0] for a,b,data in bib_graph.edges(data=True)]

for n in bib_graph:
	bib_graph.node[n]['name'] = n

_attrs = dict(id='id', source='source', target='target', key='key')
def node_link_data_modified(G, attrs=_attrs):
    """Return data in node-link format that is suitable for JSON serialization
    and use in Javascript documents.

    Parameters
    ----------
    G : NetworkX graph

    attrs : dict
        A dictionary that contains four keys 'id', 'source', 'target' and
        'key'. The corresponding values provide the attribute names for storing
        NetworkX-internal graph data. The values should be unique. Default
        value:
        :samp:`dict(id='id', source='source', target='target', key='key')`.

        If some user-defined graph data use these attribute names as data keys,
        they may be silently dropped.

    Returns
    -------
    data : dict
       A dictionary with node-link formatted data.

    Raises
    ------
    NetworkXError
        If values in attrs are not unique.

    Examples
    --------
    >>> from networkx.readwrite import json_graph
    >>> G = nx.Graph([(1,2)])
    >>> data = json_graph.node_link_data(G)

    To serialize with json

    >>> import json
    >>> s = json.dumps(data)

    Notes
    -----
    Graph, node, and link attributes are stored in this format. Note that
    attribute keys will be converted to strings in order to comply with
    JSON.

    The default value of attrs will be changed in a future release of NetworkX.

    See Also
    --------
    node_link_graph, adjacency_data, tree_data
    """
    multigraph = G.is_multigraph()
    id_ = attrs['id']
    source = attrs['source']
    target = attrs['target']
    # Allow 'key' to be omitted from attrs if the graph is not a multigraph.
    key = None if not multigraph else attrs['key']
    if len(set([source, target, key])) < 3:
        raise nx.NetworkXError('Attribute names are not unique.')
    #mapping = dict(zip(G, count()))
    data = {}
    data['directed'] = G.is_directed()
    data['multigraph'] = multigraph
    data['graph'] = G.graph
    data['nodes'] = [dict(chain(G.node[n].items(), [(id_, n)])) for n in G]
    if multigraph:
        data['links'] = [
            dict(chain(d.items(),
                       [(source, u), (target, v), (key, k)]))
            for u, v, k, d in G.edges_iter(keys=True, data=True)]
    else:
        data['links'] = [
            dict(chain(d.items(),
                       [(source, u), (target, v)]))
            for u, v, d in G.edges_iter(data=True)]

    return data

data = node_link_data_modified(bib_graph)
with open('../output/bib-graph.json', 'w') as f:
    json.dump(data, f, indent=4)
