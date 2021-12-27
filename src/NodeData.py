from src.GeoLocation import GeoLocation


class NodeData:

    def __init__(self, i, pos: tuple = None):
        self._id = i
        self.location = pos
        # self.location[0] = pos[0]
        # self.location[1] = pos[1]
        # self.location[2] = pos[2]

    def get_location(self):
        return self.location

    def set_location(self, pos: tuple = None):
        self.location[0] = pos[0]
        self.location[1] = pos[1]
        self.location[2] = pos[2]

    def get_key(self):
        return self._id

    def printNode(self):
        print("id = ,", self._id," location = ",self.location.__str__())
