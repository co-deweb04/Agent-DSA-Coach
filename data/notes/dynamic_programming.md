# DSA Coach — Dynamic Programming

## 1. Fibonacci Using Dynamic Programming

Find the Nth Fibonacci number using Dynamic Programming.

Example:

0, 1, 1, 2, 3, 5, 8...

For:

N = 6

Output:

8

Instead of repeatedly calculating the same values, store previously calculated results.

This can reduce the time complexity from exponential to O(n).

DSA Coach Hint:

If recursion calculates the same state multiple times, think:

"Can I store the answer?"

---

## 2. Climbing Stairs

You are climbing a staircase with N steps.

You can climb either:

- 1 step
- 2 steps

Find the number of distinct ways to reach the top.

Example:

N = 3

Ways:

1 + 1 + 1
1 + 2
2 + 1

Output:

3

The recurrence is:

dp[n] = dp[n-1] + dp[n-2]

DSA Coach Hint:

Ask:

"What were the possible ways to reach the previous states?"

---

## 3. House Robber

Given an array representing money in houses, find the maximum money that can be robbed without robbing two adjacent houses.

Example:

[2, 7, 9, 3, 1]

Maximum:

12

Choose:

2 + 9 + 1

At every house, choose between:

- Rob current house.
- Skip current house.

DSA Coach Hint:

State:

dp[i] = maximum money from first i houses.

---

## 4. Maximum Sum Subarray

Find the contiguous subarray having the maximum sum.

Example:

[-2, 1, -3, 4, -1, 2, 1, -5, 4]

Maximum subarray:

[4, -1, 2, 1]

Maximum sum:

6

Kadane's Algorithm solves this in O(n).

DSA Coach Hint:

At every element ask:

"Should I extend the previous subarray or start a new one?"

---

## 5. Coin Change

Given coin denominations and a target amount, find the minimum number of coins required.

Example:

Coins:

[1, 2, 5]

Amount:

11

Output:

3

Because:

5 + 5 + 1 = 11

Dynamic Programming can store the minimum coins needed for every smaller amount.

DSA Coach Hint:

Define:

dp[amount] = minimum coins required.

---

## 6. Coin Change — Number of Ways

Given coin denominations and an amount, count the number of combinations that produce that amount.

Example:

Coins:

[1, 2, 5]

Amount:

5

Possible combinations include:

5

2 + 2 + 1

2 + 1 + 1 + 1

and so on.

The order of coins does not create a new combination.

DSA Coach Hint:

Carefully decide whether:

order matters

or

order does not matter.

---

## 7. 0/1 Knapsack

Given items with weights and values, choose items to maximize total value without exceeding the bag capacity.

Each item can be selected at most once.

Example:

Weights:

[1, 3, 4]

Values:

[15, 20, 30]

Capacity:

4

Choose the combination with maximum value.

DSA Coach Hint:

For every item:

Take it

OR

Don't take it.

---

## 8. Longest Common Subsequence

Given two strings, find the length of their longest common subsequence.

Example:

String 1:

"abcde"

String 2:

"ace"

LCS:

"ace"

Length:

3

The characters do not need to be consecutive.

DSA Coach Hint:

If characters match:

dp[i][j] = 1 + dp[i-1][j-1]

Otherwise, take the better of the two possibilities.

---

## 9. Longest Increasing Subsequence

Find the length of the longest subsequence where elements are strictly increasing.

Example:

[10, 9, 2, 5, 3, 7, 101, 18]

One LIS:

[2, 3, 7, 101]

Length:

4

A dynamic programming solution can be built using the previous elements.

DSA Coach Hint:

For every element, ask:

"Which smaller previous element can I extend?"

---

## 10. Edit Distance

Find the minimum number of operations required to convert one string into another.

Allowed operations:

- Insert
- Delete
- Replace

Example:

"horse"

→

"ros"

The minimum number of operations is 3.

A 2D DP table can store answers for smaller prefixes.

DSA Coach Hint:

When the characters match:

No operation is required.

Otherwise consider:

Insert / Delete / Replace.

---

## 11. Partition Equal Subset Sum

Determine whether an array can be divided into two subsets having equal sums.

Example:

[1, 5, 11, 5]

Total sum:

22

Target for each subset:

11

Possible partition:

[11]

and

[1, 5, 5]

Output:

True

This can be reduced to a subset-sum problem.

DSA Coach Hint:

First calculate:

totalSum

If totalSum is odd, equal partition is impossible.

---

## 12. Subset Sum

Determine whether there exists a subset whose sum equals a given target.

Example:

Array:

[2, 3, 7, 8, 10]

Target:

11

Subset:

[3, 8]

Output:

True

Each element provides two choices:

- Include
- Exclude

DSA Coach Hint:

This is a classic:

Take / Not Take

DP problem.

---

## 13. Minimum Path Sum

Given a grid containing positive numbers, find the minimum sum path from the top-left to the bottom-right.

Allowed moves:

- Right
- Down

Example:

1 3 1
1 5 1
4 2 1

The minimum path has the smallest possible total.

DP stores the minimum cost required to reach each cell.

DSA Coach Hint:

Current cell cost:

grid[i][j] + minimum(previous paths)

---

## 14. Unique Paths

Find the number of different paths from the top-left to the bottom-right of an m × n grid.

Allowed moves:

- Right
- Down

Example:

For a 2 × 2 grid:

There are:

2

possible paths.

DP can store the number of ways to reach each cell.

DSA Coach Hint:

For every cell:

ways = top + left

---

## 15. Matrix Chain Multiplication

Given a sequence of matrices, find the minimum number of scalar multiplications required to multiply them.

Example:

A × B × C

Different parenthesizations can require different numbers of operations.

The goal is to find the optimal multiplication order.

Dynamic Programming is used because the problem contains overlapping subproblems and optimal substructure.

DSA Coach Hint:

Think:

"Where should I split the matrix chain?"

Try every possible partition and choose the minimum cost.