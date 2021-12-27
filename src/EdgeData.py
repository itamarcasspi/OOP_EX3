class EdgeData:

    def __init__(self, sr, de, we):  # src,dest,weight,id
        self.src = sr
        self.dest = de
        self.weight = we

    def get_src(self):
        return self.src

    def get_dest(self):
        return self.dest

    def get_weight(self):
        return self.weight

    def is_equal(self, edge):
        if self.src != edge.src or self.dest != edge.dest or self.weight != edge.weight:
            return False
        return True
