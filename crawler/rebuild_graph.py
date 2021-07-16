#!/usr/bin/env python3
import json
import json_lines
from pprint import pprint
import zlib
import csv
import networkx as nx
from networkx.readwrite import json_graph

input_file = 'data/blog.jsonl'
output_dir = 'data/graph_result'


def build_graph(file_name):
    graph = nx.DiGraph()

    # rebuild the Graph from crawled data (json-lines)
    with open(file_name, 'rb') as f:
        for item in json_lines.reader(f):
            node_id = 'page:'+str(item['id'])

            # create Page Node
            if node_id in graph.nodes:
                if 'type' not in graph.nodes[node_id]:
                    graph.nodes[node_id]['type'] = 'page'

                if 'title' not in graph.nodes[node_id]:
                    graph.nodes[node_id]['title'] = item['title']

                if 'url' not in graph.nodes[node_id]:
                    graph.nodes[node_id]['url'] = item['url']

                if 'description' not in graph.nodes[node_id]:
                    graph.nodes[node_id]['description'] = item['title'] + ' ' + item['url']
            else:
                graph.add_node(node_id,
                               type='page',
                               label=node_id,
                               title=item['title'],
                               url=item['url'],
                               description=item['title'] + ' ' + item['url'])

            # create Page Links
            for to_id, to_link in item['links'].items():
                # update destination page node
                to_id = 'page:'+str(to_id)

                if to_id in graph.nodes:
                    if 'type' not in graph.nodes[node_id]:
                        graph.nodes[to_id]['type'] = 'page'
                    if 'url' not in graph.nodes[to_id]:
                        graph.nodes[to_id]['url'] = to_link[0]
                else:
                    graph.add_node(to_id, type='page',label=to_id,url=to_link[0])

                # add link between nodes
                graph.add_edge(node_id, to_id)

                # create/update anchor node
                keyword_id = zlib.crc32(bytes(to_link[1], 'utf-8')) & 0xffffffff
                keyword_id = 'kw:'+str(keyword_id)

                if keyword_id in graph.nodes:
                    if 'type' not in graph.nodes[node_id]:
                        graph.nodes[to_id]['type'] = 'keyword'

                    if 'title' not in graph.nodes[keyword_id]:
                        graph.nodes[keyword_id]['title'] = to_link[1]
                else:
                    graph.add_node(keyword_id,
                                   type='keyword',
                                   label=keyword_id,
                                   title=to_link[1],
                                   url='none',
                                   )

                # create link from page to keyword
                graph.add_edge(keyword_id, to_id)

    # fixing the graph
    removing_nodes = []
    for node_id, data in graph.nodes(data=True):
        if data['type'] == 'page':
            if 'title' not in data or 'url' not in data:
                removing_nodes.append(node_id)
        else:
            if 'title' not in data:
                removing_nodes.append(node_id)

    for node_id in removing_nodes:
        graph.remove_node(node_id)

    return graph


def compute_centrality(graph):
    centrality_values = nx.hits(graph)
    for node_id, centrality in centrality_values[0].items():
        graph.nodes[node_id]['hub'] = centrality
    for node_id, centrality in centrality_values[1].items():
        graph.nodes[node_id]['authority'] = centrality

    centrality_values = nx.pagerank(graph)
    for node_id, centrality in centrality_values.items():
        graph.nodes[node_id]['pagerank'] = centrality

    centrality_values = nx.in_degree_centrality(graph)
    for node_id, centrality in centrality_values.items():
        graph.nodes[node_id]['in_degree'] = centrality

    centrality_values = nx.out_degree_centrality(graph)
    for node_id, centrality in centrality_values.items():
        graph.nodes[node_id]['out_degree'] = centrality

    centrality_values = nx.closeness_centrality(graph)
    for node_id, centrality in centrality_values.items():
        graph.nodes[node_id]['closeness'] = centrality

    centrality_values = nx.betweenness_centrality(graph)
    for node_id, centrality in centrality_values.items():
        graph.nodes[node_id]['betweenness'] = centrality

    centrality_values = nx.pagerank(graph)
    for node_id, centrality in centrality_values.items():
        graph.nodes[node_id]['pagerank'] = centrality



def export_graph(graph, directory):
    # write to GraphML file
    nx.write_graphml(graph, directory + "/blog.graphml")

    # write to Gexf file
    nx.write_gexf(graph, directory + "/blog.gexf")

    # write to JSON file
    json.dump(json_graph.node_link_data(graph), open(directory + '/blog.json', 'w'), indent=2)

    # write to CSV files
    with open(directory + '/blog_nodes.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['id', 'type', 'label', 'title', 'url', 'hub', 'authority', 'pagerank', 'in_degree', 'out_degree', 'closeness', 'betweenness'])
        for node, data in graph.nodes(data=True):
            writer.writerow([node, data['type'], data['label'], data['title'], data['url'],
                             data['hub'], data['authority'], data['pagerank'],
                             data['in_degree'], data['out_degree'],
                             data['closeness'], data['betweenness']])

    with open(directory + '/blog_links.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['from', 'to'])
        for f, t, a in graph.edges(data=True):
            writer.writerow([f, t])


my_graph = build_graph(input_file)
compute_centrality(my_graph)
export_graph(my_graph, output_dir)

# export_centrality(nx.in_degree_centrality(my_graph), my_graph, output_dir, 'in_degree')

