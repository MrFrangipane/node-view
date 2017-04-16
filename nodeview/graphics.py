

class GraphicNode(object):

    def __init__(self, node):
        self.node = node
        self.width = 150
        self.height = 20

    def update(self):
        self.width = 150
        self.height = 20 + 20 * max(len(self.node.inputs), len(self.node.outputs))
