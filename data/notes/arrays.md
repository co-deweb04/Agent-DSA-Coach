# DSA Coach — Arrays

## 1.Array Fundamentals

An array is a linear data structure that stores elements in a sequence. Each element can be accessed using an index.

Example:

[10, 20, 30, 40, 50]

The indices are:

0 → 10
1 → 20
2 → 30
3 → 40
4 → 50

Arrays usually provide O(1) random access using an index.

Important array operations include:

- Access
- Search
- Insertion
- Deletion
- Traversal

Accessing an element by index usually takes O(1).

Searching an unsorted array usually takes O(n).

Insertion or deletion in the middle of an array can take O(n) because elements may need to be shifted.

## 2. Array Traversal

Traversal means visiting each element of an array.

Example:

[4, 7, 2, 9]

A traversal visits:

4 → 7 → 2 → 9

A single traversal takes O(n) time because every element is visited once.

Traversal is commonly used for:

- Finding maximum
- Finding minimum
- Calculating sum
- Counting elements
- Searching
- Updating elements

DSA Coach Hint:

If a problem asks you to inspect every element, first ask:

"Can I solve this using a single traversal?"

## 3. Finding Maximum and Minimum

To find the maximum element in an unsorted array:

1. Assume the first element is the maximum.
2. Traverse the remaining elements.
3. Compare every element with the current maximum.
4. Update the maximum when a larger value is found.

Example:

[3, 7, 2, 9, 4]

Start:

maximum = 3

After checking 7:

maximum = 7

After checking 2:

maximum = 7

After checking 9:

maximum = 9

After checking 4:

maximum = 9

Time Complexity: O(n)

Space Complexity: O(1)

DSA Coach Hint:

If you need the largest or smallest element, ask:

"Can I maintain the best answer seen so far while scanning the array?"

## 4. Linear Search

Linear search checks elements one by one until the target is found.

Example:

Array:

[4, 8, 1, 6, 9]

Target:

6

Search:

4 → not found

8 → not found

1 → not found

6 → found

Best Case: O(1)

Worst Case: O(n)

Space Complexity: O(1)

Linear search is useful when the array is unsorted.

DSA Coach Hint:

Before using a complicated algorithm, ask:

"Is the array sorted?"

If it is not sorted, a simple linear scan may be sufficient.

## 5. Two Pointer Technique

The two-pointer technique uses two indices to process an array efficiently.

A common form uses:

left pointer

right pointer

Example:

[1, 2, 3, 4, 5]

left = 0

right = 4

The pointers can move toward each other.

Two pointers are commonly useful when:

- The array is sorted.
- The problem asks about pairs.
- Elements from both ends need to be compared.
- The array needs to be reversed.
- Duplicates need to be removed.
- The array needs to be partitioned.

Example:

Find two numbers whose sum equals a target.

Array:

[1, 2, 4, 7, 11]

Target:

9

Start with:

left = 0

right = 4

1 + 11 = 12

The sum is too large, so move the right pointer.

1 + 7 = 8

The sum is too small, so move the left pointer.

2 + 7 = 9

The target is found.

Time Complexity: O(n)

Space Complexity: O(1)

DSA Coach Hint:

If the array is sorted and the problem asks about a pair, ask:

"Can I start from both ends and move the pointers based on the current result?"

## 6. Sliding Window

Sliding Window is useful for problems involving contiguous subarrays or consecutive elements.

Instead of recalculating the entire range repeatedly, maintain information about the current window.

Example:

[2, 1, 5, 1, 3, 2]

Find the maximum sum of a subarray of size 3.

First window:

2 + 1 + 5 = 8

Move the window.

Remove 2.

Add 1.

New window:

1 + 5 + 1 = 7

Continue moving the window.

The main idea is to reuse information from the previous window.

Sliding Window is commonly useful for:

- Maximum sum of k consecutive elements
- Minimum sum subarray
- Longest valid subarray
- Shortest valid subarray
- Contiguous range problems

There are two common types:

Fixed-size window:

