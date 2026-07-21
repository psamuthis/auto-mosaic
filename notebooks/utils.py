import math

import geopandas as gpd
import networkx as nx
from shapely.geometry import LineString, Point
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


import networkx as nx
from shapely.geometry import LineString, MultiLineString
import matplotlib.pyplot as plt
import numpy as np


def explode_geometry(geom):
    """
    Takes any geometry (LineString or MultiLineString)
    Returns a list of individual segment LineStrings
    i.e. (A,B,C,D) -> (A,B), (B,C), (C,D)
    """
    segments = []

    # Level 1: Handle MultiLineString
    if geom.geom_type == "MultiLineString":
        lines = list(geom.geoms)  # Get individual LineStrings
    else:
        lines = [geom]  # Already a LineString

    # Level 2: Explode each LineString into segments
    for line in lines:
        if line.geom_type == "LineString":
            coords = list(line.coords)
            print(coords)
            for i in range(len(coords) - 1):
                segment = LineString([coords[i], coords[i + 1]])
                segments.append(segment)

    return segments


import networkx as nx
from shapely.geometry import LineString


def build_graph_from_segments(segments_gdf):
    """
    Build a NetworkX graph from a GeoDataFrame of line segments.

    Each segment becomes an edge in the graph. Nodes are the endpoints of segments.
    Segments that share endpoints will be connected in the graph.

    Args:
        segments_gdf (geopandas.GeoDataFrame): GeoDataFrame containing only LineString
                                              geometries (each row is a single segment)

    Returns:
        networkx.Graph: A graph where:
            - Nodes are coordinate tuples (x, y)
            - Edges have attributes:
                - 'weight': length of the segment (for shortest path)
                - 'geometry': the LineString geometry of the segment
                - 'edge_id': index of the segment in the original GeoDataFrame
    """
    G = nx.Graph()

    # Iterate through each segment
    for idx, row in segments_gdf.iterrows():
        geom = row.geometry

        # Safety check: ensure it's a LineString
        if not isinstance(geom, LineString):
            continue

        # Get the coordinates of the segment's endpoints
        coords = list(geom.coords)

        # A valid LineString should have at least 2 points
        if len(coords) < 2:
            continue

        start_node = coords[0]  # First vertex
        end_node = coords[-1]  # Last vertex (for a segment, this is the second point)

        # Calculate segment length (as weight for routing)
        weight = geom.length

        # Add edge to graph with attributes
        G.add_edge(start_node, end_node, weight=weight, geometry=geom, edge_id=idx)

    return G


def plot_graph_simple(
    G, figsize=(16, 10), node_size=0.1, edge_width=0.5, title="Graph"
):
    """
    A simpler plotting function that avoids colormap issues.
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Get node positions
    pos = {}
    for node, data in G.nodes(data=True):
        if "coord" in data:
            pos[node] = (data["coord"][0], data["coord"][1])
        elif "x" in data and "y" in data:
            pos[node] = (data["x"], data["y"])

    # Plot edges with geometry
    for u, v, data in G.edges(data=True):
        if "geometry" in data and data["geometry"] is not None:
            coords = data["geometry"].coords
            x = [c[0] for c in coords]
            y = [c[1] for c in coords]
            ax.plot(x, y, color="red", linewidth=edge_width, alpha=0.9)
        elif u in pos and v in pos:
            ax.plot(
                [pos[u][0], pos[v][0]],
                [pos[u][1], pos[v][1]],
                color="red",
                linewidth=edge_width,
                alpha=0.9,
            )

    # Plot nodes
    if pos:
        node_x = [pos[node][0] for node in pos]
        node_y = [pos[node][1] for node in pos]
        ax.scatter(node_x, node_y, s=node_size, c="blue", alpha=0.3, zorder=5)

    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)
    ax.set_title(title)
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")

    plt.tight_layout()
    return fig, ax


import networkx as nx
import numpy as np
from shapely.geometry import Point
from scipy.spatial import cKDTree
