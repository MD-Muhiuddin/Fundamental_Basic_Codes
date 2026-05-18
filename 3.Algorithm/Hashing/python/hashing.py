class HashTable:

    def __init__(self, size=10):

        self.size = size
        self.table = [None] * size

    def insert(self, key, hash_func):

        index = hash_func(key, self.size)

        start = index

        while self.table[index] is not None:

            if self.table[index] == key:
                print(f"{key} already exists")
                return

            index = (index + 1) % self.size

            if index == start:
                print("Hash table is full")
                return

        self.table[index] = key

        print(f"Inserted {key} at index {index}")

    def search(self, key, hash_func):

        index = hash_func(key, self.size)

        start = index

        while self.table[index] is not None:

            if self.table[index] == key:
                print(f"{key} found at index {index}")
                return index

            index = (index + 1) % self.size

            if index == start:
                break

        print(f"{key} not found")

        return -1

    def delete(self, key, hash_func):

        index = self.search(key, hash_func)

        if index != -1:

            self.table[index] = None

            print(f"{key} deleted")

    def display(self):

        print("\nHash Table")

        for i in range(self.size):

            print(i, ":", self.table[i])


class Node:

    def __init__(self, key):

        self.key = key
        self.next = None


class ChainingHashTable:

    def __init__(self, size=10):

        self.size = size
        self.table = [None] * size

    def insert(self, key, hash_func):

        index = hash_func(key, self.size)

        current = self.table[index]

        while current:

            if current.key == key:
                print(f"{key} already exists")
                return

            current = current.next

        new_node = Node(key)

        new_node.next = self.table[index]

        self.table[index] = new_node

        print(f"Inserted {key} at index {index}")

    def search(self, key, hash_func):

        index = hash_func(key, self.size)

        current = self.table[index]

        while current:

            if current.key == key:
                print(f"{key} found at index {index}")
                return index

            current = current.next

        print(f"{key} not found")

        return -1

    def delete(self, key, hash_func):

        index = hash_func(key, self.size)

        current = self.table[index]

        prev = None

        while current:

            if current.key == key:

                if prev is None:
                    self.table[index] = current.next

                else:
                    prev.next = current.next

                print(f"{key} deleted")

                return

            prev = current

            current = current.next

        print(f"{key} not found")

    def display(self):

        print("\nHash Table")

        for i in range(self.size):

            print(i, ":", end=" ")

            current = self.table[i]

            while current:

                print(current.key, end=" -> ")

                current = current.next

            print("None")


def mid_square_hash(key, table_size):

    square = key * key

    square_str = str(square)

    mid = len(square_str) // 2

    if len(square_str) > 1:

        value = int(square_str[mid])

    else:

        value = int(square_str)

    return value % table_size


def folding_hash(key, table_size):

    key_str = str(key)

    total = 0

    for i in range(0, len(key_str), 2):

        total += int(key_str[i:i + 2])

    return total % table_size




if __name__ == "__main__":

    keys = [43, 1234, 5678, 9, 200, 1111, 987, 56, 333, 72]

    print("Mid-Square Hash with Linear Probing\n")

    ht1 = HashTable(10)

    for key in keys:

        ht1.insert(key, mid_square_hash)

    ht1.display()

    ht1.search(1234, mid_square_hash)

    ht1.delete(43, mid_square_hash)

    ht1.display()



    print("\nMid-Square Hash with Chaining\n")

    ht2 = ChainingHashTable(10)

    for key in keys:

        ht2.insert(key, mid_square_hash)

    ht2.display()

    ht2.search(1234, mid_square_hash)

    ht2.delete(43, mid_square_hash)

    ht2.display()



    print("\nFolding Hash with Linear Probing\n")

    ht3 = HashTable(10)

    for key in keys:

        ht3.insert(key, folding_hash)

    ht3.display()

    ht3.search(5678, folding_hash)

    ht3.delete(200, folding_hash)

    ht3.display()



    print("\nFolding Hash with Chaining\n")

    ht4 = ChainingHashTable(10)

    for key in keys:

        ht4.insert(key, folding_hash)

    ht4.display()

    ht4.search(5678, folding_hash)

    ht4.delete(200, folding_hash)

    ht4.display()
