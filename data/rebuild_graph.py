#!/usr/bin/env python
import json
import json_lines
import csv
import networkx as nx
from networkx.readwrite import json_graph

G=nx.DiGraph()

with open('sitecrawl.json', 'rb') as f:
    for item in json_lines.reader(f):
        G.add_node(str(item['id']), title=item['title'], url=item['url'], description=item['title'] + ' ' + item['url'])

        for to_id, to_url in item['links'].items():
            to_id = str(to_id)
            if to_id in G.nodes:
                if not G.nodes[to_id]['url']:
                    G.nodes[to_id]['url'] = to_url
            else:
                G.add_node(to_id, url=to_url, description=to_url)

            G.add_edge(str(item['id']), to_id)

# write to GraphML file
nx.write_graphml(G, "sitegraph.graphml")

# write to JSON file
json.dump(json_graph.node_link_data(G), open('sitegraph.json', 'w'), indent=2)

# write to CSV files
with open('pages.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile);

with open('pages_links.csv', 'wb') as csvfile:
    fieldnames = ['from', 'to']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
