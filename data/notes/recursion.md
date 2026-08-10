# DSA Coach — Recursion

## 1. Factorial Using Recursion

Find the factorial of a number using recursion.

Example:

5! = 5 × 4 × 3 × 2 × 1

Output:

120

Recursive relation:

factorial(n) = n × factorial(n-1)

Base case:

factorial(0) = 1

DSA Coach Hint:

Every recursive solution needs:

1. Base case
2. Recursive case

---

## 2. Fibonacci Number

Find the Nth Fibonacci number using recursion.

Example:

0, 1, 1, 2, 3, 5, 8...

For:

N = 5

Output:

5

Recursive relation:

fib(n) = fib(n-1) + fib(n-2)

DSA Coach Hint:

Always identify the smallest cases first.

---

## 3. Sum of First N Numbers

Find the sum of numbers from 1 to N using recursion.

Example:

N = 5

Output:

15

Because:

1 + 2 + 3 + 4 + 5 = 15

Recursive relation:

sum(n) = n + sum(n-1)

Base case:

sum(0) = 0

---

## 4. Power of a Number

Calculate x raised to the power n using recursion.

Example:

2^5

Output:

32

Recursive relation:

power(x,n) = x × power(x,n-1)

The optimized recursive approach using exponentiation by squaring can run in O(log n).

DSA Coach Hint:

If n is even:

x^n = (x^(n/2))²

---

## 5. Reverse a String

Reverse a string recursively.

Example:

Input:

"hello"

Output:

"olleh"

The problem can be solved by recursively processing the remaining characters.

DSA Coach Hint:

Ask:

"What smaller version of the same problem can I solve?"

---

## 6. Check Palindrome Recursively

Determine whether a string is a palindrome using recursion.

Example:

"madam"

Output:

True

Compare the first and last characters.

Then recursively check the remaining substring.

DSA Coach Hint:

Compare:

left ↔ right

Then move:

left++

right--

---

## 7. Sum of Digits

Find the sum of all digits of a number recursively.

Example:

Input:

12345

Output:

15

Because:

1 + 2 + 3 + 4 + 5 = 15

Use:

n % 10

to extract the last digit.

Then recursively process:

n / 10

---

## 8. Count Digits

Count the number of digits in an integer using recursion.

Example:

Input:

12345

Output:

5

Remove one digit at every recursive call.

Base case:

n == 0

DSA Coach Hint:

Every division by 10 removes one digit.

---

## 9. Greatest Common Divisor

Find the GCD of two numbers using recursion.

Example:

GCD(48, 18)

Output:

6

Euclid's algorithm:

gcd(a,b) = gcd(b, a % b)

Base case:

b == 0

DSA Coach Hint:

When you see GCD, think:

Euclidean Algorithm.

---

## 10. Binary Search Recursively

Search for an element in a sorted array using recursive binary search.

Example:

[10, 20, 30, 40, 50]

Target:

40

Output:

Index 3

At each step, search only one half of the array.

The time complexity is O(log n).

DSA Coach Hint:

Every recursive call reduces the search space by half.

---

## 11. Generate All Subsequences

Generate all possible subsequences of a string.

Example:

Input:

"ab"

Possible subsequences:

""
"a"
"b"
"ab"

Each character provides two choices:

- Include it
- Exclude it

The number of subsequences is 2^n.

DSA Coach Hint:

At every element:

Take

OR

Not Take

---

## 12. Generate Permutations

Generate all permutations of a string.

Example:

Input:

"abc"

Output includes:

abc
acb
bac
bca
cab
cba

Recursion can be used by fixing one character at a time.

DSA Coach Hint:

Think:

Choose → Explore → Undo

This is the basic backtracking pattern.

---

## 13. Tower of Hanoi

Move N disks from one rod to another using an auxiliary rod.

Rules:

- Move only one disk at a time.
- A larger disk cannot be placed on a smaller disk.

For N disks, the minimum number of moves is:

2^N - 1

DSA Coach Hint:

The recursive structure is:

Move N-1 disks

Move largest disk

Move N-1 disks again

---

## 14. Count Paths in a Grid

Find the number of ways to move from the top-left corner to the bottom-right corner.

Allowed moves:

- Right
- Down

Example:

For a small grid, recursively calculate paths from each cell.

The naive recursive solution may have exponential time complexity.

DSA Coach Hint:

If the same grid positions are calculated repeatedly, think:

Memoization.

---

## 15. Solve Maze Using Backtracking

Given a maze, find a path from the starting cell to the destination.

A cell can be visited only if it is valid and unvisited.

At each cell, explore possible directions.

If a path does not lead to the destination, backtrack.

DSA Coach Hint:

Backtracking pattern:

Choose → Explore → Undo

Always mark visited cells to avoid infinite recursion.