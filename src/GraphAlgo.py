import json
import re
from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
from src.PriorityQueue import PriorityQueue, NodeVal


class GraphAlgo(GraphAlgoInterface):

    def __init__(self):
        self.graph = DiGraph()

    def load_from_json(self, file_name: str) -> bool:
        file = open("../data/"+file_name)
        graph_data = json.load(file)

        for i in graph_data["Nodes"]:
            pos_tuple = tuple(map(float, i["pos"].split(',')))
            if not self.graph.add_node(i["id"], pos_tuple):
                return False
        for i in graph_data["Edges"]:
            if not self.graph.add_edge(int(i["src"]), int(i["dest"]), float(i["w"])):
                return False
        file.close()

        return True

    def save_to_json(self, file_name: str) -> bool:

        file = open("../data/" + file_name, "w")
        file.write("{\n")
        file.write("  \"Edges\": [\n")
        first = True
        for i in self.graph.src_dst.keys():
            for j in self.graph.src_dst[i].keys():
                if first:
                    file.write("    {\n")
                    file.write("      \"src\": "+str(i)+",\n")
                    file.write("      \"w\": " +str(self.graph.src_dst[i][j])+",\n")
                    file.write("      \"dest\": " + str(j) + "\n")
                    first = False
                else:
                    file.write("    },\n")
                    file.write("    {\n")
                    file.write("      \"src\": " + str(i) + ",\n")
                    file.write("      \"w\": " + str(self.graph.src_dst[i][j]) + ",\n")
                    file.write("      \"dest\": " + str(j) + "\n")

        file.write("    }\n")
        file.write("  ],\n")
        file.write("  \"Nodes\": [\n")
        first = True
        for i in self.graph.node_map.keys():
            if first:
                file.write("    {\n")
                file.write("      \"pos\": \"" + str(self.graph.node_map.get(i)[0]) + ","+str(self.graph.node_map.get(i)[1])+","+str(self.graph.node_map.get(i)[2])+"\",\n")
                file.write("      \"id\": " + str(i) + "\n")
                first = False
            else:
                file.write("    },\n")
                file.write("    {\n")
                file.write("      \"pos\": \"" + str(self.graph.node_map.get(i)[0]) + "," + str(
                    self.graph.node_map.get(i)[1]) + "," + str(self.graph.node_map.get(i)[2]) + "\",\n")
                file.write("      \"id\": " + str(i) + "\n")
        file.write("    }\n")
        file.write("  ]\n")
        file.write("}")
        file.close()
        return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if self.graph.node_map.get(id1) is None or self.graph.node_map.get(id1) is None:
            return None
        dist = [0 for i in range(self.graph.v_size())]
        prev = arr = [0 for i in range(self.graph.v_size())]

        q = PriorityQueue()
        for i in self.graph.node_map.keys():
            dist.insert(i,float('inf'))
        dist.insert(id1,0)
        src = NodeVal(id1)
        src.val = 0
        q.insert(src)

        while not q.isEmpty():
            u = q.delete()
            if u.val <= dist[u.id]:
                dist[u.id] = u.val
                if self.graph.src_dst.get(u.id) is None:
                    continue
                for i in self.graph.src_dst.get(u.id).keys():
                    alt = dist[u.id] + self.graph.src_dst[u.id][i]
                    if alt < dist[i]:
                        v = NodeVal(i)
                        v.val = alt
                        q.insert(v)
                        dist[v.id] = alt
                        prev[v.id] = u.id

        prevlist = [id2]
        i = id2
        while i != id1:
            prevlist.append(prev[i])
            i = prev[i]

        prevlist.reverse()
        print(prevlist)

        return dist[id2],prevlist

    def plot_graph(self) -> None:
        pass