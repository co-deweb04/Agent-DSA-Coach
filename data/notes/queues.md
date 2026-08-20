# DSA Coach — Queues

## 1. Queue Operations

A queue is a linear data structure that follows:

FIFO — First In, First Out.

Example:

10 → 20 → 30

The element 10 entered first.

Therefore, 10 will leave first.

Common operations are:

- enqueue()
- dequeue()
- peek()
- isEmpty()

DSA Coach Hint:

Whenever you see:

"First come, first served"

think QUEUE.

---

## 2. Implement Queue Using Array

Implement a queue using an array.

The queue should support:

- enqueue
- dequeue
- peek
- isEmpty

Example:

Enqueue:

10 → 20 → 30

Dequeue:

10

The front points to the first element.

The rear points to the last element.

DSA Coach Hint:

Remember:

Insertion → Rear

Deletion → Front

---

## 3. Implement Circular Queue

Implement a circular queue where the last position connects back to the first position.

Example:

[10, 20, 30, 40, 50]

After removing 10 and 20, the empty spaces can be reused.

This avoids unnecessary wastage of array space.

The enqueue and dequeue operations take O(1) time.

DSA Coach Hint:

Use modulo:

(rear + 1) % size

---

## 4. Queue Using Two Stacks

Implement a queue using two stacks.

The queue follows FIFO, while stacks follow LIFO.

Use two stacks to reverse the order appropriately.

Operations:

- enqueue
- dequeue
- peek

DSA Coach Hint:

One stack can be used for insertion.

The second stack can be used for removal.

---

## 5. Stack Using Two Queues

Implement a stack using two queues.

The resulting data structure should follow LIFO even though queues follow FIFO.

Operations:

- push
- pop
- peek

DSA Coach Hint:

To make a queue behave like a stack, rearrange the elements during push or pop.

---

## 6. Generate Binary Numbers Using Queue

Generate binary numbers from 1 to N using a queue.

Example:

Input:

N = 5

Output:

1
10
11
100
101

A queue can store previously generated binary strings.

For every value:

Append 0

Append 1

DSA Coach Hint:

This is a good example of using BFS-like processing with a queue.

---

## 7. First Non-Repeating Character in a Stream

Given characters arriving one by one, find the first non-repeating character after every insertion.

Example:

Input:

a a b c

Output:

a
-1
b
b

A frequency array/map and queue can be used.

The queue stores possible non-repeating characters.

DSA Coach Hint:

Frequency tells you whether a character is repeating.

Queue maintains the order.

---

## 8. Reverse a Queue

Reverse all elements of a queue.

Example:

Input:

10 → 20 → 30 → 40

Output:

40 → 30 → 20 → 10

A stack can temporarily store the queue elements.

The time complexity is O(n).

DSA Coach Hint:

Queue gives FIFO.

Stack gives LIFO.

Combining them reverses the order.

---

## 9. Generate Numbers with Given Digits

Given a set of digits, generate numbers using those digits in a particular order.

Example:

Digits:

5, 6

Generated numbers:

5
6
55
56
65
66

A queue can be used to generate numbers level by level.

DSA Coach Hint:

Think about the problem as generating the next level from the current level.

---

## 10. Sliding Window Maximum

Given an array and a window size K, find the maximum element in every window.

Example:

Input:

[1, 3, -1, -3, 5, 3, 6, 7]

K = 3

Output:

[3, 3, 5, 5, 6, 7]

A deque can solve this problem efficiently.

The time complexity is O(n).

DSA Coach Hint:

For every window, maintain only elements that can become maximum.

---

## 11. Number of Recent Calls

Given timestamps of requests, find how many requests occurred within the last fixed time period.

Example:

Requests:

1
100
3001
3002

For each new request, remove timestamps outside the valid window.

A queue is ideal because timestamps arrive in increasing order.

DSA Coach Hint:

Oldest request is always at the front.

Remove it when it becomes invalid.

---

## 12. First K Elements of a Queue

Given a queue and an integer K, reverse only the first K elements while keeping the remaining elements in the same order.

Example:

Input:

1 → 2 → 3 → 4 → 5

K = 3

Output:

3 → 2 → 1 → 4 → 5

Use a stack to reverse the first K elements.

DSA Coach Hint:

Process only the first K elements.

Do not disturb the remaining elements.

---

## 13. BFS Traversal

Breadth First Search visits nodes level by level.

A queue is used to maintain the nodes waiting to be processed.

Example:

      1
     / \
    2   3
   / \
  4   5

BFS:

1 → 2 → 3 → 4 → 5

The time complexity is O(V + E) for a graph.

DSA Coach Hint:

Whenever the problem says:

"Level by level"

think QUEUE + BFS.

---

## 14. Task Scheduling

Given a list of tasks, process them in the order in which they arrive.

Example:

Tasks:

Task A
Task B
Task C

Processing order:

A → B → C

A queue can be used to maintain pending tasks.

When a task is completed, remove it from the front.

DSA Coach Hint:

Queues are useful whenever tasks need to be processed fairly in arrival order.

---

## 15. Josephus Problem

N people stand in a circle.

Starting from a particular person, every K-th person is removed until only one person remains.

Example:

N = 5
K = 2

People:

1 2 3 4 5

People are eliminated one by one according to the given step.

The goal is to find the last remaining person.

A circular queue can be used to simulate the process.

DSA Coach Hint:

Think about repeatedly moving through the queue and removing every K-th element.