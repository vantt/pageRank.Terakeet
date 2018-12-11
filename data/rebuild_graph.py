#!/usr/bin/env python
import json
import json_lines
import networkx as nx
from networkx.readwrite import json_graph

G=nx.DiGraph()

with open('sitecrawl.json', 'rb') as f:
    for item in json_lines.reader(f):
        G.add_node(str(item['id']), title=item['title'], url=item['url'], description=item['title'] + ' ' + item['url'])

        for to_id, to_link in item['links'].items():
            G.add_edge(str(item['id']), str(to_id))

# write to GraphML file
nx.write_graphml(G, "sitegraph.graphml")

json.dump(json_graph.node_link_data(G), open('sitegraph.json', 'w'), indent=2)
# write to JSON file
