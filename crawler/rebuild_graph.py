#!/usr/bin/env python3
import json
import json_lines
import csv
import networkx as nx
from networkx.readwrite import json_graph

input_file = 'data/fsBlog.jsonl'
output_dir = 'data/graph_result'
G = nx.DiGraph()

# rebuild the Graph from crawled data (json-lines)
with open(input_file, 'rb') as f:
    for item in json_lines.reader(f):
        node_id = str(item['id'])

        # create Node
        if node_id in G.nodes:
            if 'title' not in G.nodes[node_id]:
                G.nodes[node_id]['title'] = item['title']

            if 'url' not in G.nodes[node_id]:
                G.nodes[node_id]['url'] = item['url']

            if 'description' not in G.nodes[node_id]:
                G.nodes[node_id]['description'] = item['title'] + ' ' + item['url']
        else:
            G.add_node(node_id, title=item['title'], url=item['url'], description=item['title'] + ' ' + item['url'])

        # create Links
        for to_id, to_url in item['links'].items():
            to_id = str(to_id)

            if to_id in G.nodes:
                if not G.nodes[to_id]['url']:
                    G.nodes[to_id]['url'] = to_url
            else:
                G.add_node(to_id, url=to_url)

            G.add_edge(node_id, to_id)

    # fixing the graph
    removing_nodes = []
    for node, data in G.nodes(data=True):
        if 'title' not in data or 'url' not in data:
            removing_nodes.append(node)

    for node in removing_nodes:
        G.remove_node(node)

# write to GraphML file
nx.write_graphml(G, output_dir + "/fsBlog.graphml")

# write to Gexf file
nx.write_gexf(G, output_dir + "/fsBlog.gexf")

# write to JSON file
json.dump(json_graph.node_link_data(G), open(output_dir + '/fsBlog.json', 'w'), indent=2)

# write to CSV files
with open(output_dir + '/fsBlog_pages.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['label', 'title', 'url'])
    for node, data in G.nodes(data=True):
        writer.writerow([node, data['title'], data['url']])

with open(output_dir + '/fsBlog_pages_links.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['from', 'to'])
    for f, t, a in G.edges(data=True):
        writer.writerow([f, t])
