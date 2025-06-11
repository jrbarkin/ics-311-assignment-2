**Authors:**  
Jaeke Barkin, Michaela Gillan

# Overview

For this project, we built a searchable database of Hawaiian proverbs using an AVL tree. An AVL tree is a type of self-balancing binary search tree, which means it automatically keeps its branches balanced as new sayings are added. This helps the program stay fast and efficient when performing operations like inserting new entries, checking if a saying exists, or finding the one that comes before or after another. All of these actions take $\Theta(\log n)$ time, so the performance remains efficient even if the database grows large.

We also took care to sort the sayings according to the Hawaiian alphabet, which includes special characters like the ʻokina (ʻ) and the macron (kahakō, like ā or ē). Regular computer sorting would treat these characters incorrectly, so we created a custom sorting function that follows the correct Hawaiian collation order.

# Demo

Simply run `demo.py` to see the AVL implementation in action.
