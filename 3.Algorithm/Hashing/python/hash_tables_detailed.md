# Hash Tables: Open Addressing & Separate Chaining

---

## 💡 Initial Idea and Implementation Plan

### The Core Objective

The goal is to **map a "key"** (like an ID number) to a specific **"index"** in an array. This allows for nearly instantaneous lookups — avoiding the need to search through every item one by one — achieving an average time complexity of $O(1)$ for core operations.

### The Strategy

The implementation is built around three key concepts:

1. **Hashing Algorithms** — Two distinct functions (`mid_square_hash` and `folding_hash`) transform a large number into a valid index for a fixed-size table.

2. **Collision Resolution** — When two keys hash to the same index, one of two strategies is used:
   - **Linear Probing (`HashTable`):** If a spot is taken, the code "probes" (looks at) the very next available index until it finds an empty space or wraps around.
   - **Separate Chaining (`ChainingHashTable`):** Every index in the table acts as the head of a Linked List. If multiple keys share an index, they are simply linked together at that spot.

3. **CRUD Operations** — Both classes implement the fundamental **Create** (`insert`), **Read** (`search`), and **Delete** operations.

---

## 🧱 Part 1: Open Addressing — The `HashTable` Class

This implementation uses **Linear Probing**, where data is stored *directly* inside the table array. When a collision occurs, the algorithm searches forward for the next available slot.

### `__init__(self, size=10)`

```python
def __init__(self, size=10):
    self.size = size
    self.table = [None] * size
```

- Sets the table to a fixed `size` (default: 10).
- Initializes every slot to `None`, indicating it is empty.

---

### `insert(self, key, hash_func)`

```python
def insert(self, key, hash_func):
    index = hash_func(key, self.size)
    start = index

    while self.table[index] is not None:
        if self.table[index] == key:
            return  # Duplicate — do not insert
        index = (index + 1) % self.size
        if index == start:
            raise Exception("Hash table is full")

    self.table[index] = key
```

**Step-by-step breakdown:**

| Step | Code | Purpose |
|---|---|---|
| Generate index | `index = hash_func(key, self.size)` | Computes the starting position for the key. |
| Check for collision | `while self.table[index] is not None` | Enters a probing loop if the slot is occupied. |
| Prevent duplicates | `if self.table[index] == key` | Stops insertion if the key already exists. |
| Linear probe | `index = (index + 1) % self.size` | Moves to the next slot; `%` wraps index `9` back to `0`. |
| Full table check | `if index == start` | If we've looped back to the start, the table is completely full. |

> **Key Concept — Modulo Wrapping:** The expression `(index + 1) % self.size` is what makes the probing "circular." When we reach the last slot, we seamlessly wrap back to index `0` instead of going out of bounds.

---

### `search(self, key, hash_func)`

```python
def search(self, key, hash_func):
    index = hash_func(key, self.size)
    start = index

    while self.table[index] is not None:
        if self.table[index] == key:
            return index  # Found!
        index = (index + 1) % self.size
        if index == start:
            break

    return -1  # Not found
```

- Follows the **exact same probe path** used during insertion.
- If a `None` slot is encountered before finding the key, the search stops — the key is definitively not in the table (it would have been placed before this empty gap).

---

### `delete(self, key, hash_func)`

```python
def delete(self, key, hash_func):
    index = self.search(key, hash_func)
    if index != -1:
        self.table[index] = None
```

- Locates the key's index via `search()` and clears it by setting it to `None`.

> ⚠️ **Technical Note — The Tombstone Problem:**
> Simply setting a deleted slot back to `None` can **"break the probe chain"** for elements that were displaced past that slot during an earlier insertion. In production systems, a special **"Tombstone"** marker (e.g., `"DELETED"`) is placed instead, signaling to `search()` to keep probing past it rather than stopping.

---

## 🔗 Part 2: Separate Chaining — `Node` & `ChainingHashTable`

This version resolves collisions by maintaining a **Linked List at every index**. Instead of displacing keys to nearby slots, all keys that hash to the same index are chained together vertically.

### The `Node` Class

Represents a single link in a chain.

```python
class Node:
    def __init__(self, key):
        self.key = key
        self.next = None
```

