# Circular Queue: Array & Linked List Implementations

---

## 💡 Initial Idea and Implementation Plan

### The Goal

To create a queue that **reuses memory efficiently** by allowing the "end" of the queue to loop back to the "start." A standard linear queue wastes memory — once the front pointer advances past deleted elements, those slots can never be reclaimed. A circular queue solves this entirely.

### The Strategy

Two distinct implementations are explored:

1. **Array Implementation** — Use a fixed-size list. We track `front` and `rear` positions. When either pointer reaches the end of the array, **modulo arithmetic** resets it back to index `0`, creating the illusion of a circle.

2. **Linked List Implementation** — Use nodes where each node points to the next. To make it circular, we ensure the `next` pointer of the **rear node always points back to the front node**. This elegant structure lets us manage the entire queue using only a **single `rear` pointer**, since `rear.next` is always the front.

---

## 🧱 Part 1: Circular Queue Using an Array

### 1.1 The Constructor (`__init__`)

```python
def __init__(self, capacity):
    self.capacity = capacity
    self.queue = [None] * capacity
    self.front = -1
    self.rear = -1
    self.count = 0
```

| Attribute | Purpose |
|---|---|
| `self.capacity` | Sets the maximum number of items the queue can hold. |
| `self.queue = [None] * capacity` | Pre-allocates a list of a fixed size, reserving memory upfront. |
| `self.front = -1` | Tracks the index of the first (oldest) element. `-1` means empty. |
| `self.rear = -1` | Tracks the index of the last (newest) element. `-1` means empty. |
| `self.count = 0` | Tracks the current number of elements for easy `is_full` and `is_empty` checks, avoiding complex pointer comparisons. |

> **Why `-1`?** Using `-1` for both pointers is a clean sentinel value that unambiguously signals an empty queue, separating the "empty" state from any valid index (which starts at `0`).

---

### 1.2 Adding Items (`enqueue`)

```python
def enqueue(self, item):
    if self.count == self.capacity:
        print("Queue is full.")
        return

    if self.count == 0:
        self.front = 0       # First item: initialise front pointer

    self.rear = (self.rear + 1) % self.capacity   # Wrap-around
    self.queue[self.rear] = item
    self.count += 1
```

**Step-by-step breakdown:**

| Step | Code | Purpose |
|---|---|---|
| **Full Check** | `if self.count == self.capacity` | Prevents overflow — stops adding when the queue is at capacity. |
| **First Item Logic** | `if self.count == 0: self.front = 0` | Moves `front` off its sentinel value (`-1`) to a valid index on the very first insertion. |
| **Modulo Wrap-around** | `self.rear = (self.rear + 1) % self.capacity` | The core "circular" operation — if `rear` was at the last index (e.g., `9`), adding `1` and taking modulo resets it to `0`. |
| **Assignment** | `self.queue[self.rear] = item` | Places the new item at the updated `rear` index. |

> **The "Magic" Line — Modulo Wrap-around:**
> ```
> Capacity = 5,  rear = 4  (last index)
> (4 + 1) % 5  →  5 % 5  →  0   ✅ Wraps back to the start
> ```
> This single expression is what transforms a linear array into a circular one.

---

### 1.3 Removing Items (`dequeue`)

```python
def dequeue(self):
    if self.count == 0:
        print("Queue is empty.")
        return None

    item = self.queue[self.front]
    self.queue[self.front] = None   # Clean up the slot
    self.count -= 1

    if self.count == 0:
        self.front = -1             # Reset to empty state
        self.rear = -1
    else:
        self.front = (self.front + 1) % self.capacity  # Wrap-around

    return item
```

**Step-by-step breakdown:**

| Step | Code | Purpose |
|---|---|---|
| **Empty Check** | `if self.count == 0` | Cannot remove from an empty queue — guards against underflow. |
| **Retrieve & Clean** | `item = self.queue[self.front]` then `= None` | Retrieves the front item and frees the slot so it can be reused. |
| **Full Empty Reset** | `if self.count == 0: front = rear = -1` | If the last element was just removed, both pointers reset to the clean "empty" sentinel. |
| **Front Wrap-around** | `self.front = (self.front + 1) % self.capacity` | Advances `front` to the next item, wrapping around the end of the array if needed. |

---

### 1.4 Helper Methods

#### `peek()`

```python
def peek(self):
    if self.count == 0:
        return None
    return self.queue[self.front]
```

Simply returns `queue[self.front]` **without removing it** — a read-only view of the next item to be dequeued.

---

#### `display()`

```python
def display(self):
    for i in range(self.count):
        index = (self.front + i) % self.capacity
        print(self.queue[index], end=" ")
```

This is more subtle than it looks. Because items might physically wrap around the end of the array, we can't just iterate from index `0` to `count`. Instead:

- Loop `i` from `0` to `count`.
- Calculate the **physical index** as `(self.front + i) % self.capacity`.

