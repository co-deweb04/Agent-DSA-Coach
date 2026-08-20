# DSA Coach — Linked Lists

## 1. Linked List Traversal

Traversal means visiting every node of a linked list one by one.

Example:

10 → 20 → 30 → 40 → NULL

A traversal visits:

10 → 20 → 30 → 40

The time complexity is O(n) because every node is visited once.

Traversal is commonly used for:

- Searching
- Finding maximum
- Finding minimum
- Calculating sum
- Counting nodes
- Updating nodes

DSA Coach Hint:

If a problem asks you to inspect every node, first ask:

"Can I solve this using a single traversal?"

---

## 2. Insert Node at Beginning

Insert a new node at the beginning of a linked list.

Example:

Before:

20 → 30 → 40 → NULL

Insert:

10

After:

10 → 20 → 30 → 40 → NULL

The new node becomes the head of the linked list.

Insertion at the beginning takes O(1) time.

DSA Coach Hint:

Create a new node and make:

newNode.next = head

Then update:

head = newNode

---

## 3. Insert Node at End

Insert a new node at the end of a linked list.

Example:

Before:

10 → 20 → 30 → NULL

Insert:

40

After:

10 → 20 → 30 → 40 → NULL

If there is no tail pointer, traversal to the last node is required.

The time complexity is O(n).

DSA Coach Hint:

Move until:

current.next == NULL

Then connect the new node.

---

## 4. Insert Node at a Given Position

Insert a new node at a specified position.

Example:

10 → 20 → 40

Insert 30 at position 3.

Result:

10 → 20 → 30 → 40

The list must be traversed until the node before the required position.

The time complexity is O(n).

DSA Coach Hint:

To insert between two nodes:

1. Find previous node.
2. Connect new node to next node.
3. Connect previous node to new node.

---

## 5. Delete Node from Beginning

Delete the first node of a linked list.

Example:

Before:

10 → 20 → 30 → NULL

After deletion:

20 → 30 → NULL

The head pointer is moved to the second node.

The time complexity is O(1).

DSA Coach Hint:

Simply move:

head = head.next

Be careful when the list is empty.

---

## 6. Delete Node from End

Delete the last node of a linked list.

Example:

Before:

10 → 20 → 30 → NULL

After:

10 → 20 → NULL

The second-last node must point to NULL.

The time complexity is O(n) for a singly linked list without a tail/previous pointer.

DSA Coach Hint:

Find the second-last node.

Then set:

secondLast.next = NULL

---

## 7. Search an Element

Search for a given value in a linked list.

Example:

10 → 20 → 30 → 40

Search:

30

Output:

Element found.

Since linked lists do not provide direct indexing, nodes must be checked sequentially.

The time complexity is O(n).

DSA Coach Hint:

Start from head and compare:

current.data == target

---

## 8. Find Length of Linked List

Find the total number of nodes in a linked list.

Example:

10 → 20 → 30 → 40 → NULL

Length:

4

Traverse the complete list and increase a counter for every node.

The time complexity is O(n).

DSA Coach Hint:

Maintain:

count = 0

For every node:

count++

---

## 9. Reverse a Linked List

Reverse the links of a singly linked list.

Example:

Before:

10 → 20 → 30 → 40 → NULL

After:

40 → 30 → 20 → 10 → NULL

Three pointers can be used:

- previous
- current
- next

The time complexity is O(n).

DSA Coach Hint:

Before changing current.next, save it first:

next = current.next

Otherwise, the remaining list may be lost.

---

## 10. Find Middle Node

Find the middle node of a linked list.

Example:

10 → 20 → 30 → 40 → 50

Middle:

30

A slow and fast pointer approach can solve this efficiently.

Slow moves one step.

Fast moves two steps.

The time complexity is O(n).

DSA Coach Hint:

When fast reaches the end, slow will be at the middle.

Think:

slow → 1 step

fast → 2 steps

---

## 11. Detect Cycle

Determine whether a linked list contains a cycle.

Example:

10 → 20 → 30 → 40
          ↑       |
          |_______|

The list contains a cycle.

Floyd's Cycle Detection Algorithm uses two pointers:

- slow
- fast

If they meet, a cycle exists.

The time complexity is O(n).

DSA Coach Hint:

Cycle detection:

slow = slow.next

fast = fast.next.next

If slow == fast, a cycle exists.

---

## 12. Remove Cycle

Detect and remove a cycle from a linked list.

Example:

10 → 20 → 30 → 40
          ↑       |
          |_______|

After removing the cycle:

10 → 20 → 30 → 40 → NULL

Floyd's cycle detection algorithm can first be used to detect the cycle.

Then the cycle's starting point must be identified.

DSA Coach Hint:

First detect the cycle.

Do not try to remove it before knowing where the cycle starts.

---

## 13. Merge Two Sorted Linked Lists

Merge two sorted linked lists into one sorted linked list.

Example:

List 1:

10 → 30 → 50

List 2:

20 → 40 → 60

Result:

10 → 20 → 30 → 40 → 50 → 60

Compare the current nodes of both lists and attach the smaller node.

The time complexity is O(n + m).

DSA Coach Hint:

Always compare:

list1.data

and

list2.data

Then move the pointer belonging to the smaller value.

---

## 14. Remove Duplicates from Sorted List

Remove duplicate values from a sorted linked list.

Example:

10 → 20 → 20 → 30 → 30

Result:

10 → 20 → 30

Because the list is sorted, duplicate values will be adjacent.

The time complexity is O(n).

DSA Coach Hint:

Compare:

current.data

with:

current.next.data

If they are equal, skip the next node.

---

## 15. Check if Linked List is Palindrome

Determine whether the values in a linked list form a palindrome.

Example:

10 → 20 → 30 → 20 → 10

Output:

Palindrome

One efficient approach is:

1. Find the middle.
2. Reverse the second half.
3. Compare both halves.

The time complexity is O(n).

DSA Coach Hint:

Linked lists do not support reverse indexing.

Use slow/fast pointers and reversal instead.