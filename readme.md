
# oop-ex3
 
In this project we have implemented a program that represent a directed and weighted graph.


- NodeData

  Interface that represent a node, that has a unique ID and an optional tuple (x,y,z).

- DirectedWeightedGraph

  Interface that represets the whole graph, that has any number of node and edges.
  Holds the NodeData of the graph inside a dictionary. The edges are stored in a nested dictoinary, where the first key is the Source, the second key is the destination and the value is the weight.
  The second dictionary for the edges, is the same but reversed: the first key is the destintion, second key the source and the value is the weight.
- DirectedWeightedGraphAlgorithms
  Interface that represents the whole graph and allow for several algorithms to be used.


The algorithms that we have implemented in the project are the following:
- Center():
  Returns the NodeData which minimizes the max distance to all the other nodes and its longest available path.
  
- shortestPathDist(NodeData A, NodeData B)
  Returns the minimal total weight of a path between node A and B, and an id list of the nodes in that route.

- tsp(List: cities)
   Returns a list of nodes that represent the shortest path that contains all the nodes in the list "cities".
   A variation of the known The Traveling Salesman algorithm. also returns the total weight of that path.
  


Comparison of the previous assignment and this assignment in terms of time:
(previous assignment vs this assignment)

1k graph:

  load() = 100ms vs 53ms , save() = 74ms vs 33 ms , center() = 16sec, 738ms 

 10k graph:

  load() = 820ms vs  634ms , save() = 648ms vs 289ms

 100k:

  load() = 23sec, 770ms vs 13sec, 574ms ,save() = 17sec, 479ms vs 8.102 




    def get_graph(self) -> GraphInterface:
    @return: the directed graph on which the algorithm works on.
.

    def load_from_json(self, file_name: str) -> bool:
    @returns True if the loading was successful, False o.w.

.

    def save_to_json(self, file_name: str) -> bool:
    @return: True if the save was successful, False o.w.

.

    def shortest_path(self, id1: int, id2: int) -> (float, list): 
    
    implemented with dijkstra algorithm.
    @return: The distance of the path, a list of the nodes ids that the path goes through

.

    def TSP(self, node_lst: List[int]) -> (List[int], float):
    implemented with a "greedy" algorithm. finds the closest node available in the list and go to it.
    try starting from every node in the list and find the shortest path.
    @return: A list of the nodes id's in the path, and the overall distance

.

    def centerPoint(self) -> (int, float):
    implemented with Floyd Warshall algorithm, and when we know all the possible path's costs, compare every column's maximul value and take the lowest one.
    @return: The nodes id, min-maximum distance
  
.

    def plot_graph(self) -> None:
    Create a visual representation of the graph in its current state. (GUI)
    @return None











