# Iterative Sorting: Merge Sort & Quick Sort

## 💡 Initial Idea and Implementation Plan

### The Goal
To sort an array **without using recursion**. This is often done to avoid `RecursionError` on extremely large datasets where the recursion depth might exceed the system limit.

### The Strategy

- **The Container:** Create a `Stack` class to mimic the "Last-In, First-Out" (LIFO) behavior of a function call.

- **Merge Sort Plan:**
  - *Split Phase:* Instead of calling itself, the function pushes index ranges `(low, high)` onto a stack. It records every split made in a list called `splits`.
  - *Merge Phase:* Since we need to merge from the bottom up (starting with the smallest pieces), we iterate through that `splits` list in reverse order and call a standard merge helper.

- **Quick Sort Plan:**
  - Push the initial range of the array onto the stack.
  - While the stack isn't empty, pop a range, partition it (find the pivot), and then push the two resulting sub-ranges back onto the stack to be handled later.

---

## 🧱 Part 1: The Stack Class

A standard wrapper around a Python list to ensure we only use "Stack" operations.

| Method | Code | Description |
|---|---|---|
| Constructor | `def __init__(self): self.items = []` | Initializes an empty list to store data. |
| Push | `def push(self, value): self.items.append(value)` | Adds an item to the top (end of the list). |
| Pop | `def pop(self): return self.items.pop()` | Removes and returns the top item. |
| Peek | `def peek(self): return self.items[-1]` | Looks at the top item without removing it. |
| Is Empty | `def is_empty(self): return len(self.items) == 0` | Returns `True` if the stack has no items. |

---

## 🧩 Part 2: Iterative Merge Sort

### `merge_sort(arr)`

- `arr = arr[:]` — Creates a shallow copy so we don't mutate the original input.
- `if len(arr) < 2: return arr` — Base case: a list with 0 or 1 items is already sorted.
- `stack = Stack()` — Creates our manual stack.
- `stack.push((0, len(arr) - 1))` — Pushes the boundaries of the entire array.
- `splits = []` — A history log of every division made, so we know how to reassemble later.

#### The "Splitting" Loop

```python
while not stack.is_empty():
    low, high = stack.pop()
    if low < high:
        mid = (low + high) // 2
        splits.append((low, mid, high))  # Record the split
        stack.push((mid + 1, high))      # Push right half
        stack.push((low, mid))           # Push left half
```

- Keeps going until there are no more ranges to divide.
- `mid = (low + high) // 2` — Finds the midpoint.
- **Crucial Step:** Records the split as `(low, mid, high)` so we can merge these exact indices later.

#### The "Merging" Loop

```python
for low, mid, high in reversed(splits):
    merge(arr, low, mid, high)
```

Iterates through the history log **backwards** — the last split made was the smallest, so we must merge small pieces before large ones.

### `merge(arr, low, mid, high)`

Standard "Combine" logic for Merge Sort.

```python
left = arr[low:mid + 1]
right = arr[mid + 1:high + 1]
```

- Creates temporary copies of the two halves to merge.
- Uses pointers `i`, `j`, `k` for the left half, right half, and original array respectively.
- **Comparison Loop:** Compares `left[i]` and `right[j]`, placing the smaller one back into `arr[k]`.
- **Cleanup Loops:** If one half finishes first, the remaining elements are copied over.

---

## ⚡ Part 3: Iterative Quick Sort

### `quick_sort(arr)`

```python
stack.push((0, len(arr) - 1))  # Start with the full range

while not stack.is_empty():
    low, high = stack.pop()
    pivot = partition(arr, low, high)
    stack.push((low, pivot - 1))   # Push left sub-range
    stack.push((pivot + 1, high))  # Push right sub-range
```

- `partition(arr, low, high)` moves elements so everything smaller than the pivot is on the left, and everything larger is on the right, then returns the pivot's final index.

### `partition(arr, low, high)` — Lomuto Partition Scheme

```python
pivot = arr[high]   # Choose the last element as the pivot
i = low - 1         # Tracks the boundary of the "small elements" zone

for j in range(low, high):
    if arr[j] <= pivot:
        i += 1
        arr[i], arr[j] = arr[j], arr[i]  # Swap into the small zone

arr[i + 1], arr[high] = arr[high], arr[i + 1]  # Place pivot in correct spot
return i + 1
```

- `pivot = arr[high]` — The last element serves as the benchmark.
- `i = low - 1` — Tracks the boundary of the "small elements" zone.
- For each element smaller than the pivot, expand the zone and swap the element into it.
- Finally, move the pivot into its correct position (right after the small elements).

---

## 🏎️ Summary of Complexity

Both algorithms maintain their average-case time complexities:

| Algorithm | Average Time Complexity | Space Complexity |
|---|---|---|
| Merge Sort | $O(n \log n)$ | $O(n)$ |
| Quick Sort | $O(n \log n)$ | $O(\log n)$ (Stack space) |
