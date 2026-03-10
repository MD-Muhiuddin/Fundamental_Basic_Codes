from .node import Node

class LinkedList:
    def __init__(self, value=None):
        if value is not None:
            new_node = Node(value)
            self.head = new_node
            self.tail = new_node
            self.length = 1
        else:
            self.head = None
            self.tail = None
            self.length = 0

    @classmethod
    def register_operation(cls, func):
        """Attaches the function to the class at runtime."""
        setattr(cls, func.__name__, func)
        return func