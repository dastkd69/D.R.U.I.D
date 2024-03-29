# viz.py

import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_entities(self, entities):
        # Add all entities
        self.graph.add_nodes_from(entities)

    def add_relationships(self, relationships):
        # Add all relationships
        for relationship in relationships:
            self.graph.add_edge(relationship[0], relationship[2], name=relationship[1])

    def visualize_graph(self, filename="graph.html"):
        pos = nx.spring_layout(self.graph)
        edge_x = []
        edge_y = []
        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        for node in self.graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='Network graph made with Python',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
        fig.write_html(filename)

    def visualize_wordcloud(self, entities, filename="wordcloud.png"):
        from wordcloud import WordCloud

        text = ' '.join(entity[0] for entity in entities)

        wordcloud = WordCloud(width=800, height=400,
                              background_color='white').generate(text)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(filename)

    def visualize_sentiment_pie(self, sentiment, filename="sentiment_pie_chart.html"):
        labels = ['Negative', 'Neutral', 'Positive']
        values = [len([s for s in sentiment if s < 0]), len([s for s in sentiment if s == 0]),
                  len([s for s in sentiment if s > 0])]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

        fig.update_layout(
            title='Sentiment Distribution',
            annotations=[dict(text='Sentiment', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )

        fig.write_html(filename)