The window size remains constant.

Variable-size window:

The window expands or contracts depending on a condition.

DSA Coach Hint:

If you see words such as:

"contiguous"

"consecutive"

"subarray"

"window of size k"

ask:

"Can I maintain a moving window instead of checking every possible subarray?"

## 7. Prefix Sum

Prefix Sum is used to efficiently calculate sums of ranges.

Example:

Original array:

[2, 4, 6, 8, 10]

Prefix sum:

[2, 6, 12, 20, 30]

The prefix sum at index i represents the sum from index 0 through index i.

For a range from l to r:

range_sum = prefix[r] - prefix[l - 1]

when l > 0.

If l = 0:

range_sum = prefix[r]

Building a prefix sum takes O(n).

Each range sum query can then be answered in O(1).

DSA Coach Hint:

If a problem asks many times:

"Find the sum from index l to r"

think:

"Can I precompute cumulative information?"

## 8. Hashing with Arrays

Hashing can be combined with arrays to make lookup operations faster.

Example:

Find whether an array contains duplicates.

Array:

[1, 2, 3, 1]

Maintain a set of values already seen.

Process:

1 → add

2 → add

3 → add

1 → already exists

Therefore, a duplicate exists.

Average Time Complexity: O(n)

Space Complexity: O(n)

Hashing is commonly useful for:

- Finding duplicates
- Two Sum
- Frequency counting
- Checking whether a value exists
- Finding repeated values

DSA Coach Hint:

If you repeatedly need to ask:

"Have I seen this value before?"

think about using a HashSet or HashMap.

## 9. Frequency Counting

Frequency counting stores how many times each value occurs.

Example:

[1, 2, 2, 3, 3, 3]

Frequency:

1 → 1

2 → 2

3 → 3

A HashMap or dictionary can be used.

Frequency counting is useful for:

- Finding duplicates
- Finding the most frequent element
- Counting occurrences
- Majority element
- Checking anagrams

DSA Coach Hint:

If a problem repeatedly asks:

"How many times does this value occur?"

think:

"Can I build a frequency map first?"

## 10. Kadane's Algorithm

Kadane's Algorithm is used to find the maximum sum of a contiguous subarray.

Example:

[-2, 1, -3, 4, -1, 2, 1, -5, 4]

The maximum-sum contiguous subarray is:

[4, -1, 2, 1]

Its sum is:

6

The key idea is to decide at every position whether to:

1. Continue the current subarray.

or

2. Start a new subarray from the current element.

Maintain:

current_sum

best_sum

At each element:

current_sum = max(element, current_sum + element)

best_sum = max(best_sum, current_sum)

Time Complexity: O(n)

Space Complexity: O(1)

DSA Coach Hint:

If the problem asks for the maximum sum of a contiguous subarray, ask:

"At each element, should I continue the current subarray or start a new one?"

## 11. Binary Search

Binary Search is useful when the search space is ordered.

Example:

[1, 3, 5, 7, 9, 11]

Target:

7

Check the middle element.

Instead of checking every element, eliminate half of the search space after each comparison.

Time Complexity: O(log n)

Space Complexity: O(1) for an iterative implementation.

Binary Search is commonly used for:

- Searching a sorted array
- Finding first occurrence
- Finding last occurrence
- Finding lower bound
- Finding upper bound
- Searching for a minimum valid value
- Searching for a maximum valid value
- Binary search on answer

DSA Coach Hint:

Whenever you see a sorted array, ask:

"Can I eliminate half of the search space?"

## 12. Sorting as a Preprocessing Technique

Sorting can simplify many array problems.

Example:

Original:

[7, 2, 9, 1, 5]

Sorted:

[1, 2, 5, 7, 9]

Sorting can help with:

- Two pointer problems
- Duplicate detection
- Interval problems
- Greedy algorithms
- Finding closest values
- Grouping similar values

Comparison-based sorting generally takes O(n log n).

Important:

Sorting can change the original order.

Before sorting, ask:

