# DSA Coach — Searching

## 1. Linear Search

Find a target element in an array by checking elements one by one.

Example:

Array:

[10, 20, 30, 40]

Target:

30

Output:

Element found at index 2.

The time complexity is O(n).

DSA Coach Hint:

Use linear search when:

- The array is unsorted.
- The input is small.
- Simplicity is more important than optimization.

---

## 2. Find First Occurrence

Find the first occurrence of a target element in an array.

Example:

[10, 20, 30, 20, 40]

Target:

20

Output:

Index 1

Traverse from left to right and return immediately when the target is found.

The time complexity is O(n).

DSA Coach Hint:

Do not continue searching after finding the first occurrence.

---

## 3. Find Last Occurrence

Find the last occurrence of a target element.

Example:

[10, 20, 30, 20, 40]

Target:

20

Output:

Index 3

Traverse the complete array and update the answer whenever the target appears.

The time complexity is O(n).

DSA Coach Hint:

Unlike first occurrence, you must continue searching until the end.

---

## 4. Count Occurrences

Count how many times a target value occurs in an array.

Example:

[2, 4, 2, 6, 2]

Target:

2

Output:

3

Traverse the array and increase a counter whenever the target is found.

The time complexity is O(n).

DSA Coach Hint:

Think:

if arr[i] == target

then:

count++

---

## 5. Binary Search

Search for an element in a sorted array using binary search.

Example:

[10, 20, 30, 40, 50]

Target:

40

Binary search repeatedly divides the search range into two halves.

The time complexity is O(log n).

DSA Coach Hint:

Binary search requires a sorted search space.

---

## 6. Find First Occurrence Using Binary Search

Find the first occurrence of a target in a sorted array containing duplicates.

Example:

[10, 20, 20, 20, 30]

Target:

20

Output:

Index 1

When the target is found, continue searching toward the left.

The time complexity is O(log n).

DSA Coach Hint:

Found target?

Do not stop immediately.

Move:

right = mid - 1

---

## 7. Find Last Occurrence Using Binary Search

Find the last occurrence of a target in a sorted array.

Example:

[10, 20, 20, 20, 30]

Target:

20

Output:

Index 3

When the target is found, continue searching toward the right.

The time complexity is O(log n).

DSA Coach Hint:

Found target?

Try:

left = mid + 1

---

## 8. Search Insert Position

Given a sorted array, find the index where a target should be inserted.

Example:

[1, 3, 5, 6]

Target:

5

Output:

2

Target:

2

Output:

1

Binary search can solve this problem in O(log n).

DSA Coach Hint:

If target is not found, the final left pointer usually represents the insertion position.

---

## 9. Find Square Root

Find the integer square root of a non-negative number.

Example:

Input:

16

Output:

4

Input:

20

Output:

4

Binary search can be performed over the range:

0 to n

The time complexity is O(log n).

DSA Coach Hint:

Instead of calculating every number, ask:

"Can I binary search the answer?"

---

## 10. Search in Rotated Sorted Array

Search for an element in a sorted array that has been rotated.

Example:

[4, 5, 6, 7, 0, 1, 2]

Target:

0

Output:

Index 4

At least one half of the array will always remain sorted.

The time complexity is O(log n).

DSA Coach Hint:

At every step determine:

Which half is sorted?

Then decide where the target can exist.

---

## 11. Find Peak Element

Find an element that is greater than its neighboring elements.

Example:

[1, 2, 3, 1]

Peak:

3

A binary-search-based approach can find a peak efficiently.

The time complexity is O(log n).

DSA Coach Hint:

Compare:

arr[mid]

with:

arr[mid + 1]

Use the slope to decide which direction to move.

---

## 12. Find Minimum in Rotated Sorted Array

Find the minimum element in a rotated sorted array.

Example:

[4, 5, 6, 7, 0, 1, 2]

Output:

0

Binary search can identify the point where the rotation occurred.

The time complexity is O(log n).

DSA Coach Hint:

Compare the middle element with the rightmost element.

---

## 13. Find Missing Number

Given numbers from 0 to n with one number missing, find the missing number.

Example:

[3, 0, 1]

Output:

2

A mathematical, XOR, or binary-search approach can be considered depending on the input properties.

The XOR approach takes O(n) time and O(1) space.

DSA Coach Hint:

Ask:

"Can I exploit the expected range of values?"

---

## 14. Find Majority Element

Find the element that occurs more than n/2 times.

Example:

[2, 2, 1, 1, 1, 2, 2]

Output:

2

The Boyer-Moore Voting Algorithm can solve this in O(n) time and O(1) space.

DSA Coach Hint:

When one element dominates the array, think about:

Candidate + Count

---

## 15. Search in 2D Matrix

Search for a target value in a sorted matrix.

Example:

[
[1,  4,  7],
[10, 11, 16],
[20, 30, 40]
]

Target:

16

Output:

Found

Depending on the matrix properties, binary search can be applied row-wise or to the entire matrix.

DSA Coach Hint:

First understand exactly how the matrix is sorted before choosing the search strategy.