import random


class GraphNode:
    def __init__(self, id: int, pos: tuple = None):
        """
        Constructor
        """
        self.tag = 0
        self.id = id
        self.pos = pos


    def __repr__(self):
        return "Node ID:"+str(self.id)