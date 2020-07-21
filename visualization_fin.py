import numpy as np
import pandas as pd
import holoviews as hv
hv.extension('bokeh')

def draw_network_graph(file_path):
    df = pd.read_csv(file_path)
    print(df)
    exit()
    # Data
    edges_df = pd.read_csv('../../../assets/fb_edges.csv')
    nodes_df = pd.read_csv('../../../assets/fb_nodes.csv')

    fb_nodes = hv.Nodes(nodes_df).sort()
    fb_graph = hv.Graph((edges_df, fb_nodes), label='Facebook Circles')

    # Plot
    colors = ['#000000']+hv.Cycle('Category20').values
    fb_graph = fb_graph.redim.range(x=(-0.05, 1.05), y=(-0.05, 1.05))
    
    fb_graph.opts(color_index='circle', width=800, height=800, show_frame=False,
                    xaxis=None, yaxis=None,node_size=10, edge_line_width=1, cmap=colors)
    return

if __name__ == "__main__":
    draw_network_graph("./transaction/experiment/experiment.csv")