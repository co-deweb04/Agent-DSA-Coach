# DSA Coach — Trees

## 1. Tree Traversal

Tree traversal means visiting every node of a tree.

The three major DFS traversals are:

- Inorder
- Preorder
- Postorder

Example:

      1
     / \
    2   3

Inorder:

2 → 1 → 3

Preorder:

1 → 2 → 3

Postorder:

2 → 3 → 1

A traversal takes O(n) time because every node is visited once.

DSA Coach Hint:

If a problem asks you to visit every node, think about tree traversal.

---

## 2. Inorder Traversal

Inorder traversal follows:

Left → Root → Right

Example:

      1
     / \
    2   3

Inorder:

2 → 1 → 3

In a Binary Search Tree, inorder traversal produces elements in sorted order.

The time complexity is O(n).

DSA Coach Hint:

Remember:

L → N → R

Left → Node → Right

---

## 3. Preorder Traversal

Preorder traversal follows:

Root → Left → Right

Example:

      1
     / \
    2   3

Preorder:

1 → 2 → 3

It is useful when creating a copy of a tree or representing its structure.

The time complexity is O(n).

DSA Coach Hint:

Remember:

N → L → R

Node → Left → Right

---

## 4. Postorder Traversal

Postorder traversal follows:

Left → Right → Root

Example:

      1
     / \
    2   3

Postorder:

2 → 3 → 1

It is useful when deleting nodes because children are processed before the parent.

The time complexity is O(n).

DSA Coach Hint:

Remember:

L → R → N

---

## 5. Find Height of a Binary Tree

The height of a tree represents the longest path from the root to a leaf.

Example:

      1
     /
    2
   /
  3

The height is 2 if height is counted using edges.

The height can be calculated recursively.

For every node:

height = 1 + max(leftHeight, rightHeight)

The time complexity is O(n).

DSA Coach Hint:

A leaf node has height 0 when using edge-based height.

---

## 6. Count Number of Nodes

Given a binary tree, count the total number of nodes.

Example:

      1
     / \
    2   3
   /
  4

Total nodes:

4

Recursively count:

left subtree + right subtree + current node.

The time complexity is O(n).

DSA Coach Hint:

For every node:

count = 1 + left + right

---

## 7. Find Maximum Element in Binary Tree

Given a binary tree, find the maximum value stored in any node.

Example:

      10
     /  \
    5    20
        /
       15

Maximum:

20

Every node needs to be inspected.

The time complexity is O(n).

DSA Coach Hint:

Maintain a maximum value while traversing the tree.

---

## 8. Find Minimum Element in Binary Search Tree

Given a Binary Search Tree, find the minimum value.

Example:

       8
      / \
     4   12
    /
   2

Minimum:

2

In a BST, the minimum element is present at the leftmost node.

The time complexity is O(h), where h is the height of the tree.

DSA Coach Hint:

BST property:

Left < Root < Right

Therefore, keep moving left.

---

## 9. Search in Binary Search Tree

Given a value, search for it in a Binary Search Tree.

Example:

       8
      / \
     4   12
    / \
   2   6

Search:

6

Start at 8.

Since 6 < 8, move left.

Since 6 > 4, move right.

6 is found.

The average time complexity is O(log n) for a balanced BST.

DSA Coach Hint:

Do not traverse the entire tree unnecessarily.

Use the BST property.

---

## 10. Insert into Binary Search Tree

Insert a new value into a Binary Search Tree while maintaining the BST property.

Example:

       8
      / \
     4   12

Insert:

6

Since:

6 < 8

move left.

Since:

6 > 4

move right.

The new node is inserted at the correct position.

The average time complexity is O(log n).

DSA Coach Hint:

At every node ask:

"Should I go left or right?"

---

## 11. Check if Two Trees are Identical

Given two binary trees, determine whether they have exactly the same structure and values.

Example:

Tree 1:

    1
   / \
  2   3

Tree 2:

    1
   / \
  2   3

Both trees are identical.

The solution recursively compares:

- Current node values
- Left subtrees
- Right subtrees

The time complexity is O(n).

DSA Coach Hint:

Two nodes are equal only when:

value is same

AND

left subtrees are same

AND

right subtrees are same.

---

## 12. Check if a Binary Tree is Balanced

A binary tree is balanced when the height difference between the left and right subtree of every node is not more than 1.

Example:

      1
     / \
    2   3
   /
  4

This tree is balanced.

An unbalanced tree may look like:

1
 \
  2
   \
    3

The time complexity can be O(n) using an optimized approach.

DSA Coach Hint:

For every node check:

|leftHeight - rightHeight| <= 1

---

## 13. Level Order Traversal

Visit the nodes of a binary tree level by level.

Example:

       1
      / \
     2   3
    / \
   4   5

Level order:

1 → 2 → 3 → 4 → 5

A queue is used to process nodes level by level.

The time complexity is O(n).

DSA Coach Hint:

Whenever you see:

"level by level"

think:

Queue + BFS.

---

## 14. Find Lowest Common Ancestor

Given two nodes in a tree, find their lowest common ancestor.

Example:

       1
      / \
     2   3
    / \
   4   5

For nodes:

4 and 5

The lowest common ancestor is:

2

The problem requires understanding the relationship between nodes and their ancestors.

DSA Coach Hint:

Ask:

"Is one target present in the left subtree and the other in the right subtree?"

If yes, the current node may be the answer.

---

## 15. Diameter of a Binary Tree

The diameter of a binary tree is the longest path between any two nodes.

Example:

       1
      / \
     2   3
    / \
   4   5

One longest path is:

4 → 2 → 1 → 3

The diameter is 3 edges.

The solution uses subtree heights.

The optimized approach takes O(n) time.

DSA Coach Hint:

At every node, consider:

leftHeight + rightHeight

This gives the longest path passing through that node.