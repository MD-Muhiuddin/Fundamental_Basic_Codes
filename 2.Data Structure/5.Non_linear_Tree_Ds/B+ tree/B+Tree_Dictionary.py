import csv
import bisect
import time
import os

class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []  # For internal nodes
        self.values = []    # For leaf nodes (stores lists of meanings)
        self.next = None    # Linked list pointer for leaf nodes connecting them sequentially

class BPlusTree:
    def __init__(self, order=50):
        self.root = BPlusTreeNode(is_leaf=True)
        self.order = order

    def search(self, key):
        key = key.lower()
        curr = self.root

        # Traverse down through internal nodes to find the correct leaf
        while not curr.is_leaf:
            i = bisect.bisect_right(curr.keys, key)
            curr = curr.children[i]

        # Search within the found leaf node
        i = bisect.bisect_left(curr.keys, key)
        if i < len(curr.keys) and curr.keys[i] == key:
            return curr.values[i]
        return None

    def insert(self, key, value):
        key = key.lower()
        root = self.root

        # If the root is full, split it and create a new root
        if len(root.keys) == self.order - 1:
            new_root = BPlusTreeNode(is_leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0, self.root)
            self.root = new_root

        self._insert_non_full(self.root, key, value)

    def _split_child(self, parent, i, child):
        order = self.order
        mid = (order - 1) // 2

        new_node = BPlusTreeNode(is_leaf=child.is_leaf)

        # Logic for splitting a leaf node
        if child.is_leaf:
            parent.keys.insert(i, child.keys[mid])
            parent.children.insert(i + 1, new_node)

            new_node.keys = child.keys[mid:]
            new_node.values = child.values[mid:]
            child.keys = child.keys[:mid]
            child.values = child.values[:mid]

            # Maintain the linked list for sequential access
            new_node.next = child.next
            child.next = new_node

        # Logic for splitting an internal node
        else:
            parent.keys.insert(i, child.keys[mid])
            parent.children.insert(i + 1, new_node)

            new_node.keys = child.keys[mid + 1:]
            new_node.children = child.children[mid + 1:]
            child.keys = child.keys[:mid]
            child.children = child.children[:mid + 1]

    def _insert_non_full(self, node, key, value):
        if node.is_leaf:
            i = bisect.bisect_left(node.keys, key)

            # If the word already exists, append the new meaning to its list
            if i < len(node.keys) and node.keys[i] == key:
                node.values[i].append(value)
            else:
                node.keys.insert(i, key)
                node.values.insert(i, [value])
        else:
            i = bisect.bisect_right(node.keys, key)
            child = node.children[i]

            # Split child if it is full before moving down
            if len(child.keys) == self.order - 1:
                self._split_child(node, i, child)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

class DictionaryApp:
    def __init__(self, order=75):
        # Initializing the B+ Tree. Order 75 is an excellent balance for ~200k items.
        self.tree = BPlusTree(order=order)

    def load_from_csv(self, filepath):
        print(f"Loading dictionary from {filepath}...")
        start_time = time.time()
        count = 0

        try:
            with open(filepath, mode='r', encoding='utf-8') as file:
                # Using standard csv.reader for your header-less format
                reader = csv.reader(file)

                for row_num, row in enumerate(reader, 1):
                    # Ensure the row has both a word and a meaning
                    if len(row) >= 2:
                        word = row[0].strip()
                        # Strip standard whitespace, then strip the triple quotes
                        meaning = row[1].strip().strip('"')

                        if word and meaning:
                            self.tree.insert(word, meaning)
                            count += 1
                    else:
                        if row:
                            print(f"Warning: Skipping malformed data on row {row_num}: {row}")

            elapsed = time.time() - start_time
            print(f"Successfully loaded {count} definitions in {elapsed:.2f} seconds.")

        except FileNotFoundError:
            print(f"Error: The file '{filepath}' was not found. Please check the path.")
        except Exception as e:
            print(f"An error occurred while loading the file: {e}")

    def run_interactive_prompt(self):
        print("\n" + "="*30)
        print("    B+ Tree Dictionary")
        print("="*30)
        print("Commands:")
        print("  - Type a word to search.")
        print("  - Type '!add' to insert a new word.")
        print("  - Type '!exit' to quit.\n")

        while True:
            try:
                user_input = input("Enter command or word: ").strip()
            except KeyboardInterrupt:
                print("\nExiting dictionary. Goodbye!")
                break

            # Handle Exit command
            if user_input.lower() == '!exit':
                print("Exiting dictionary. Goodbye!")
                break

            # Handle Add command
            if user_input.lower() == '!add':
                new_word = input("Enter the new word: ").strip()
                if not new_word:
                    print("Word cannot be empty.\n")
                    continue

                new_meaning = input(f"Enter the meaning for '{new_word}': ").strip()
                if not new_meaning:
                    print("Meaning cannot be empty.\n")
                    continue

                # Utilize the existing insert method
                self.tree.insert(new_word, new_meaning)
                print(f"Successfully added '{new_word}' to the dictionary!\n")
                continue

            # Ignore empty inputs
            if not user_input:
                continue

            # Standard Search Logic
            start_search = time.time()
            meanings = self.tree.search(user_input)
            search_time = (time.time() - start_search) * 1000 # Convert to milliseconds

            if meanings:
                print("\nMeaning(s):")
                for idx, meaning in enumerate(meanings, 1):
                    if len(meanings) > 1:
                        print(f"{idx}. {meaning}")
                    else:
                        print(meaning)
                print(f"\n[Lookup time: {search_time:.3f} ms]\n")
            else:
                print(f"\nWord '{user_input}' not found in the dictionary.\n")


if __name__ == "__main__":
    app = DictionaryApp(order=500)
     # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build full path to CSV
    csv_path = os.path.join(script_dir, "my_dictionary_output.csv")

    app.load_from_csv(csv_path)
    app.run_interactive_prompt()