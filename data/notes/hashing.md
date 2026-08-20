# DSA Coach — Hashing

## 1. Frequency of Elements

Count the frequency of every element in an array.

Example:

[1, 2, 2, 3, 1, 1]

Output:

1 → 3
2 → 2
3 → 1

A HashMap can store:

element → frequency

The average time complexity is O(n).

DSA Coach Hint:

Whenever the problem asks:

"How many times does something occur?"

Think HashMap.

---

## 2. Find Duplicate Elements

Find all elements that appear more than once.

Example:

[1, 2, 3, 2, 4, 1]

Output:

1, 2

A HashSet can keep track of previously seen elements.

The average time complexity is O(n).

DSA Coach Hint:

Ask:

"Have I already seen this element?"

---

## 3. Find First Repeating Element

Find the first element that appears more than once.

Example:

[10, 5, 3, 4, 3, 5]

Output:

3

A HashSet can be used while traversing the array.

DSA Coach Hint:

Traverse from left to right and stop when an element is already present in the set.

---

## 4. Find First Non-Repeating Element

Find the first element whose frequency is exactly one.

Example:

[4, 5, 1, 2, 0, 4]

Output:

5

First calculate frequencies.

Then traverse again to find the first element with frequency 1.

The time complexity is O(n).

DSA Coach Hint:

Two passes are often easier than trying to solve everything in one pass.

---

## 5. Two Sum

Find two elements whose sum equals a target.

Example:

Array:

[2, 7, 11, 15]

Target:

9

Output:

[0, 1]

A HashMap can store previously seen values.

For every element, check whether:

target - current

already exists.

The average time complexity is O(n).

DSA Coach Hint:

Think:

"Do I already have the complement?"

---

## 6. Intersection of Two Arrays

Find the common elements between two arrays.

Example:

A:

[1, 2, 2, 3]

B:

[2, 2, 4]

Intersection:

[2]

A HashSet can be used for membership checking.

DSA Coach Hint:

HashSet is useful when the question is:

"Does this element exist?"

---

## 7. Union of Two Arrays

Find the unique elements present in either of two arrays.

Example:

A:

[1, 2, 3]

B:

[2, 3, 4]

Union:

[1, 2, 3, 4]

A HashSet can automatically remove duplicates.

The average time complexity is O(n + m).

---

## 8. Longest Consecutive Sequence

Find the length of the longest sequence of consecutive integers.

Example:

[100, 4, 200, 1, 3, 2]

Sequence:

1, 2, 3, 4

Output:

4

A HashSet allows O(1) average membership checks.

The overall time complexity is O(n) on average.

DSA Coach Hint:

Only start a sequence when:

number - 1

does not exist.

---

## 9. Subarray with Given Sum

Find whether an array contains a subarray whose sum equals a target.

Example:

[1, 2, 3, 7, 5]

Target:

12

Subarray:

[3, 7, 2]

depending on the input; alternatively identify a valid exact subarray based on the given array.

Prefix sums combined with hashing can solve the general problem efficiently.

DSA Coach Hint:

Think:

Current Prefix Sum - Target

If this value has appeared before, a valid subarray exists.

---

## 10. Count Subarrays with Given Sum

Count the number of subarrays whose sum equals K.

Example:

[1, 1, 1]

K = 2

Output:

2

Valid subarrays:

[1,1] at positions 0-1

[1,1] at positions 1-2

Prefix sum + HashMap can solve this in O(n).

DSA Coach Hint:

Store:

prefixSum → frequency

---

## 11. Group Anagrams

Group strings that are anagrams of each other.

Example:

["eat", "tea", "tan", "ate", "nat", "bat"]

Output groups:

["eat","tea","ate"]

["tan","nat"]

["bat"]

A sorted string or character-frequency representation can be used as the HashMap key.

DSA Coach Hint:

Anagrams should produce the same key.

---

## 12. Isomorphic Strings

Determine whether two strings are isomorphic.

Example:

"egg"

"add"

Output:

True

Each character from the first string must consistently map to one character in the second string.

HashMaps can store character mappings.

DSA Coach Hint:

Mapping must work in both directions.

---

## 13. Longest Substring Without Repeating Characters

Find the length of the longest substring without duplicate characters.

Example:

Input:

"abcabcbb"

Output:

3

Longest substring:

"abc"

A HashSet or HashMap with a sliding window can solve this efficiently.

The time complexity is O(n).

DSA Coach Hint:

When duplicates appear, move the left side of the window.

Think:

Hashing + Sliding Window.

---

## 14. Find Common Elements with Frequencies

Given two arrays, find common elements while considering their frequencies.

Example:

A:

[1, 2, 2, 3]

B:

[2, 2, 2, 4]

Output:

[2, 2]

Store the frequency of elements from one array.

Then process the second array.

DSA Coach Hint:

This is different from simple intersection because duplicates matter.

---

## 15. Detect Duplicate Within K Distance

Determine whether the same element occurs within K positions of itself.

Example:

[1, 2, 3, 1]

K = 3

Output:

True

The two occurrences of 1 are within the allowed distance.

A HashMap can store the most recent index of each element.

DSA Coach Hint:

Store:

element → latest index

Then calculate:

currentIndex - previousIndex