"Does the problem require the original indices or original order?"

If yes, sorting may require additional information.

## 13. In-Place Array Operations

An in-place algorithm modifies the input array directly instead of creating another large array.

Example:

Reverse an array.

Use two pointers:

left

right

Swap the elements at left and right.

Then move both pointers toward the center.

Time Complexity: O(n)

Space Complexity: O(1)

DSA Coach Hint:

If the problem says:

"Do it in-place"

ask:

"Can I modify the original array instead of creating another array?"

## 14. Reverse an Array

Example:

[1, 2, 3, 4, 5]

Use:

left = 0

right = n - 1

Swap:

1 and 5

Then:

2 and 4

Final array:

[5, 4, 3, 2, 1]

Time Complexity: O(n)

Space Complexity: O(1)

This is a common application of the two-pointer technique.

## 15. Removing Duplicates from a Sorted Array

When an array is sorted, duplicate values are adjacent.

Example:

[1, 1, 2, 2, 3]

A slow pointer can track the position where the next unique element should be placed.

A fast pointer scans the array.

The slow pointer represents the position of the latest unique element.

The fast pointer searches for the next unique element.

DSA Coach Hint:

If an array is sorted and the problem asks you to remove duplicates, think:

"Duplicates are next to each other. Can I use a slow pointer to overwrite duplicates?"

## 16. Move Zeroes

Example:

[0, 1, 0, 3, 12]

Goal:

[1, 3, 12, 0, 0]

A common approach is to maintain a position where the next non-zero element should be placed.

Traverse the array.

Whenever a non-zero value is found, place it at the insertion position.

Then increment the insertion position.

Finally, fill the remaining positions with zero.

Pattern:

Two Pointers

In-place Array Manipulation

DSA Coach Hint:

Separate the problem into two goals:

1. Move all useful elements toward the front.
2. Put the remaining zeroes at the end.

## 17. Best Time to Buy and Sell Stock

Given stock prices, find the maximum profit from buying and selling once.

Example:

[7, 1, 5, 3, 6, 4]

Buy at:

1

Sell at:

6

Profit:

5

The key idea is to maintain the minimum price seen so far.

For every current price:

profit = current_price - minimum_price

Update the maximum profit.

Time Complexity: O(n)

Space Complexity: O(1)

DSA Coach Hint:

Instead of checking every possible buy and sell pair, ask:

"What is the cheapest price I have seen before today?"

## 18. Product of Array Except Self

Example:

Input:

[1, 2, 3, 4]

Output:

[24, 12, 8, 6]

For every position, calculate the product of all elements except the current element.

A brute-force approach repeatedly multiplies all other elements.

That approach takes O(n²).

A better approach uses prefix and suffix products.

For every index:

answer[i] =
product of elements to the left
multiplied by
product of elements to the right

Time Complexity: O(n)

Space Complexity: O(1) extra space if the output array is not counted.

DSA Coach Hint:

For every index, ask:

"What is the product of everything before this index?"

and:

"What is the product of everything after this index?"

## 19. Subarrays

A subarray is a contiguous portion of an array.

For:

[1, 2, 3]

Subarrays include:

[1]

[2]

[3]

[1, 2]

[2, 3]

[1, 2, 3]

The key property is:

A subarray must be contiguous.

Subarray and subsequence are different.

A subsequence does not have to be contiguous.

Example:

[1, 3]

is a subsequence of:

[1, 2, 3]

but it is not a subarray.

DSA Coach Hint:

If the problem uses words such as:

"contiguous"

"consecutive"

"subarray"

think about:

- Sliding Window
- Prefix Sum
- Kadane's Algorithm
- Two Pointers

## 20. Array Problem-Solving Workflow

When solving an array problem, follow this process.

Step 1:

Understand the problem.

Step 2:

Identify the input and output.

Step 3:

Look at the constraints.

Step 4:

Try a brute-force approach.

Step 5:

Identify the bottleneck.

Step 6:

Look for a pattern.

Possible patterns include:

