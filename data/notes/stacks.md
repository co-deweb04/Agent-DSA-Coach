# DSA Coach — Stacks

## 1. Stack Operations

A stack is a linear data structure that follows:

LIFO — Last In, First Out.

Example:

Push: 10
Push: 20
Push: 30

Stack:

30 ← Top
20
10

If we perform pop(), 30 will be removed first.

Common stack operations are:

- push()
- pop()
- peek()
- isEmpty()

Most stack operations take O(1) time.

DSA Coach Hint:

Whenever you see:

"Last inserted element should come out first"

think STACK.

---

## 2. Implement Stack Using Array

Implement a stack using an array.

The stack should support:

- push
- pop
- peek
- isEmpty

Example:

Push:

10 → 20 → 30

Pop:

30

The top pointer keeps track of the current top element.

Push and pop operations take O(1) time.

DSA Coach Hint:

Maintain a variable:

top

to represent the top position.

---

## 3. Reverse a String Using Stack

Use a stack to reverse a string.

Example:

Input:

"hello"

Push every character:

h
e
l
l
o

Then pop them one by one:

o → l → l → e → h

Output:

"olleh"

The time complexity is O(n).

DSA Coach Hint:

Stack naturally reverses the order because it follows LIFO.

---

## 4. Check Balanced Parentheses

Given an expression, determine whether all parentheses are balanced.

Example:

Input:

"{[()]}"

Output:

Balanced

Example:

"{[(])}"

Output:

Not Balanced

Push opening brackets into a stack.

When a closing bracket appears, compare it with the top of the stack.

The time complexity is O(n).

DSA Coach Hint:

Opening bracket → PUSH

Closing bracket → MATCH + POP

---

## 5. Next Greater Element

For every element in an array, find the next greater element to its right.

Example:

Input:

[4, 5, 2, 10]

Output:

[5, 10, 10, -1]

A monotonic stack can solve this efficiently.

The time complexity is O(n).

DSA Coach Hint:

If the problem asks for:

"Next greater"

think about a stack.

---

## 6. Evaluate Postfix Expression

Evaluate an arithmetic expression written in postfix notation.

Example:

Input:

"23+"

Output:

5

For:

"23*54*+"

The stack stores operands.

When an operator appears, pop the required operands and perform the operation.

The time complexity is O(n).

DSA Coach Hint:

Operand → PUSH

Operator → POP operands → Calculate → PUSH result

---

## 7. Convert Infix to Postfix

Convert an infix expression into postfix notation.

Example:

Infix:

A + B * C

Postfix:

ABC*+

A stack is used to temporarily store operators.

Operator precedence must be considered.

The time complexity is O(n).

DSA Coach Hint:

Remember operator precedence:

^
* /
+ -

---

## 8. Remove Adjacent Duplicates

Given a string, repeatedly remove adjacent duplicate characters.

Example:

Input:

"abbaca"

Process:

abbaca
→ aaca
→ ca

Output:

"ca"

A stack can be used to keep track of the previous character.

The time complexity is O(n).

DSA Coach Hint:

If the current character equals the stack top:

POP

Otherwise:

PUSH

---

## 9. Min Stack

Design a stack that supports retrieving the minimum element in O(1) time.

Operations:

- push()
- pop()
- top()
- getMin()

Example:

Push:

5
3
7
2

Minimum:

2

Even after removing 2, the previous minimum should be available.

DSA Coach Hint:

Maintain an additional stack for minimum values.

---

## 10. Implement Two Stacks in One Array

Implement two independent stacks using a single array.

One stack grows from the beginning.

The other stack grows from the end.

Example:

Stack 1 → → →

← ← ← Stack 2

Both stacks should use the same array efficiently.

The goal is to avoid wasting unused space.

DSA Coach Hint:

Use:

top1 = -1

top2 = size

---

## 11. Stock Span Problem

For each day's stock price, find the number of consecutive previous days having a price less than or equal to today's price.

Example:

Prices:

[100, 80, 60, 70, 60, 75, 85]

Output:

[1, 1, 1, 2, 1, 4, 6]

A stack can maintain useful previous prices.

The time complexity is O(n).

DSA Coach Hint:

This is another classic monotonic stack problem.

---

## 12. Largest Rectangle in Histogram

Given heights of histogram bars, find the largest rectangular area.

Example:

Input:

[2, 1, 5, 6, 2, 3]

Output:

10

The rectangle using heights 5 and 6 produces the maximum area.

A monotonic stack can solve the problem efficiently.

The time complexity is O(n).

DSA Coach Hint:

Think about:

Previous Smaller Element

Next Smaller Element

---

## 13. Undo Operation Using Stack

Design an undo mechanism where every operation can be reversed.

Example:

Type:

A

Type:

B

Type:

C

Undo:

C is removed.

Undo:

B is removed.

A stack can store previous operations.

DSA Coach Hint:

Every new action can be pushed.

Undo means:

POP the most recent action.

---

## 14. Browser Back Button

Simulate the back button of a browser using a stack.

Example:

Visit:

Google

→ YouTube

→ GitHub

Press Back:

GitHub is removed.

Current page:

YouTube

A stack stores previously visited pages.

The time complexity of a basic back operation is O(1).

DSA Coach Hint:

The most recently visited page should be accessed first.

This is LIFO.

---

## 15. Celebrity Problem

Given a group of people, determine whether there is a celebrity.

A celebrity:

- Knows nobody.
- Is known by everybody else.

Example:

People:

A, B, C

If:

A knows B
C knows B
B knows nobody

Then B is the celebrity.

A stack can be used to eliminate people who cannot be celebrities.

DSA Coach Hint:

If A knows B, A cannot be the celebrity.

Use this observation to eliminate candidates.