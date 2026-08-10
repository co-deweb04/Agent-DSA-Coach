# DSA Coach — Graphs

## 1. Graph Representation

Represent a graph using:

- Adjacency Matrix
- Adjacency List

Example:

A — B
|   |
C — D

An adjacency list stores the neighbors of every vertex.

For sparse graphs, adjacency lists are generally more space efficient.

DSA Coach Hint:

Ask:

"Is this graph sparse or dense?"

This helps choose the representation.

---

## 2. Breadth First Search

Perform BFS traversal of a graph.

BFS visits nodes level by level.

A queue is used.

Example:

A → B → C
|       |
D       E

Possible BFS:

A → B → C → D → E

The time complexity is O(V + E).

DSA Coach Hint:

BFS = Queue + Visited array/set.

---

## 3. Depth First Search

Perform DFS traversal of a graph.

DFS explores as deeply as possible before backtracking.

It can be implemented using:

- Recursion
- Stack

The time complexity is O(V + E).

DSA Coach Hint:

DFS = Stack/Recursion + Visited array/set.

---

## 4. Detect Cycle in Undirected Graph

Determine whether an undirected graph contains a cycle.

DFS or BFS can be used while keeping track of the parent node.

Example:

A — B
|   |
C — D

A cycle exists if we encounter an already visited node that is not the parent.

The time complexity is O(V + E).

DSA Coach Hint:

Visited neighbor + neighbor is not parent

means a cycle may exist.

---

## 5. Detect Cycle in Directed Graph

Determine whether a directed graph contains a cycle.

Example:

A → B → C
    ↑   |
    |___|

DFS with a recursion stack can detect back edges.

The time complexity is O(V + E).

DSA Coach Hint:

For directed graphs, maintain:

visited[]

and

recursionStack[]

---

## 6. Number of Connected Components

Find the number of connected components in an undirected graph.

Example:

A — B       C — D

There are:

2 connected components.

Run DFS/BFS from every unvisited vertex.

Each new traversal represents one component.

DSA Coach Hint:

For every unvisited node:

start a new DFS/BFS

and increase the component count.

---

## 7. Number of Islands

Given a grid containing land and water, count the number of islands.

Example:

1 1 0
0 1 0
1 0 1

Connected groups of 1s represent islands.

DFS or BFS can be used.

The time complexity is O(rows × columns).

DSA Coach Hint:

Every unvisited land cell can be the start of a new island.

---

## 8. Shortest Path in an Unweighted Graph

Find the shortest path between two vertices in an unweighted graph.

BFS can find the shortest path because every edge has equal cost.

Example:

A — B — C
|       |
D — E — F

Find shortest path from A to F.

DSA Coach Hint:

Unweighted graph + shortest path

→ BFS

---

## 9. Bipartite Graph

Determine whether a graph is bipartite.

A graph is bipartite if its vertices can be divided into two sets such that no two vertices in the same set are connected.

Color vertices using two colors.

If adjacent vertices require the same color, the graph is not bipartite.

DSA Coach Hint:

Think:

Graph coloring with 2 colors.

---

## 10. Topological Sorting

Find a valid ordering of vertices in a Directed Acyclic Graph.

Example:

A → C
B → C
C → D

Possible ordering:

A → B → C → D

Kahn's Algorithm uses indegrees and a queue.

DFS can also be used.

DSA Coach Hint:

Topological sorting works only for:

DAG — Directed Acyclic Graph.

---

## 11. Course Schedule

Given courses and prerequisite relationships, determine whether all courses can be completed.

Example:

Course 1 requires Course 0.

Then:

0 → 1

If prerequisites form a cycle, completing all courses is impossible.

Cycle detection or topological sorting can solve the problem.

DSA Coach Hint:

Course prerequisites naturally form a directed graph.

Look for cycles.

---

## 12. Dijkstra's Shortest Path

Find the shortest distance from a source vertex to all other vertices in a weighted graph with non-negative edge weights.

Example:

A --4-- B
|       |
2       1
|       |
C --3-- D

Dijkstra's algorithm repeatedly selects the closest unvisited vertex.

A priority queue is commonly used.

The time complexity with a binary heap is O((V + E) log V).

DSA Coach Hint:

Dijkstra works with:

Non-negative edge weights.

---

## 13. Minimum Spanning Tree

Find a minimum spanning tree of a weighted undirected graph.

Two common algorithms are:

- Prim's Algorithm
- Kruskal's Algorithm

The goal is to connect all vertices with minimum total edge weight.

DSA Coach Hint:

MST should:

- Connect all vertices.
- Contain no cycles.
- Have minimum total weight.

---

## 14. Flood Fill

Given a grid and a starting cell, change the color of all connected cells having the same original color.

Example:

1 1 1
1 1 0
1 0 1

Starting from the center, change the connected region.

DFS or BFS can be used.

The time complexity is O(rows × columns).

DSA Coach Hint:

This is essentially graph traversal on a grid.

---

## 15. Word Ladder

Transform one word into another by changing one character at a time.

Each intermediate word must belong to a given dictionary.

Example:

hit → hot → dot → dog → cog

The goal is to find the shortest transformation sequence.

BFS is commonly used because every transformation has equal cost.

DSA Coach Hint:

Each word can be treated as a graph node.

A valid one-character transformation creates an edge.