import bisect


class BPlusNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []  # Used only if it's an internal node
        self.values = []  # Used only if it's a leaf node
        self.next = None  # Pointer to the next leaf for fast range scans


class BPlusTree:
    def __init__(self, order=4):
        self.root = BPlusNode(is_leaf=True)
        self.order = order

    def insert(self, key, value):
        # Insert returns the split key and new node if a split happened
        split_key, new_child = self._insert_recursive(self.root, key, value)

        # If the root itself split, create a new root above it
        if new_child is not None:
            new_root = BPlusNode(is_leaf=False)
            new_root.keys = [split_key]
            new_root.children = [self.root, new_child]
            self.root = new_root

    def _insert_recursive(self, node, key, value):
        if node.is_leaf:
            # Find exact insertion index to keep keys sorted
            idx = bisect.bisect_left(node.keys, key)

            # If key already exists, just update the value
            if idx < len(node.keys) and node.keys[idx] == key:
                node.values[idx] = value
                return None, None

            # Insert the new key and value
            node.keys.insert(idx, key)
            node.values.insert(idx, value)

            # If node is full, split it
            if len(node.keys) >= self.order:
                return self._split_leaf(node)
            return None, None

        else:  # INTERNAL NODE
            # Find which child to traverse down into
            idx = bisect.bisect_right(node.keys, key)
            split_key, new_child = self._insert_recursive(node.children[idx], key, value)

            # If the child split, insert its new separator into this node
            if new_child is not None:
                node.keys.insert(idx, split_key)
                node.children.insert(idx + 1, new_child)

                if len(node.keys) >= self.order:
                    return self._split_internal(node)
            return None, None

    def _split_leaf(self, leaf):
        new_leaf = BPlusNode(is_leaf=True)
        mid = (len(leaf.keys) + 1) // 2

        # Python list slicing makes splitting trivial
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.values = leaf.values[mid:]

        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]

        # Link the leaves together for fast sequential reads
        new_leaf.next = leaf.next
        leaf.next = new_leaf

        # The separator to pass up is the first key of the new right leaf
        return new_leaf.keys[0], new_leaf

    def _split_internal(self, node):
        new_node = BPlusNode(is_leaf=False)
        mid = len(node.keys) // 2

        # The middle key is pushed UP to the parent, it doesn't stay here
        split_key = node.keys[mid]

        new_node.keys = node.keys[mid + 1:]
        new_node.children = node.children[mid + 1:]

        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]

        return split_key, new_node

    def find(self, key):
        node = self.root

        # Walk down internal nodes
        while not node.is_leaf:
            idx = bisect.bisect_right(node.keys, key)
            node = node.children[idx]

        # Binary search inside the leaf
        idx = bisect.bisect_left(node.keys, key)
        if idx < len(node.keys) and node.keys[idx] == key:
            return node.values[idx]
        return None

    def range_scan(self):
        # Step 1: Drop straight down the left side to find the smallest leaf
        node = self.root
        while not node.is_leaf:
            node = node.children[0]

        # Step 2: Traverse horizontally using the `next` pointers
        while node is not None:
            for k, v in zip(node.keys, node.values):
                yield k, v
            node = node.next

    def print_tree(self):
        self._print_node(self.root, 0)

    def _print_node(self, node, depth):
        indent = "  " * depth
        if node.is_leaf:
            data_str = " ".join([f"{k}({v})" for k, v in zip(node.keys, node.values)])
            print(f"{indent}[LEAF] Data: {data_str}")
        else:
            keys_str = " ".join(map(str, node.keys))
            print(f"{indent}[INTERNAL] Keys: {keys_str}")
            for child in node.children:
                self._print_node(child, depth + 1)


# =====================================================================
# Demonstration Driver
# =====================================================================
if __name__ == "__main__":
    tree = BPlusTree(order=4)

    # Insert some sample data
    data = [
        (30, "C"), (20, "B"), (10, "A"), (40, "D"),
        (50, "E"), (25, "C+"), (15, "A+"), (35, "D+")
    ]

    for key, val in data:
        tree.insert(key, val)

    print("=== Tree structure ===")
    tree.print_tree()

    print("\n=== Exact Match Search ===")
    key_to_find = 25
    val = tree.find(key_to_find)
    if val:
        print(f"Found key {key_to_find}: {val}")
    else:
        print(f"Key {key_to_find} not found.")

    print("\n=== Range scan (All keys in order) ===")
    for key, val in tree.range_scan():
        print(f"  ({key}, {val})")