| Attribute | Description |
|---|---|
| `self.key` | The actual data value stored in this node. |
| `self.next` | A pointer to the next node in the list (`None` if it's the last node). |

---

### `ChainingHashTable` — `insert(self, key, hash_func)`

```python
def insert(self, key, hash_func):
    index = hash_func(key, self.size)
    current = self.table[index]

    # Check for duplicates
    while current:
        if current.key == key:
            return
        current = current.next

    # Insert at head of list — O(1)
    new_node = Node(key)
    new_node.next = self.table[index]
    self.table[index] = new_node
```

**Key detail — Head Insertion:**
The new node is inserted at the **head** (front) of the list:
```
new_node.next = self.table[index]   # New node points to old head
self.table[index] = new_node         # New node becomes the new head
```
This is a highly efficient $O(1)$ operation since no traversal to the tail is needed.

---

### `ChainingHashTable` — `delete(self, key, hash_func)`

```python
def delete(self, key, hash_func):
    index = hash_func(key, self.size)
    current = self.table[index]
    prev = None

    while current:
        if current.key == key:
            if prev:
                prev.next = current.next  # Bypass the deleted node
            else:
                self.table[index] = current.next  # Deleted node was the head
            return
        prev = current
        current = current.next
```

**Standard Linked List deletion logic:**

1. Track a `prev` (previous) pointer alongside `current` as you traverse.
2. When the target key is found, "snip" it out by connecting `prev.next` directly to `current.next`, skipping over the deleted node entirely.
3. If the node to delete is the **head** of the list (i.e., `prev` is still `None`), update the table's reference to the head directly.

```
Before: [prev] --> [current (DELETE ME)] --> [next]
After:  [prev] --------------------------------> [next]
```

---

## 🔢 Part 3: The Hashing Algorithms

These functions are the **"brains"** that decide where data lives in the table. A good hash function distributes keys evenly to minimize collisions.

### Mid-Square Hash

```python
def mid_square_hash(key, table_size):
    square = key * key
    square_str = str(square)
    mid = len(square_str) // 2
    value = int(square_str[mid])
    return value % table_size
```

**How it works, step by step:**

| Step | Example (`key = 42`) | Purpose |
|---|---|---|
| `square = key * key` | `42 * 42 = 1764` | Squaring spreads out the digit distribution. |
| `square_str = str(square)` | `"1764"` | Converts to a string to easily index individual digits. |
| `mid = len(square_str) // 2` | `4 // 2 = 2` → index `2` → digit `'6'` | Extracts the middle digit (most "mixed" part of the square). |
| `return value % table_size` | `6 % 10 = 6` | Ensures the result is a valid index within the table bounds. |

---

### Folding Hash

```python
def folding_hash(key, table_size):
    key_str = str(key)
    total = 0
    for i in range(0, len(key_str), 2):
        total += int(key_str[i:i + 2])
    return total % table_size
```

**How it works, step by step:**

| Step | Example (`key = 123456`) | Purpose |
|---|---|---|
| `key_str = str(key)` | `"123456"` | Converts the key to a string for slicing. |
| Loop in steps of 2 | `"12"`, `"34"`, `"56"` | Splits ("folds") the key into two-digit chunks. |
| `total += int(key_str[i:i+2])` | `12 + 34 + 56 = 102` | Sums all the chunks together. |
| `return total % table_size` | `102 % 10 = 2` | Returns the remainder as the final index. |

> The name "folding" comes from the idea of folding a long strip of paper — each fold layers a portion on top of the others before combining them.

---

## 🚀 Part 4: Main Execution (`__main__`)

The script tests **four specific combinations** to allow direct comparison of how each hash function and collision strategy interact:

| Instance | Collision Strategy | Hash Function | Key Behavior |
|---|---|---|---|
| `HT1` | Linear Probing | Mid-Square | Keys may be "pushed" to nearby indices |
| `HT2` | Separate Chaining | Mid-Square | Keys chain vertically at shared indices |
| `HT3` | Linear Probing | Folding | Keys may be "pushed" to nearby indices |
| `HT4` | Separate Chaining | Folding | Keys chain vertically at shared indices |

### Observable Difference

By comparing the printed outputs:

- **Linear Probing** (HT1, HT3): When collisions occur, keys get displaced to adjacent empty slots — you'll see keys clustered at consecutive indices like `4, 5, 6`.
- **Separate Chaining** (HT2, HT4): Collisions result in vertical lists at a single index — you'll see chains like `1 -> 9 -> None` at one slot.

---

## 📊 Part 5: Feature Comparison

| Feature | `HashTable` (Linear Probing) | `ChainingHashTable` (Separate Chaining) |
|---|---|---|
| **Storage Location** | Elements stored directly inside the table array. | Elements stored in external Linked Lists. |
| **Table Capacity** | Strict limit based on `size`. Cannot exceed it. | Theoretically infinite (limited only by memory). |
| **On Collision** | Key is displaced to the next available slot. | Key is prepended to the list at that index. |
| **Search Speed** | Degrades as the table fills up (longer probe chains). | Degrades as individual chains grow longer. |
| **Memory Usage** | More cache-friendly (data is contiguous in memory). | Extra memory used for `Node` objects and pointers. |
| **Deletion Complexity** | Risk of breaking probe chains (requires Tombstones). | Clean pointer re-linking; no side effects on other keys. |
| **Best Used When** | Table size is known and load factor stays low. | Key distribution is unpredictable or table may overflow. |
