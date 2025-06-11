# -*- coding: utf-8 -*-
"""avl_tree.py

An ordered dictionary keyed by an ʻōlelo Hawaiʻi proverb (string) implemented
as an AVL. 

The key comparator honours the Hawaiian collation order
ʻ a ā e ē i ī o ō u ū h k l m n p w
so okina (ʻ) sorts before any alpha and kahakō (ā, ē, …) sort
immediately after their short vowel counterparts.

The implementation keeps the tree balanced so that *all* operations above are
Θ(log n) in the worst case.  Rotation proofs follow the textbook treatment in
Goodrich, Tamassia & Goldwasser, sect. 12.3.

Author: Jaeke Barkin
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generator, Iterable, Optional, Tuple, TypeVar, Union


_HAW_ALPHABET = [
    "ʻ",  
    "a", "ā",
    "e", "ē",
    "i", "ī",
    "o", "ō",
    "u", "ū",
    "h", "k", "l", "m", "n", "p", "w",
]

_HAW_ORDER = {c: i for i, c in enumerate(_HAW_ALPHABET)}
_MAX_ORDER = len(_HAW_ALPHABET)

def _hawaiian_key(string: str):
    """Return a tuple usable as a sort key under Hawaiian alphabetical order."""
    return tuple(_HAW_ORDER.get(ch.lower(), _MAX_ORDER) for ch in string)


def _hawaiian_compare(a: str, b: str):
    """Like (a > b) – (a < b) following Hawaiian collation."""
    ka, kb = _hawaiian_key(a), _hawaiian_key(b)
    return (ka > kb) - (ka < kb)


@dataclass(slots=True, frozen=True)
class Saying:
    """Container for a single ʻōlelo noʻeau entry."""
    olelo_haw: str                 # canonical Hawaiian text (key)
    translation_en: str            # English translation
    explanation_haw: str           # optional… may be empty
    explanation_en: str

    @property
    def key(self):  # alias for clarity
        return self.olelo_haw

    def __str__(self):  
        return f"{self.olelo_haw} — {self.translation_en}"



S = TypeVar("S", bound="Saying")
Comparator = Callable[[str, str], int]


class _AVLNode:
    __slots__ = ("key", "value", "left", "right", "height")

    def __init__(self, key: str, value: Saying):
        self.key: str = key
        self.value: Saying = value
        self.left: Optional[_AVLNode] = None
        self.right: Optional[_AVLNode] = None
        self.height: int = 1  # leaf ≡ height 1

    def _update_height(self):
        lh = self.left.height if self.left else 0
        rh = self.right.height if self.right else 0
        self.height = max(lh, rh) + 1

    def _balance_factor(self):
        return (self.left.height if self.left else 0) - (
            self.right.height if self.right else 0
        )


class AVLDict:

    def __init__(self, comparator: Comparator | None = None):
        self._root: Optional[_AVLNode] = None
        self._size: int = 0
        # Default comparator is Hawaiian alphabetical order.
        self._cmp: Comparator = comparator or _hawaiian_compare

    def __len__(self):
        return self._size

    def __contains__(self, key: str):  # Member()
        return self._find_node(key) is not None

    def __getitem__(self, key: str):
        node = self._find_node(key)
        if node is None:
            raise KeyError(key)
        return node.value
    
    def insert(self, value: Saying):  # Insert()
        """Insert or replace *value* keyed by its olelo_haw string."""
        def _insert(node: Optional[_AVLNode], key: str, val: Saying) -> _AVLNode:
            if node is None:
                self._size += 1
                return _AVLNode(key, val)
            c = self._cmp(key, node.key)
            if c < 0:
                node.left = _insert(node.left, key, val)
            elif c > 0:
                node.right = _insert(node.right, key, val)
            else:  # replace existing
                node.value = val  # type: ignore[attr-defined]
                return node
            return self._rebalance(node)

        self._root = _insert(self._root, value.key, value)


    def first(self):  # First()
        node = self._min_node(self._root)
        return node.value if node else None

    def last(self):  # Last()
        node = self._max_node(self._root)
        return node.value if node else None

    def predecessor(self, key: str):  # Predecessor()
        pred = None
        node = self._root
        while node:
            c = self._cmp(key, node.key)
            if c <= 0:
                node = node.left
            else:
                pred = node
                node = node.right
        return pred.value if pred else None

    def successor(self, key: str):  # Successor()
        succ = None
        node = self._root
        while node:
            c = self._cmp(key, node.key)
            if c < 0:
                succ = node
                node = node.left
            else:
                node = node.right
        return succ.value if succ else None

    def __iter__(self):
        yield from self._inorder(self._root)

    def keys(self):
        for saying in self:
            yield saying.key

    def values(self):
        yield from self

    def _find_node(self, key: str):
        node = self._root
        while node:
            c = self._cmp(key, node.key)
            if c == 0:
                return node
            node = node.left if c < 0 else node.right
        return None

    @staticmethod
    def _inorder(node):
        if node is not None:
            yield from AVLDict._inorder(node.left)
            yield node.value
            yield from AVLDict._inorder(node.right)

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

    def _rebalance(self, node: _AVLNode):
        node._update_height()
        balance = node._balance_factor()
        if balance > 1:
            # left heavy
            if node.left and node.left._balance_factor() < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1:
            # right heavy
            if node.right and node.right._balance_factor() > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    @staticmethod
    def _rotate_left(z: _AVLNode):
        y = z.right
        if y is None:
            return z  # should not happen
        T2 = y.left
        # perform rotation
        y.left = z
        z.right = T2
        # update heights
        z._update_height()
        y._update_height()
        return y

    @staticmethod
    def _rotate_right(z: _AVLNode):
        y = z.left
        if y is None:
            return z
        T3 = y.right
        # perform rotation
        y.right = z
        z.left = T3
        # update heights
        z._update_height()
        y._update_height()
        return y


if __name__ == "__main__":
    sayings = AVLDict()

    sayings.insert(Saying("ʻAʻohe hana nui ke alu ʻia", "No task is too big when done together", "…", "…"))
    sayings.insert(Saying("Aia i ka ʻōpua ke ola", "Life is in the clouds", "…", "…"))
    sayings.insert(Saying("E ulu nō ka lālā i ke kumu", "The branches grow because of the trunk", "…", "…"))

    print("First:", sayings.first())
    print("Last :", sayings.last())

    for s in sayings:
        print(" ·", s)
