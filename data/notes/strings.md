# DSA Coach — Strings

## 1. String Traversal

String traversal means visiting every character of a string one by one.

Example:

"hello"

A traversal visits:

h → e → l → l → o

A single traversal takes O(n) time because every character is visited once.

String traversal is commonly used for:

- Counting characters
- Searching for a character
- Finding vowels and consonants
- Converting characters
- Checking conditions on each character

DSA Coach Hint:

If a problem asks you to inspect every character, first ask:

"Can I solve this using a single traversal?"

---

## 2. Reverse a String

The problem is to reverse the characters of a given string.

Example:

Input:
"hello"

Output:
"olleh"

One simple approach is to traverse the string from the last character to the first.

The time complexity is O(n).

DSA Coach Hint:

When the question asks for the reverse of a string, think about:

- Two pointers
- StringBuilder
- Character array
- Traversing from the end

---

## 3. Check Palindrome

A palindrome is a string that reads the same from both directions.

Example:

"madam"

Reverse:

"madam"

Therefore, the string is a palindrome.

Another example:

"hello"

Reverse:

"olleh"

Therefore, it is not a palindrome.

A two-pointer approach takes O(n) time and O(1) extra space when using a character array.

DSA Coach Hint:

Compare:

first ↔ last
second ↔ second-last

Continue until the pointers meet.

---

## 4. Count Vowels and Consonants

Given a string, count the number of vowels and consonants present in it.

Example:

Input:
"programming"

Vowels:
3

Consonants:
8

The string should be traversed character by character.

For every character, check whether it is:

- a vowel
- a consonant
- a digit
- a space
- a special character

The time complexity is O(n).

DSA Coach Hint:

Do not create unnecessary nested loops.

One traversal is enough.

---

## 5. Count Frequency of Characters

Given a string, find how many times each character occurs.

Example:

Input:

"banana"

Frequency:

b → 1
a → 3
n → 2

A HashMap can be used to store the character and its frequency.

The average time complexity is O(n).

DSA Coach Hint:

Whenever a problem asks:

"How many times does each element occur?"

Think about:

HashMap / frequency array.

---

## 6. Check Anagram

Two strings are called anagrams if they contain the same characters with the same frequencies.

Example:

"listen"

"silent"

Both contain the same characters.

Therefore, they are anagrams.

One approach is to count the frequency of every character in both strings.

The time complexity is O(n).

DSA Coach Hint:

Before checking an anagram, first check:

"Are the lengths equal?"

If lengths are different, they cannot be anagrams.

---

## 7. Remove Duplicate Characters

Given a string, remove duplicate characters while keeping the first occurrence.

Example:

Input:

"programming"

Output:

"progamin"

A HashSet can be used to remember characters that have already appeared.

If the character is not present in the set, add it to the result.

The time complexity is O(n).

DSA Coach Hint:

When the question says:

"Remove duplicates"

think about:

HashSet.

---

## 8. Find First Non-Repeating Character

Given a string, find the first character that appears only once.

Example:

Input:

"swiss"

Frequency:

s → 3
w → 1
i → 1

The first non-repeating character is:

w

A frequency map can be used.

The problem can be solved in O(n) time.

DSA Coach Hint:

Usually use two steps:

1. Count frequencies.
2. Traverse again to find the first character with frequency 1.

---

## 9. Find First Repeating Character

Given a string, find the first character that appears more than once.

Example:

Input:

"programming"

The first repeating character is:

r

A HashSet can be used while traversing the string.

If a character already exists in the set, it is repeating.

The time complexity is O(n).

DSA Coach Hint:

For finding the first duplicate, ask:

"Have I already seen this character?"

---

## 10. Reverse Words in a String

Given a sentence, reverse the order of its words.

Example:

Input:

"DSA is important"

Output:

"important is DSA"

The characters inside each word do not need to be reversed.

Only the order of the words changes.

The time complexity is O(n).

DSA Coach Hint:

First split the sentence into words.

Then process the words from right to left.

---

## 11. Check if String Contains Only Digits

Given a string, determine whether every character is a digit.

Example:

Input:

"123456"

Output:

True

Example:

"123a56"

Output:

False

Traverse the string and check every character.

If any character is not a digit, return false.

The time complexity is O(n).

DSA Coach Hint:

The moment you find an invalid character, you can stop.

This is called early termination.

---

## 12. Find Longest Word in a Sentence

Given a sentence, find the longest word.

Example:

Input:

"DSA makes programming interesting"

Output:

"programming"

The sentence can be split into individual words.

Maintain a variable storing the longest word found so far.

The time complexity is O(n).

DSA Coach Hint:

Maintain:

longestWord

and update it whenever a longer word is found.

---

## 13. String Compression

Compress a string by storing consecutive repeated characters along with their counts.

Example:

Input:

"aaabbc"

Output:

"a3b2c1"

The string should be traversed once.

For every group of identical characters, count how many times it appears.

The time complexity is O(n).

DSA Coach Hint:

Think about:

current character + count

and update the count until the character changes.

---

## 14. Check Rotation of a String

Determine whether one string is a rotation of another string.

Example:

String 1:

"abcd"

String 2:

"cdab"

String 2 is a rotation of String 1.

One common approach is to concatenate the first string with itself:

"abcdabcd"

Then check whether the second string exists inside it.

The time complexity is generally O(n) for suitable substring search algorithms.

DSA Coach Hint:

Before doing complicated logic, think:

s1 + s1

---

## 15. Longest Common Prefix

Given an array of strings, find the longest common prefix shared by all strings.

Example:

Input:

["flower", "flow", "flight"]

Output:

"fl"

All strings begin with:

"fl"

The solution can compare characters position by position.

The time complexity is O(n × m), where n is the number of strings and m is the length of the shortest string.

DSA Coach Hint:

The answer cannot be longer than the shortest string.