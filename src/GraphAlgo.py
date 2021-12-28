import json
import re
from DiGraph import DiGraph
from GraphAlgoInterface import GraphAlgoInterface
from PriorityQueue import PriorityQueue, NodeVal

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.backends.backend_agg as agg
import pygame
from pygame.locals import *
import easygui


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g=None):
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

    def load_from_json(self, file_name: str) -> bool:
        file = open(file_name)
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

        file = open("data/" + file_name, "w")
        file.write("{\n")
        file.write("  \"Edges\": [\n")
        first = True
        for i in self.graph.src_dst.keys():
            for j in self.graph.src_dst[i].keys():
                if first:
                    file.write("    {\n")
                    file.write("      \"src\": "+str(i)+",\n")
                    file.write("      \"w\": " +
                               str(self.graph.src_dst[i][j])+",\n")
                    file.write("      \"dest\": " + str(j) + "\n")
                    first = False
                else:
                    file.write("    },\n")
                    file.write("    {\n")
                    file.write("      \"src\": " + str(i) + ",\n")
                    file.write("      \"w\": " +
                               str(self.graph.src_dst[i][j]) + ",\n")
                    file.write("      \"dest\": " + str(j) + "\n")

        file.write("    }\n")
        file.write("  ],\n")
        file.write("  \"Nodes\": [\n")
        first = True
        for i in self.graph.node_map.keys():
            if first:
                file.write("    {\n")
                file.write("      \"pos\": \"" + str(self.graph.node_map.get(i)[0]) + ","+str(
                    self.graph.node_map.get(i)[1])+","+str(self.graph.node_map.get(i)[2])+"\",\n")
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
            dist.insert(i, float('inf'))
        dist.insert(id1, 0)
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
        return dist[id2], prevlist

    def plot_graph(self) -> None:
        """
        This is the function that manage the GUI.
        First the user will be asked if he wants to use the advanced GUI (with buttons) or just
        draw the graph using just matplotlib.
        """
        # GUI = easygui.boolbox(
        #     "Do you want simple or advanced GUI?\n *advanced GUI is WIP and likely to crash when given wrong inputs\nbut do play with it :)", choices=("Advanced", "Simple"))
        if False:
            self.advancedGUI()
        else:
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

    def advancedGUI(self) -> None:
        """
        This function runs the advanced GUI.
        Creates the buttons and update the matplotlib that is presented in pygame.
        """
        matplotlib.use("Agg")

        fig = self.drawGraph()

        pygame.font.init()
        myfont = pygame.font.SysFont('Courier New', 15)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        pygame.init()

        window = pygame.display.set_mode((800, 500), DOUBLEBUF)
        screen = pygame.display.get_surface()

        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(surf, (0, 0))
        pygame.draw.rect(screen, (100, 150, 200), [700, 0, 100, 25])
        pygame.draw.rect(screen, (100, 200, 150), [700, 25, 100, 25])
        pygame.draw.rect(screen, (150, 100, 200), [700, 50, 100, 25])
        pygame.draw.rect(screen, (100, 150, 200), [700, 75, 100, 25])
        pygame.draw.rect(screen, (100, 200, 150), [700, 100, 100, 25])
        pygame.draw.rect(screen, (150, 100, 200), [700, 125, 100, 25])
        pygame.draw.rect(screen, (100, 150, 200), [700, 350, 100, 25])
        pygame.draw.rect(screen, (100, 200, 150), [700, 375, 100, 25])
        pygame.draw.rect(screen, (150, 100, 200), [700, 400, 100, 25])
        pygame.draw.rect(screen, (100, 150, 200), [700, 425, 100, 25])
        pygame.draw.rect(screen, (100, 200, 150), [700, 450, 100, 25])
        pygame.draw.rect(screen, (150, 100, 200), [700, 475, 100, 25])
        loadgraphtext = myfont.render("load", False, (0, 0, 0))
        savegraphtext = myfont.render("save", False, (0, 0, 0))
        centertext = myfont.render("center", False, (0, 0, 0))
        pathtext = myfont.render("path", False, (0, 0, 0))
        unpathtext = myfont.render("clear path", False, (0, 0, 0))
        tsptext = myfont.render("tsp", False, (0, 0, 0))
        removenodetext = myfont.render("remove node", False, (0, 0, 0))
        addnodetext = myfont.render("add node", False, (0, 0, 0))
        connecttext = myfont.render("connect", False, (0, 0, 0))
        disconnecttext = myfont.render("disconnect", False, (0, 0, 0))
        edgetext = myfont.render("show edges", False, (0, 0, 0))
        screen.blit(loadgraphtext, (705, 2.5))
        screen.blit(savegraphtext, (705, 30.5))
        screen.blit(centertext, (705, 57))
        screen.blit(pathtext, (705, 83))
        screen.blit(unpathtext, (702, 100))
        screen.blit(tsptext, (705, 127))
        screen.blit(removenodetext, (702, 350))
        screen.blit(addnodetext, (705, 375))
        screen.blit(connecttext, (702, 400))
        screen.blit(disconnecttext, (705, 425))
        screen.blit(edgetext, (705, 450))
        pygame.display.flip()
        crashed = False
        updated = False
        while not crashed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if 700 < pos[0] < 800 and 0 < pos[1] < 25:
                        graphname = easygui.enterbox(
                            "Enter the name of the graph you want to load\n NO NEED to enter data/... or ..json")
                        self.load_from_json("data/"+graphname+".json")
                        self.currList = []
                        updated = True
                    if 700 < pos[0] < 800 and 75 > pos[1] > 50:
                        if self.centerToggle:
                            self.centerToggle = False
                        else:
                            self.centerToggle = True
                        updated = True
                    if 700 < pos[0] < 800 and 50 > pos[1] > 25:
                        newname = easygui.enterbox(
                            "Name your graph\n DO NOT add .json\n you WILL override the existing graph")
                        self.save_to_json(newname)
                    if 700 < pos[0] < 800 and 100 > pos[1] > 75:
                        src = int(easygui.enterbox(
                            "Enter your source ID\n enter an empty string for removing current path"))
                        dest = int(easygui.enterbox(
                            "Enter your destination ID\n enter an empty string for removing current path"))
                        self.currList = self.shortest_path(src, dest)[1]
                        updated = True
                    if 700 < pos[0] < 800 and 125 > pos[1] > 100:
                        self.currList = []
                        updated = True
                    if 700 < pos[0] < 800 and 150 > pos[1] > 125:
                        stops = int(easygui.enterbox(
                            "how many STOPS do you want to make?"))
                        self.currList = []
                        tsplist = []
                        for i in range(stops):
                            tsplist.append(int(easygui.enterbox(
                                "enter a stop "+str(i+1)+"/"+str(stops))))
                        self.currList = self.TSP(tsplist)[0]
                        updated = True
                    if 700 < pos[0] < 800 and 375 > pos[1] > 350:
                        self.graph.remove_node(
                            int(easygui.enterbox("Which node to remove?")))
                        updated = True
                    if 700 < pos[0] < 800 and 400 > pos[1] > 375:
                        pos = ""
                        ID = int(easygui.enterbox(
                            "Enter new ID\n Make sure this ID is not taken"))
                        x = easygui.enterbox(
                            "Enter X \n enter -1 for random location")
                        if x != "-1":
                            y = easygui.enterbox("Enter Y")
                            pos = x+","+y+","+"0"
                        else:
                            pos = None
                        self.graph.add_node(ID, pos)
                        updated = True

                    if 700 < pos[0] < 800 and 425 > pos[1] > 400:
                        src = int(easygui.enterbox(
                            "Enter source ID\nMake sure it exists"))
                        dest = int(easygui.enterbox(
                            "Enter destination ID\nMake sure it exists"))
                        weight = float(easygui.enterbox(
                            "Enter weight\n positive (and zero) values only"))
                        self.graph.add_edge(src, dest, weight)
                        updated = True

                    if 700 < pos[0] < 800 and 450 > pos[1] > 425:
                        src = int(easygui.enterbox(
                            "Enter source ID\nMake sure it exists"))
                        dest = int(easygui.enterbox(
                            "Enter destination ID\nMake sure it exists"))
                        self.graph.remove_edge(src, dest)
                        updated = True

                    if 700 < pos[0] < 800 and 475 > pos[1] > 450:
                        if self.edgeToggle:
                            self.edgeToggle = False
                        else:
                            self.edgeToggle = True
                        updated = True

                if updated:
                    plt.close(fig)
                    fig = self.drawGraph()
                    canvas = agg.FigureCanvasAgg(fig)
                    canvas.draw()
                    renderer = canvas.get_renderer()
                    raw_data = renderer.tostring_rgb()
                    surf = pygame.image.fromstring(raw_data, size, "RGB")
                    screen.blit(surf, (0, 0))
                    pygame.display.flip()
                    updated = False
