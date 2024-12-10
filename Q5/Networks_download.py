import osmnx as ox
import shapely
import networkx as nx
import numpy as np
import pandas as pd

# time
# Try to use https://www.keene.edu/campus/maps/tool/ to find the set of suitable coordinates your prefer (in the form of Long, Lat). 
# but please check as it sometimes return wrong coordinates (+-360 degree)
# 144.9592888, -37.8198277
# 144.9561453, -37.8118437
# 144.9687517, -37.8082412
# 144.9724102, -37.8160646

coords = ((144.939, -37.825),
    (144.939, -37.805),
    (144.98, -37.805),
    (144.98, -37.825),
    (144.939, -37.825))
polygon = shapely.Polygon(coords)

# Check https://osmnx.readthedocs.io/en/stable/user-reference.html for other network types that can be downloaded directly.
# You can choose to simplify network or not use the parameter of 'simplify'
# Before simplify 5000+ nodes, after:1000+
graph = ox.graph_from_polygon(polygon, simplify=True, network_type='drive')

ox.graph_to_gdfs(graph, nodes=False).explore()

nx.write_edgelist(graph,'Melbourne_Edgelist.txt')

node_properties = pd.DataFrame.from_dict(dict(graph.nodes(data=True)), orient='index')

node_properties.to_csv('Melbourne_Node.csv')