**Example — visualising wrap-around:**
```
Capacity = 5,  front = 3,  count = 4
i=0 → (3+0) % 5 = 3  ✅
i=1 → (3+1) % 5 = 4  ✅
i=2 → (3+2) % 5 = 0  ✅  (wrapped!)
i=3 → (3+3) % 5 = 1  ✅  (wrapped!)
```
This prints items in their correct **logical order** regardless of their physical position in the array.

---

## 🔗 Part 2: Circular Queue Using a Linked List

### 2.1 The `Node` Class

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
```

A simple building block with two attributes:

| Attribute | Description |
|---|---|
| `self.data` | The actual value stored in this node. |
| `self.next` | A pointer to the next node in the sequence (`None` initially). |

---

### 2.2 The `CircularQueueLinkedList` Class

```python
def __init__(self):
    self.rear = None
    self.count = 0
```

> **Key Design Insight:** We only store a reference to the **`rear`** node. We don't need a separate `front` pointer because the structure is always circular — `self.rear.next` **is** the front. This keeps the implementation lean.

```
  ┌──────────────────────────────┐
  ↓                              │
[front] → [node2] → [node3] → [rear]
```

---

### 2.3 Adding Items (`enqueue`)

```python
def enqueue(self, item):
    new_node = Node(item)
    self.count += 1

    if self.rear is None:
        # Empty queue: node points to itself
        new_node.next = new_node
        self.rear = new_node
    else:
        new_node.next = self.rear.next   # New node → old front
        self.rear.next = new_node         # Old rear → new node
        self.rear = new_node              # Advance rear to new node
```

**The three-step linking process for a non-empty queue:**

```
Before:
  [rear] → [front] → ...

Step 1:  new_node.next = self.rear.next
         [rear] → [front]
                    ↑
                [new_node]

Step 2:  self.rear.next = new_node
         [rear] → [new_node] → [front]

Step 3:  self.rear = new_node
         (new_node is now the rear)
         [old_rear] → [new rear] → [front] → ...
```

| Step | Code | Purpose |
|---|---|---|
| **Empty State** | `new_node.next = new_node` | The very first node must point to itself to establish circularity from the start. |
| **Link to Front** | `new_node.next = self.rear.next` | New node takes over as the last item, so it must point to the front (what `rear.next` currently is). |
| **Link from Old Rear** | `self.rear.next = new_node` | Old rear no longer points directly to front — it now points to the new node. |
| **Advance Rear** | `self.rear = new_node` | Officially makes the new node the new `rear`. |

---

### 2.4 Removing Items (`dequeue`)

```python
def dequeue(self):
    if self.rear is None:
        print("Queue is empty.")
        return None

    front_node = self.rear.next
    self.count -= 1

    if self.count == 0:
        self.rear = None           # Only one node — queue becomes empty
    else:
        self.rear.next = front_node.next  # Bypass the old front

    return front_node.data
```

**The bypassing logic:**

```
Before:
  [rear] → [front] → [second] → ...

front_node = self.rear.next       (grab the front)

self.rear.next = front_node.next  (rear now skips directly to second)

After:
  [rear] → [second] → ...         (front is dropped from the circle)
```

| Case | Handling |
|---|---|
| **Single node** | `self.rear = None` — the queue is now empty; no nodes remain. |
| **Multiple nodes** | `self.rear.next = front_node.next` — the circle is redrawn to skip the removed front node. |

> **Memory Note:** In Python, once `front_node` is no longer referenced, it is automatically garbage collected. No manual memory management is needed.

---

## 📊 Part 3: Comparison and Complexity

### Time Complexity

| Operation | Array Implementation | Linked List Implementation |
|---|---|---|
| `enqueue` | $O(1)$ | $O(1)$ |
| `dequeue` | $O(1)$ | $O(1)$ |
| `peek` | $O(1)$ | $O(1)$ |
| `search` | $O(n)$ | $O(n)$ |
| `display` | $O(n)$ | $O(n)$ |

Both implementations achieve constant time for the core queue operations.

---

### Space & Design Comparison

| Feature | Array Implementation | Linked List Implementation |
|---|---|---|
| **Memory Allocation** | Fixed — pre-allocated at construction. | Dynamic — grows and shrinks with usage. |
| **Capacity** | Hard limit (`capacity`). Cannot exceed it. | Theoretically unlimited (bounded only by available memory). |
| **Memory Efficiency** | May waste slots if queue is small relative to capacity. | Allocates exactly as much as needed — no wasted slots. |
| **Overhead** | No pointer overhead; data sits in contiguous memory. | Each node carries an extra `next` pointer (~8 bytes in CPython). |
| **Cache Performance** | Better — array elements are contiguous in memory. | Worse — nodes may be scattered across the heap. |
| **Pointer Tracking** | Requires both `front` and `rear` indices. | Requires only `rear` (since `rear.next` is always the front). |
| **Best Used When** | Capacity is known in advance and memory is constrained. | Queue size is unpredictable or must be flexible at runtime. |
