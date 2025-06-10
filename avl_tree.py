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
        self.left  = None   # type: _Node | None
        self.right = None   # type: _Node | None
        self.height = 1     # leaf height = 1