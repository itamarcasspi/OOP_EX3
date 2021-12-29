import copy
import json
import re
from typing import List

from DiGraph import DiGraph
from GraphAlgoInterface import GraphAlgoInterface
from PriorityQueue import PriorityQueue, NodeVal
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.backends.backend_agg as agg
import pygame
from pygame.locals import *
import easygui
from GraphInterface import GraphInterface

INF = 20000000

class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g: DiGraph = None):
        """
        Init the graph, prepares the variables for the GUI and gives it a name
        :param g:
        """
        if g is None:
            self.graph = DiGraph()
        else:
            self.graph = g

        self.name = ""
        self.centerToggle = False
        self.currList = []
        if self.graph.e_size() > 200:
            self.edgeToggle = False
        else:
            self.edgeToggle = True

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        file = open("../"+file_name)
        graph_data = json.load(file)
        self.graph = DiGraph()
        for i in graph_data["Nodes"]:
            pos_tuple = None
            if "pos" in i:
                pos_tuple = tuple(map(float, i["pos"].split(',')))
            if not self.graph.add_node(i["id"], pos_tuple):
                file.close()

                return False
        for i in graph_data["Edges"]:
            if not self.graph.add_edge(int(i["src"]), int(i["dest"]), float(i["w"])):
                file.close()
                return False
        file.close()

        return True

    def save_to_json(self, file_name: str) -> bool:
        """
        saves the graph into a new json file.
        The function WILL override any existing graph if the name is taken.
        :param file_name:
        :return:
        """
        try:
            nodes = []
            edges = []
            for currNode in self.graph.node_map.values():
                nodes.append({"pos": str(currNode.pos), "id": currNode.id})

            for destNode in self.graph.dst_src.items():
                for srcNode in destNode[1].items():
                    edges.append(
                        {"src": srcNode[0], "w": srcNode[1], "dest": destNode[0]})

            graphdict = {}
            graphdict["Edges"] = edges
            graphdict["Nodes"] = nodes

            with open("../"+file_name, "w") as file:
                json.dump(graphdict, fp=file)
            return True
        except:
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if self.graph.node_map.get(id1) is None or self.graph.node_map.get(id1) is None:
            return None
        dist = [0 for i in range(self.graph.v_size())]
        prev = [0 for i in range(self.graph.v_size())]

        q = PriorityQueue()
        for i in self.graph.node_map.keys():
            dist[i] = float('inf')

        dist[id1] = 0
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

        if dist[id2] == float('inf'):
            return dist[id2], []

        prevlist = [id2]
        i = id2
        while i != id1:
            prevlist.append(prev[i])
            i = prev[i]

        prevlist.reverse()
        return dist[id2], prevlist

    def centerPoint(self) -> (int, float):
        # floyd warshall algo- first we get a neighboring matrice
        dist = [[float('inf')] * self.graph.v_size() for i in range(self.graph.v_size())]
        for i in range(self.graph.v_size()):
            dist[i][i] = 0

        for i in self.graph.src_dst.keys():
            for j in self.graph.src_dst.get(i).keys():
                dist[i][j] = self.graph.src_dst.get(i).get(j)
        for k in range(self.graph.v_size()):
            for j in range(self.graph.v_size()):
                for i in range(self.graph.v_size()):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        min_longest_path = float('inf')
        center_id = 0
        for i in range(self.graph.v_size()):
            current_max_path = 0
            for j in range(self.graph.v_size()):
                if dist[i][j] > current_max_path:
                    current_max_path = dist[i][j]
            if current_max_path < min_longest_path:
                min_longest_path = current_max_path
                center_id = i

        return center_id, min_longest_path

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        ans = []
        original = copy.deepcopy(node_lst)
        temp = []
        closest_node = 0
        shortest_path = float('inf')

        for z in range(len(node_lst)):
            current_path_cost = 0
            i = z
            t = 0
            while t < len(node_lst):
                shortest_dist = float('inf')
                if node_lst[i] != None:
                    for j in range(len(node_lst)):
                        if node_lst[j] == None or i == j:
                            continue
                        curr_dist = self.shortest_path(node_lst[i],node_lst[j])[0]
                        if curr_dist < shortest_dist:
                            closest_node = j
                            shortest_dist = curr_dist

                    if node_lst[i] != node_lst[closest_node]:
                        to_closest_node = self.shortest_path(node_lst[i], node_lst[closest_node])[1]
                        current_path_cost = current_path_cost + self.shortest_path(node_lst[i],node_lst[closest_node])[0]
                        node_lst[i] = None
                        ans.extend(to_closest_node)
                i = closest_node
                t = t + 1
            node_lst = copy.deepcopy(original)
            if current_path_cost < shortest_path:
                shortest_path = current_path_cost
                temp = copy.deepcopy(ans)
            ans = []
        for i in range(len(temp)-2):
            if temp[i] == temp[i+1]:
                temp.pop(i)

        return temp,shortest_path


    def plot_graph(self) -> None:
        """
        This is the function that manage the GUI.
        First the user will be asked if he wants to use the advanced GUI (with buttons) or just
        draw the graph using just matplotlib.
        """
        # GUI = easygui.boolbox(
        #     "Do you want simple or advanced GUI?\n *advanced GUI is WIP and likely to crash when given wrong inputs\nbut do play with it :)", choices=("Advanced", "Simple"))
        fig, axes = plt.subplots(figsize=(7, 5))
        axes.set_title("Graph " + self.name + "",
                        {'fontname': 'Courier New'}, fontsize=20)
    
        for node in self.graph.node_map.values():
            plt.scatter(node.pos[0], node.pos[1], s=20, color="red")
            plt.text(node.pos[0] + 0.00002, node.pos[1] +
                        0.00006, str(node.id), color="red", fontsize=10)
    
        ecount = 0
        for dest in self.graph.node_map.values():
            currDict = self.graph.all_out_edges_of_node(dest.id)
            destx = dest.pos[0]
            desty = dest.pos[1]
            if currDict is not None:
                for currEdge in currDict:
                    srcx = self.graph.node_map.get(currEdge).pos[0]
                    srcy = self.graph.node_map.get(currEdge).pos[1]
                    plt.annotate("", xy=(srcx, srcy), xytext=(
                        destx, desty), arrowprops=dict(arrowstyle="->"))
                    ecount += 1
    
        if ecount != self.graph.e_size():
            print("error has been occurred")
        else:
            plt.show()
