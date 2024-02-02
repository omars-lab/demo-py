import plotly.graph_objects as go
import igraph
from igraph import Graph, EdgeSeq

# * https://plotly.com/python/tree-plots/
# * https://dash.plotly.com/tutorial
# * https://python.igraph.org/en/stable/tutorial.html#layout-algorithms

def descriptionForLabel(graph_def, node):
    return graph_def["nodeMetadata"].get(node, {"description": node})["description"]
    #     return f"This is a long desc for node {node}"

def innerTextForNode(graph_def, nodeIndex):
    return graph_def["nodeMetadata"].get(graph_def["nodes"][nodeIndex], {"innerText": graph_def["nodes"][nodeIndex]})["innerText"]
#     return f"{labels[node]}(1)"

def make_annotations(graph_def, pos, text, y_shifter, font_size=10, font_color='rgb(250,250,250)'):
    L=len(pos)
    if len(text)!=L:
        raise ValueError('The lists pos and text must have the same len')
    annotations = []
    for k in range(L):
        annotations.append(
            dict(
                text=innerTextForNode(graph_def, k), # or replace labels with a different list for the text within the circle
                x=pos[k][0], 
                y=y_shifter(pos[k][1]),
                xref='x1',
                yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False
            )
        )
    return annotations

def buildGraph(nodes, edges):
    g = Graph()
    nodeMapping = dict([(y, x) for x, y in enumerate(nodes)])
    g.add_vertices(len(nodes))
    g.add_edges([
        (nodeMapping[node_a], nodeMapping[node_b]) 
        for node_a, nodes in edges.items() 
        for node_b in nodes
    ])
    return g

def visualize_graph_as_tree(graph_def):
    # Make a list of nodes
    labels = graph_def["nodes"]
    nr_vertices = len(labels)
    v_label = list(map(str, range(nr_vertices)))
    
    # Build graph
    G = buildGraph(
        graph_def["nodes"],
        graph_def["edges"]
    )
    lay = G.layout('tree', root=[0])
    position = {k: lay[k] for k in range(nr_vertices)}

    # Get the highest y value of the layout amoungst the nodes
    Y = [lay[k][1] for k in range(nr_vertices)]
    M = max(Y)
    y_shifter=lambda y: 2*M-y

    # Build edges
    es = EdgeSeq(G) # sequence of edges
    E = [e.tuple for e in G.es] # list of edges

    L = len(position)

    # Figure out where the nodes are ...
    Xn = [position[k][0] for k in range(L)]
    Yn = [y_shifter(position[k][1]) for k in range(L)]
    
    # Figure out where the edge lines are ...
    Xe = []
    Ye = []
    for edge in E:
        Xe+=[position[edge[0]][0],position[edge[1]][0], None]
        Ye+=[y_shifter(position[edge[0]][1]),y_shifter(position[edge[1]][1]), None]

    fig = go.Figure()
    # Add lines/edges
    fig.add_trace(
        go.Scatter(
            x=Xe,
            y=Ye,
            mode='lines',
            line=dict(color='rgb(210,210,210)', width=1),
            hoverinfo='none'
        )
    )
    # Draw nodes ...
    fig.add_trace(
        go.Scatter(
            x=Xn,
            y=Yn,
            mode='markers',
            name='bla',
            marker=dict(
                symbol='circle-dot',
                size=42,
                color='#6175c1', #'#DB4551',
                line=dict(color='rgb(50,50,50)', width=1)
            ),
            text=[descriptionForLabel(graph_def, l) for l in labels],
            hoverinfo='text',
            opacity=0.8
        )
    )
    axis = dict(
        showline=False, # hide axis line, grid, ticklabels and  title
        zeroline=False,
        showgrid=False,
        showticklabels=False,
    )
    fig.update_layout(
        title=graph_def["title"],
        annotations=make_annotations(graph_def, position, v_label, y_shifter=y_shifter),
        font_size=8,
        showlegend=False,
        xaxis=axis,
        yaxis=axis,
        margin=dict(l=40, r=40, b=85, t=100),
        hovermode='closest',
        plot_bgcolor='rgb(248,248,248)'
    )
    return fig