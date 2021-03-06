class Node:

    def __init__(self, name, neighbors = set()):
        self.name = name
        self.discovered = False
        self.distance = None
        self.neighbors = neighbors
        self.parent = None

    def is_discovered(self):
        return self.discovered

    def discover(self):
        self.discovered = True
        return self

    def set_distance(self, distance):
        self.distance = distance
        return self

    def get_parent(self):
        return self.parent

    def get_neighbors(self):
        return self.neighbors

    def set_parent(self, parent):
        self.parent = parent

    def has(self, neighbor):
        if neighbor in self.neighbors():
            return True
        return False

