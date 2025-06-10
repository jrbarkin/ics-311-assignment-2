# -*- coding: utf-8 -*-
"""

Author: Jaeke Barkin

A base class for an AVL self‑balancing binary‑search tree.


Public interface:

    tree = AVLTree()
    tree.insert(key, value)      # add or replace
    tree.member(key)  -> bool    # existence test
    tree.first()     -> value | None
    tree.last()      -> value | None
    tree.predecessor(key) -> value | None
    tree.successor(key)   -> value | None

Iteration (`for k, v in tree:`) yields *(key, value)* pairs in ascending order.

"""

class _Node:
    __slots__ = ("key", "value", "left", "right", "height")

    def __init__(self, key, value):
        self.key   = key
        self.value = value
        self.left  = None  
        self.right = None  
        self.height = 1    


class AVLTree:
    """Self‑balancing binary‑search tree"""

    def __init__(self):
        self._root = None
        self._size = 0
        

    def __len__(self):
        return self._size

    def __iter__(self):
        stack = []
        node = self._root
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                yield (node.key, node.value)
                node = node.right



    def insert(self, key, value):
        """Insert (*key*, *value*) with AVL re‑balancing (replace if duplicate)."""
        self._root = self._insert(self._root, key, value)

    def member(self, key):
        return self._find(self._root, key) is not None

    def first(self):
        node = self._min_node(self._root)
        return None if node is None else node.value

    def last(self):
        node = self._max_node(self._root)
        return None if node is None else node.value

    def _compare(self, a, b):
        return (a > b) - (a < b)  

    def _find(self, node, key):
        while node:
            cmp = self._compare(key, node.key)
            if cmp == 0:
                return node
            node = node.left if cmp < 0 else node.right
        return None

    def _insert(self, node, key, value):
        if node is None:
            self._size += 1
            return _Node(key, value)

        cmp = self._compare(key, node.key)
        if cmp < 0:
            node.left  = self._insert(node.left,  key, value)
        elif cmp > 0:
            node.right = self._insert(node.right, key, value)
        else:  # replace existing
            node.value = value
            return node

        # update height and rebalance
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._balance_factor(node)

        # Left‑Left / Left‑Right cases
        if balance > 1:
            if self._compare(key, node.left.key) > 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right‑Right / Right‑Left cases
        if balance < -1:
            if self._compare(key, node.right.key) < 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _rotate_left(self, z):
        y  = z.right
        t2 = y.left
        y.left  = z
        z.right = t2
        # update heights
        z.height = 1 + max(self._height(z.left),  self._height(z.right))
        y.height = 1 + max(self._height(y.left),  self._height(y.right))
        return y

    def _rotate_right(self, z):
        y  = z.left
        t3 = y.right
        y.right = z
        z.left  = t3
        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), y._height if hasattr(y, "_height") else self._height(y.right))
        return y

    @staticmethod
    def _height(node):
        return 0 if node is None else node.height

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    @staticmethod
    def _min_node(node):
        if node is None:
            return None
        while node.left:
            node = node.left
        return node

    @staticmethod
    def _max_node(node):
        if node is None:
            return None
        while node.right:
            node = node.right
        return node

if __name__ == "__main__":
    t = AVLTree()
    for k, v in ((30, "A"), (20, "B"), (40, "C"), (10, "D"), (25, "E")):
        t.insert(k, v)

    print("in‑order:")
    for k, v in t:
        print(k, v)

    print("min →", t.first())
    print("max →", t.last())

