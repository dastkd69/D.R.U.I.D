import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_entities(self, entities):
        # Only add entities of type 'ORG' or 'PRODUCT'
        relevant_entities = [entity for entity in entities if entity[1] in ['ORG', 'PRODUCT']]
        self.graph.add_nodes_from(relevant_entities)

    def add_relationships(self, relationships):
        # Only add relationships between relevant entities
        relevant_relationships = [relationship for relationship in relationships if relationship[0] in self.graph and relationship[2] in self.graph]
        for relationship in relevant_relationships:
            self.graph.add_edge(relationship[0], relationship[2], name=relationship[1])

    def visualize(self):
        pos = nx.spring_layout(self.graph, k=0.5, iterations=20)  # Adjust these parameters to change the layout
        plt.figure(figsize=(10, 10))  # Adjust this parameter to change the size of the figure
        nx.draw(self.graph, pos, edge_color='black', width=1, linewidths=1,
                node_size=500, node_color='seagreen', alpha=0.9,
                labels={node: node for node in self.graph.nodes()})
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=nx.get_edge_attributes(self.graph, 'name'))
        plt.axis('off')
        plt.show()
