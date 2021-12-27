from src.GraphInterface import GraphInterface



class DiGraph(GraphInterface):

    def __init__(self):
        self.node_map = dict()
        self.src_dst = dict()
        self.dst_src = dict()
        self.mc = 0
        self.edges_size = 0



    def v_size(self) -> int:
        return len(self.node_map)

    def e_size(self) -> int:
        return self.edges_size

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if self.node_map.get(id1) is None or self.node_map.get(id2) is None:
            return False
        if self.src_dst.get(id1) is None:
            self.src_dst[id1] = dict()
        self.src_dst[id1][id2] = weight
        self.mc = self.mc + 1
        self.edges_size = self.edges_size + 1

        if self.dst_src.get(id2) is None:
            self.dst_src[id2] = dict()
        self.dst_src[id2][id1] = weight

        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if self.node_map.get(node_id) is not None:
            return False
        # node = NodeData(node_id, pos)
        self.node_map[node_id] = pos
        self.mc = self.mc +1
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
                self.edges_size = self.edges_size -1
                self.mc = self.mc + 1
                ans = True
        if self.dst_src.get(node_id2) is not None:
            if self.dst_src.get(node_id2).get(node_id1) is not None:
                del self.dst_src[node_id2][node_id1]
        return ans

    def print_nodes(self):
        for i in self.node_map.keys():
            print("id = ", i, " pos = ", self.node_map.get(i))

    def print_edges(self):
        for i in self.src_dst.keys():
            for j in self.src_dst[i].keys():
                print("src = ", i, " dest = ", j, " weight = ", self.src_dst.get(i).get(j))
