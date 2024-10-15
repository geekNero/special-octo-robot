class Tree:

    def __init__(self, value):
        self.set_value(value=value)
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        return child

    def set_value(self, value):
        self.value = value
