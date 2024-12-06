import string
import numpy as np
from numpy import ndarray
from typing import List, Union


def generate_node_names(distance_matrix: Union[List, ndarray]) -> List[str]:
    """Generates alphabetical node names based on the size of the distance matrix."""
    num_nodes = len(distance_matrix)
    alphabet = string.ascii_uppercase
    node_names = [alphabet[i] for i in range(num_nodes)]
    return node_names

def generate_node_coordinates(num_nodes: int, node_names: List[str]) -> dict:
    """Generates coordinates for nodes in a circular layout."""
    angle = 2 * np.pi / num_nodes
    return {node_names[i]: (np.cos(i * angle), np.sin(i * angle)) for i in range(num_nodes)}