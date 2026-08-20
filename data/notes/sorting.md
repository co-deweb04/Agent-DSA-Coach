# DSA Coach — Sorting

## 1. Bubble Sort

Sort an array using Bubble Sort.

Example:

[5, 3, 8, 1]

Output:

[1, 3, 5, 8]

Bubble Sort repeatedly compares adjacent elements and swaps them if they are in the wrong order.

The average time complexity is O(n²).

DSA Coach Hint:

After every complete pass, the largest remaining element moves toward the end.

---

## 2. Selection Sort

Sort an array using Selection Sort.

Example:

[64, 25, 12, 22, 11]

Output:

[11, 12, 22, 25, 64]

Find the smallest element from the unsorted portion and place it at the beginning.

The time complexity is O(n²).

DSA Coach Hint:

Think:

Find minimum → Put it at correct position.

---

## 3. Insertion Sort

Sort an array using Insertion Sort.

Example:

[5, 2, 4, 6, 1]

Output:

[1, 2, 4, 5, 6]

Build the sorted portion one element at a time.

The worst-case time complexity is O(n²).

DSA Coach Hint:

Think of arranging playing cards in your hand.

Take one element and insert it into its correct position.

---

## 4. Merge Sort

Sort an array using Merge Sort.

Example:

[38, 27, 43, 3]

Output:

[3, 27, 38, 43]

Merge Sort follows:

Divide → Sort → Merge

The time complexity is O(n log n).

DSA Coach Hint:

Whenever you see:

"Divide the array into halves"

think Merge Sort.

---

## 5. Quick Sort

Sort an array using Quick Sort.

A pivot element is selected and the array is partitioned around the pivot.

Example:

[10, 7, 8, 9, 1, 5]

Output:

[1, 5, 7, 8, 9, 10]

Average time complexity is O(n log n).

DSA Coach Hint:

Think:

Pivot → Partition → Recursively sort both sides.

---

## 6. Sort an Array of 0s, 1s and 2s

Sort an array containing only 0, 1 and 2.

Example:

[2, 0, 2, 1, 1, 0]

Output:

[0, 0, 1, 1, 2, 2]

The Dutch National Flag algorithm can solve this in O(n) time and O(1) space.

DSA Coach Hint:

Maintain three regions:

0 region

1 region

2 region

---

## 7. Sort by Frequency

Sort elements according to their frequency.

Example:

[1, 1, 2, 2, 2, 3]

Output may be:

[2, 2, 2, 1, 1, 3]

First calculate frequencies, then sort according to the required frequency rule.

DSA Coach Hint:

Frequency problems often begin with:

HashMap / frequency array.

---

## 8. Find Kth Smallest Element

Find the Kth smallest element in an array.

Example:

[7, 10, 4, 3, 20, 15]

K = 3

Output:

7

Sorting the array is one simple approach.

After sorting:

[3, 4, 7, 10, 15, 20]

The third element is 7.

DSA Coach Hint:

For large inputs, consider:

Quickselect

instead of completely sorting the array.

---

## 9. Find Kth Largest Element

Find the Kth largest element.

Example:

[3, 2, 1, 5, 6, 4]

K = 2

Output:

5

A min-heap of size K can solve the problem efficiently.

The time complexity is O(n log k).

DSA Coach Hint:

For K largest elements:

Think:

Min Heap of size K.

---

## 10. Merge Overlapping Intervals

Given intervals, merge all overlapping intervals.

Example:

[1,3], [2,6], [8,10]

Output:

[1,6], [8,10]

Sort intervals by starting point first.

Then compare the current interval with the previous merged interval.

The time complexity is O(n log n).

DSA Coach Hint:

Sort first.

Then perform a single traversal.

---

## 11. Sort Strings Alphabetically

Sort a collection of strings in lexicographical order.

Example:

["banana", "apple", "cat"]

Output:

["apple", "banana", "cat"]

A standard sorting algorithm can be used with string comparison.

The time complexity depends on the sorting algorithm and string lengths.

DSA Coach Hint:

Understand how lexicographical comparison works before sorting strings.

---

## 12. Sort Characters by Frequency

Given a string, arrange characters according to their frequency.

Example:

Input:

"tree"

Output:

"eert"

or another valid ordering depending on equal frequencies.

First count character frequencies.

Then sort characters based on frequency.

DSA Coach Hint:

This is a combination of:

Hashing + Sorting.

---

## 13. Sort Nearly Sorted Array

Given an array where every element is at most K positions away from its correct position, sort it efficiently.

Example:

[6, 5, 3, 2, 8, 10, 9]

If K is small, a min-heap can be used.

The time complexity is O(n log k).

DSA Coach Hint:

When an element can only move a small distance, think:

Min Heap.

---

## 14. Count Inversions

Count the number of pairs `(i, j)` such that:

i < j

and

arr[i] > arr[j]

Example:

[2, 4, 1, 3, 5]

Inversions:

(2,1)
(4,1)
(4,3)

Total:

3

Merge Sort can count inversions efficiently.

The time complexity is O(n log n).

DSA Coach Hint:

If you see:

"How many pairs are out of order?"

think:

Merge Sort + Counting.

---

## 15. Sort Array by Parity

Rearrange an array so that even numbers appear before odd numbers.

Example:

[3, 1, 2, 4]

Output:

[2, 4, 3, 1]

The relative ordering may or may not need to be preserved depending on the problem.

A two-pointer approach can solve the basic version in O(n).

DSA Coach Hint:

Use two pointers:

one from the left

one from the right

and move elements into their correct category.