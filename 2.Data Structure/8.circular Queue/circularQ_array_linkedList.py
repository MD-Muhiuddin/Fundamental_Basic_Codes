class CircularQueueArray:

    def __init__(self, capacity):

        self.capacity = capacity
        self.queue = [None] * capacity

        self.front = -1
        self.rear = -1

        self.count = 0

    def enqueue(self, item):

        if self.is_full():
            print("Queue is full")
            return

        if self.is_empty():
            self.front = 0

        self.rear = (self.rear + 1) % self.capacity

        self.queue[self.rear] = item

        self.count += 1

    def dequeue(self):

        if self.is_empty():
            print("Queue is empty")
            return None

        item = self.queue[self.front]

        self.queue[self.front] = None

        self.count -= 1

        if self.count == 0:

            self.front = -1
            self.rear = -1

        else:

            self.front = (self.front + 1) % self.capacity

        return item

    def peek(self):

        if self.is_empty():
            return None

        return self.queue[self.front]

    def is_empty(self):

        return self.count == 0

    def is_full(self):

        return self.count == self.capacity

    def display(self):

        if self.is_empty():
            print("Queue is empty")
            return

        values = []

        for i in range(self.count):

            index = (self.front + i) % self.capacity

            values.append(str(self.queue[index]))

        print("Queue:", " -> ".join(values))


class Node:

    def __init__(self, data):

        self.data = data
        self.next = None


class CircularQueueLinkedList:

    def __init__(self):

        self.rear = None
        self.count = 0

    def enqueue(self, item):

        new_node = Node(item)

        if self.is_empty():

            new_node.next = new_node

            self.rear = new_node

        else:

            new_node.next = self.rear.next

            self.rear.next = new_node

            self.rear = new_node

        self.count += 1

    def dequeue(self):

        if self.is_empty():

            print("Queue is empty")

            return None

        front_node = self.rear.next

        if self.count == 1:

            self.rear = None

        else:

            self.rear.next = front_node.next

        self.count -= 1

        return front_node.data

    def peek(self):

        if self.is_empty():

            return None

        return self.rear.next.data

    def is_empty(self):

        return self.rear is None

    def display(self):

        if self.is_empty():

            print("Queue is empty")

            return

        values = []

        current = self.rear.next

        for i in range(self.count):

            values.append(str(current.data))

            current = current.next

        print("Queue:", " -> ".join(values))


if __name__ == "__main__":

    print("Circular Queue Using Array\n")

    q1 = CircularQueueArray(4)

    q1.enqueue(10)
    q1.enqueue(20)
    q1.enqueue(30)
    q1.enqueue(40)

    q1.display()

    print("\nRemoved:", q1.dequeue())
    print("Removed:", q1.dequeue())

    q1.display()

    q1.enqueue(50)
    q1.enqueue(60)

    q1.display()

    print("\nFront element:", q1.peek())

    print("\nRemoving all elements")

    while not q1.is_empty():

        print("Removed:", q1.dequeue())

        q1.display()




    print("\nCircular Queue Using Linked List\n")

    q2 = CircularQueueLinkedList()

    q2.enqueue(10)
    q2.enqueue(20)
    q2.enqueue(30)
    q2.enqueue(40)

    q2.display()

    print("\nRemoved:", q2.dequeue())
    print("Removed:", q2.dequeue())

    q2.display()

    q2.enqueue(50)
    q2.enqueue(60)

    q2.display()

    print("\nFront element:", q2.peek())

    print("\nRemoving all elements")

    while not q2.is_empty():

        print("Removed:", q2.dequeue())

        q2.display()