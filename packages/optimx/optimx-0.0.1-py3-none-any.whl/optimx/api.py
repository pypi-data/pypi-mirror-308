import numpy as np
from numpy import ndarray
from typing import List, Union, Optional, Literal
from .tsp.solver import TspSolver
from .tsp.visual import plot_tsp_route_matplot
from .utils import generate_node_coordinates


def solve_tsp(distance_matrix: Union[List, ndarray],
              algorithm: Literal["brute", "nearest_neighbour", "dynamic_programming", "branch_and_bound"] = "dynamic_programming",
              node_names: Optional[List[str]] = None,
              start_node: Optional[Union[int, str]] = None,
              cycle: bool = False
              ) -> List[Union[int, str]]:
    
    if not isinstance(distance_matrix, (list, ndarray)):
        raise ValueError("distance_matrix must be a list or numpy array")
    
    if isinstance(distance_matrix, list):
        distance_matrix = np.array(distance_matrix)
    
    if distance_matrix.shape[0] != distance_matrix.shape[1]:
        raise ValueError("distance_matrix must be a square matrix")
    
    if not isinstance(algorithm, str):
        raise ValueError("algorithm must be a string")
    
    if node_names is not None:
        if not isinstance(node_names, list):
            raise ValueError("node_names must be a list")
        if len(node_names) != distance_matrix.shape[0]:
            raise ValueError("node_names must have the same length as distance_matrix")
        
    if start_node is not None:
        if isinstance(start_node, int):
            if start_node < 0 or start_node >= distance_matrix.shape[0]:
                raise ValueError("start_node must be a valid index")
        elif isinstance(start_node, str):
            if start_node not in node_names:
                raise ValueError("start_node must be a valid node name")
            else:
                start_node = node_names.index(start_node)
        else:
            raise ValueError("start_node must be an integer or string")
        
    if not isinstance(cycle, bool):
        raise ValueError("cycle must be a boolean")
    
    solver = TspSolver()
    best_route = solver.solve_problem(distance_matrix, algorithm, start_node, cycle)

    if node_names:
        best_route = [node_names[i] for i in best_route]
    
    return best_route


def calculate_tsp_distance_by_route(route: List, 
                                    distance_matrix: Union[List, ndarray],
                                    node_names: Optional[List[str]]=None
                                    ) -> float:
    if node_names:
        indexes = [node_names.index(node) for node in route]
    else:
        indexes = route
    
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[indexes[i]][indexes[i + 1]]
    return total_distance


def plot_tsp_route(route: List[Union[str, int]], 
                   node_names: Optional[List[str]] = None,
                   node_coordinates: Optional[dict] = None,
                   start_node: Optional[Union[int, str]] = None,
                   cycle: bool = True) -> None:
    
    if cycle:
        route = route[:-1]

    if node_names is None:
        node_names = list(range(len(route)))
    else:
        route = [node_names.index(node) for node in route]
        
    if node_coordinates is None:
        node_coordinates = generate_node_coordinates(len(route), node_names)

    if node_names is not None:
        if not isinstance(node_names, list):
            raise ValueError("node_names must be a list")
        if len(node_names) != len(route):
            raise ValueError("node_names must have the same length as route")
    
    if len(route) != len(node_coordinates):
        raise ValueError("route and node_coordinates must have the same length")
    
    if start_node is not None:
        if isinstance(start_node, int):
            if start_node < 0 or start_node >= len(route):
                raise ValueError("start_node must be a valid index")
        elif isinstance(start_node, str):
            if start_node not in node_names:
                raise ValueError("start_node must be a valid node name")
            else:
                start_node = node_names.index(start_node)
        else:
            raise ValueError("start_node must be an integer or string")
        
    if not isinstance(cycle, bool):
        raise ValueError("cycle must be a boolean")
    
    plot_tsp_route_matplot(route, node_names, node_coordinates, start_node, cycle)

    return