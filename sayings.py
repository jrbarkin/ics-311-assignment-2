# sayings.py

# Author: Michaela Gillan

import unicodedata
from collections import defaultdict

# Normalize word to help search operation. Deals with Olelo symbols for sorting/comparing.
def normalize(s):
  return unicodedata.normalize('NFKD',s).lower()

# Define class Saying
class Saying:
    def __init__(self, non_english_words, english_words, explanation_non_english, explanation_english):
        self.non_english_words = non_english_words  # List of Hawaiian (or other language) words
        self.english_words = english_words          # List of English words
        self.explanation_non_english = explanation_non_english
        self.explanation_english = explanation_english

    def __str__(self):
        return f"ʻŌlelo: {' '.join(self.non_english_words)}\nEnglish: {' '.join(self.english_words)}"

# Maps from individual words to lists of Saying objects
non_english_index = defaultdict(list)  # e.g., "hana" -> [s1, s2, ...]
english_index = defaultdict(list)      # e.g., "day" -> [s2, ...]

# Adds a saying to both indices
def index_saying(saying):
    for word in saying.non_english_words:
        normalized = normalize(word)
        non_english_index[normalized].append(saying)

    for word in saying.english_words:
        normalized = word.lower()
        english_index[normalized].append(saying)

# Look up functions 

def mehua(word):
    """Return all sayings that contain the given non-English word."""
    return non_english_index.get(normalize(word), [])


def withword(word):
    """Return all sayings that contain the given English word."""
    return english_index.get(word.lower(), [])
