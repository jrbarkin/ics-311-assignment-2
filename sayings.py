# sayings.py

# Author: Michaela Gillan

import unicodedata
from collections import defaultdict
from avl_tree import Saying 

# Normalize word to help search operation. Deals with Olelo symbols for sorting/comparing.
def normalize(s):
  return unicodedata.normalize('NFKD',s).lower()

# Index dictionaries
non_english_index = defaultdict(list)  # e.g., "hana" -> [s1, s2, ...]
english_index = defaultdict(list)      # e.g., "life" -> [s1, s3, ...]

def index_saying(saying: Saying):
    """
    Indexes a Saying object by its words in both the olelo_haw and translation_en.
    """
    # Index Hawaiian words
    for word in saying.olelo_haw.split():
        normalized = normalize(word)
        non_english_index[normalized].append(saying)

    # Index English translation words
    for word in saying.translation_en.split():
        normalized = word.lower()
        english_index[normalized].append(saying)

def mehua(word):
    """Return all sayings that contain the given Hawaiian word."""
    return non_english_index.get(normalize(word), [])

def withword(word):
    """Return all sayings that contain the given English word."""
    return english_index.get(word.lower(), [])

def withword(word):
    """Return all sayings that contain the given English word."""
    return english_index.get(word.lower(), [])
