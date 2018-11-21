import networkx as nx
import json
from networkx.readwrite import json_graph
import re

G=nx.read_graphml('complete-graph.graphml')
data = json_graph.node_link_data(G)

for node in data['nodes']:
  str=node['id']
  node['id']=[int(s) for s in str.split("n") if s.isdigit()][0]

for link in data['links']:
  str=link['source']
  link['source']=[int(s) for s in str.split("n") if s.isdigit()][0]
  str=link['target']
  link['target']=[int(s) for s in str.split("n") if s.isdigit()][0]

with open('complete-graph.json', 'w') as f:
  json.dump(data, f, indent=4)