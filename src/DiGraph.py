from GraphInterface import GraphInterface
from GraphNode import GraphNode


class DiGraph(GraphInterface):

    def __init__(self):
        self.node_map = {}
        self.src_dst = {} # out
        self.dst_src = {} # in
        self.mc = 0
        self.edges_size = 0

    def __repr__(self):
        graph_str = "Graph: |V|="+str(self.v_size())+", |E|="+str(self.e_size())+"\n"
        for i in self.node_map.keys():
            if self.all_out_edges_of_node(i) is None:
                if self.all_in_edges_of_node(i) is None:
                    graph_str += str(i) + ": |edges out|=" + str(0) + \
                        "  |edges in|=" + str(0) + ", "
                else:
                    graph_str += str(i) + ": |edges out|=" + str(0) + "  |edges in|=" + \
                        str(len(self.all_in_edges_of_node(i))) + ", "
            else:
                if self.all_in_edges_of_node(i) is None:
                    graph_str += str(i) + ": |edges out|=" + str(
                        len(self.all_out_edges_of_node(i))) + "  |edges in|=" + str(0) + ", "
                else:
                    graph_str += str(i) + ": |edges out|=" + str(len(self.all_out_edges_of_node(i))
                                                           ) + "  |edges in|=" + str(len(self.all_in_edges_of_node(i))) + ", "
        return graph_str

    def v_size(self) -> int:
        return len(self.node_map)

    def e_size(self) -> int:
        size = 0
        for i in self.node_map:
            if i in self.dst_src.keys():
                size += len(self.dst_src[i])
        return size

    def get_mc(self) -> int:
        return self.mc

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
         (node_id, node_data)
        """
        return self.node_map

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes does not exists the functions will do nothing
        """
        if id1 is id2:        # check if the IDs are the same
            return False
        if weight < 0:      # check if weight is valid
            return False
        # check if the nodes exist
        if self.node_map.get(id1) is None or self.node_map.get(id2) is None:
            return False

        if id1 in self.src_dst.keys():      # check if the edge already exists
            if id2 in self.src_dst.get(id1):
                return False

        if id1 in self.src_dst.keys():                  # check if id1 is already in the edgesOutOf dict
            # if it does, update the new edge
            self.src_dst[id1].update({id2: weight})
        else:
            # if it does not exists, initialize it with the new edge
            self.src_dst[id1] = {id2: weight}

        if id2 in self.dst_src.keys():                   # check if id2 is already in the edgesInto dict
            # if it does, update the new edge
            self.dst_src[id2].update({id1: weight})
        else:
            # if it does not exists, initialize it with the new edge
            self.dst_src[id2] = {id1: weight}

        self.mc += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """
        if self.node_map.get(node_id):    # check if the ID is already taken
            return False
        n = GraphNode(node_id, pos)      # create new node

        self.mc += 1
        self.node_map[node_id] = n
        return True

    def remove_node(self, node_id: int) -> bool:
        if self.node_map.get(node_id) is None:
            return False
        del self.node_map[node_id]

        for i in self.dst_src[node_id].keys():
            if self.src_dst[i] is not None:
                del self.src_dst[i][node_id]
                self.edges_size = self.edges_size - 1
                if not bool(self.src_dst[i]):
                    del self.src_dst[i]

        if self.src_dst.get(node_id) is not None:
            self.edges_size = self.edges_size - len(self.src_dst[node_id])
            del self.src_dst[node_id]
        self.mc = self.mc + 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        ans = False
        if self.src_dst.get(node_id1) is not None:
            if self.src_dst.get(node_id1).get(node_id2) is not None:
                del self.src_dst[node_id1][node_id2]
                self.edges_size = self.edges_size - 1
                self.mc = self.mc + 1
                ans = True
        if self.dst_src.get(node_id2) is not None:
            if self.dst_src.get(node_id2).get(node_id1) is not None:
                del self.dst_src[node_id2][node_id1]
        return ans

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """
        return self.dst_src.get(id1)

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        return self.src_dst.get(id1)

    def printnode_map(self):
        for i in self.node_map.keys():
            print("id = ", i, " pos = ", self.node_map.get(i))

    def print_edges(self):
        for i in self.src_dst.keys():
            for j in self.src_dst[i].keys():
                print("src = ", i, " dest = ", j,
                      " weight = ", self.src_dst.get(i).get(j))