- Hashing
- Two Pointers
- Sliding Window
- Prefix Sum
- Binary Search
- Sorting
- Greedy
- Dynamic Programming

Step 7:

Determine the required data structure.

Step 8:

Write the algorithm in plain English.

Step 9:

Analyze time and space complexity.

Step 10:

Test edge cases.

Step 11:

Write the code.

## 21. Common Array Mistakes

Common mistakes include:

1. Off-by-one errors.

2. Accessing arr[n] when the last valid index is n - 1.

3. Forgetting empty arrays.

4. Forgetting single-element arrays.

5. Accidentally modifying the original array.

6. Using O(n²) when O(n) is possible.

7. Confusing a subarray with a subsequence.

8. Ignoring integer overflow in languages where integer size matters.

9. Not checking the input constraints.

10. Forgetting duplicate values.

## 22. Array Pattern Recognition

When you receive an array problem, ask the following questions.

Question 1:

Is the array sorted?

If yes, think about:

- Binary Search
- Two Pointers

Question 2:

Does the problem involve a contiguous range?

If yes, think about:

- Sliding Window
- Prefix Sum
- Kadane's Algorithm

Question 3:

Do I need to quickly determine whether I have seen a value?

If yes, think about:

- HashSet
- HashMap

Question 4:

Do I need to find a pair?

Think about:

- Hashing
- Two Pointers

Question 5:

Can I eliminate half of the search space?

If yes, think about:

- Binary Search

Question 6:

Does the problem ask for a maximum sum contiguous subarray?

Think about:

- Kadane's Algorithm

## 23. Brute Force vs Optimized Solution

A good DSA problem-solving process starts with brute force.

Example:

Two Sum.

Brute Force:

Check every possible pair.

Time Complexity:

O(n²)

Optimized:

Use a HashMap.

Average Time Complexity:

O(n)

The optimization comes from avoiding repeated searching.

DSA Coach Strategy:

First ask:

"What is the simplest solution I can think of?"

Then ask:

"What part of this solution is repeated or expensive?"

Then ask:

"Can another data structure or algorithm remove that repeated work?"

## 24. Array Edge Cases

Always consider:

Empty array:

[]

Single element:

[5]

All elements equal:

[3, 3, 3, 3]

Already sorted:

[1, 2, 3, 4, 5]

Reverse sorted:

[5, 4, 3, 2, 1]

Negative numbers:

[-5, -2, -10, -1]

Duplicate values:

[1, 2, 2, 3, 3]

Very large values.

Very large input size.

## 25. DSA Coach Hint Philosophy

The goal of DSA Coach is not to immediately reveal the solution.

Hints should progressively reduce the search space.

### Hint Level 1 — Conceptual

Give a question that points toward the relevant concept.

Example:

"Can you think of a data structure that lets you quickly check whether you have seen a value before?"

Do not immediately reveal the exact data structure.

### Hint Level 2 — Pattern

Reveal the general technique.

Example:

"Try keeping track of previously seen values while traversing the array."

### Hint Level 3 — Algorithm

Explain the workflow.

Example:

"For every element, calculate the value needed to reach the target. Check whether that value has already been seen."

### Hint Level 4 — Pseudocode

Provide the algorithm structure.

Example:

1. Create an empty map.
2. Traverse the array.
3. Calculate the complement.
4. Check the map.
5. Store the current value.
6. Return the answer when found.

### Hint Level 5 — Full Solution

Only provide the complete solution when the user asks for it or has exhausted the hints.

The complete solution should contain:

- Algorithm
- Code
- Explanation
- Time Complexity
- Space Complexity
- Edge Cases

## 26. Important Array Patterns

The major patterns to recognize are:

1. Simple Traversal
2. Hashing
3. Two Pointers
4. Sliding Window
5. Prefix Sum
6. Binary Search
7. Sorting
8. Kadane's Algorithm
9. Prefix/Suffix Techniques
10. In-place Manipulation

The most important skill is recognizing the pattern from the problem statement rather than memorizing solutions.
