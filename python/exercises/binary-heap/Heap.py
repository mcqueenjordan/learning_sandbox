import Node, math, sys, queue

class Heap:

    def __init__(self, **kwargs):

        data = kwargs.pop('data', ())
        self.type = kwargs.pop('type', 'max')
        self.tree = []
        self.queue = queue.Queue()
        if data:
            self.size = len(data)
            self.height = math.floor(math.log(self.size, 2))
            self.initialize_tree(data)
            self.build()


    def initialize_tree(self, data):
        for i in range(0, self.size):
            self.tree.append(Node.Node(value = data[i], heap = self, index = i))


    def build(self):
        for node in reversed(self.tree):
            if node.has_children():
                for child in node.children():
                    if not self.verify(child):
                        self.correct(child)


    def insert(self, value):
        keywords = {
            'index': self.size,
            'value': value,
            'heap': self,
            }
        node = Node.Node(**keywords)
        self.tree.append(node)
        self.refresh()
        self.correct(node)
        return self

    def refresh(self):
        self.size = len(self.tree)
        self.height = math.floor(math.log(self.size, 2))

    def get_node(self, index):
        if index > self.size - 1:
            return False
        return self.tree[index]


    def verify(self, node):
        if node.parent().get_value() >= node.get_value():
            return True
        return False


    def correct(self, node):
        while node.parent().get_value() < node.get_value():
            self.queue.put(node.parent())
            self.swap(node.parent(), node)
            if node.is_root():
                self.check(node)
                break
        self.resolve_queue()


    def resolve_queue(self):
        while not self.queue.empty():
            node = self.queue.get()
            self.check(node)
            self.correct(node)

    def swap(self, a, b):
        i, j = a.get_index(), b.get_index()
        self.tree[i], self.tree[j] = self.tree[j], self.tree[i]
        a.set_index(j)
        b.set_index(i)


    def delete(self, node):
        index = node.get_index()
        self.swap(node, self.tree[self.size - 1])
        self.tree.pop()
        self.refresh()
        self.check(self.tree[index])
        self.correct(self.tree[index])

    def check(self, node):
        for child in node.children():
            if child.get_value() > node.get_value():
                self.swap(node, node.get_largest_child())
                self.queue.put(node)
                self.queue.put(child)

    def draw(self):
        space_counter = 2**(self.height + 2) - 1
        string = ""
        node_i = 0
        for height in range(0, self.height + 1):
            space_between = space_counter * " "
            space_counter //= 2
            string += " " * space_counter
            for i in range(0, 2**height):
                if not self.get_node(node_i):
                    break
                string += str(self.get_node(node_i).get_value())
                string += space_between
                node_i += 1
            string += "\n"
        print(string)
