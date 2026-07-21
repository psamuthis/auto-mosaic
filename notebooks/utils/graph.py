from typing import Any, Generator
from shapely import LineString
from collections import defaultdict
from typing import Dict, List, Tuple

def count_components(graph: Dict[Tuple[float, float], List[Tuple[float, float]]]) -> int:
    """
    Count the number of connected components in an undirected graph.
    
    Args:
        graph: Dictionary where keys are points and values are lists of neighboring points
    
    Returns:
        Number of connected components
    """
    visited = set()
    components = 0
    
    def dfs(node: Tuple[float, float]):
        """Depth-first search to visit all nodes in a component"""
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                # Add all unvisited neighbors
                for neighbor in graph.get(current, []):
                    if neighbor not in visited:
                        stack.append(neighbor)
    
    # Iterate through all nodes in the graph
    for node in graph:
        if node not in visited:
            components += 1
            dfs(node)
    
    return components