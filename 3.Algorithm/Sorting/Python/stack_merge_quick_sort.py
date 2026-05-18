class Stack:
    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0


def merge_sort(arr):

    arr = arr[:]

    if len(arr) < 2:
        return arr

    stack = Stack()

    stack.push((0, len(arr) - 1))

    splits = []

    while not stack.is_empty():

        low, high = stack.pop()

        if low < high:

            mid = (low + high) // 2

            splits.append((low, mid, high))

            stack.push((mid + 1, high))
            stack.push((low, mid))

    for low, mid, high in reversed(splits):
        merge(arr, low, mid, high)

    return arr


def merge(arr, low, mid, high):

    left = arr[low:mid + 1]
    right = arr[mid + 1:high + 1]

    i = 0
    j = 0
    k = low

    while i < len(left) and j < len(right):

        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1

        else:
            arr[k] = right[j]
            j += 1

        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1


def quick_sort(arr):

    arr = arr[:]

    if len(arr) < 2:
        return arr

    stack = Stack()

    stack.push((0, len(arr) - 1))

    while not stack.is_empty():

        low, high = stack.pop()

        if low < high:

            pivot = partition(arr, low, high)

            stack.push((low, pivot - 1))
            stack.push((pivot + 1, high))

    return arr


def partition(arr, low, high):

    pivot = arr[high]

    i = low - 1

    for j in range(low, high):

        if arr[j] <= pivot:

            i += 1

            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    return i + 1


if __name__ == "__main__":

    data = [
        [38, 27, 43, 3, 9, 82, 10],
        [5, 4, 3, 2, 1],
        [1],
        [],
        [3, 3, 1, 2, 1]
    ]

    print("Merge Sort Using Stack\n")

    for item in data:
        print("Input :", item)
        print("Output:", merge_sort(item))
        print()

    print("Quick Sort Using Stack\n")

    for item in data:
        print("Input :", item)
        print("Output:", quick_sort(item))
        print()