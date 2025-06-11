# main.py

# Author: Jaeke Barkin & Michaela Gillan

from avl_tree import AVLDict, Saying
from sayings import index_saying, mehua, withword

def demo():
    tree = AVLDict()

    # — INSERT five sayings —
    sample = [
        Saying("ʻAʻohe hana nui ke alu ʻia",
               "No task is too big when done together by all",
               "ʻAʻohe hana nui ke alu ʻia means if everyone contributes to the task, it lightens the load.",
               "This Hawaiian proverb emphasizes teamwork."),
        Saying("Aia i ka ʻōpua ke ola",
               "Life is in the clouds",
               "Aia i ka ʻōpua ke ola means hope or life lies ahead.",
               "It suggests looking forward with optimism."),
        Saying("E ulu nō ka lālā i ke kumu",
               "The branches grow because of the trunk",
               "E ulu nō ka lālā i ke kumu means success comes from strong foundations.",
               "This reflects the importance of ancestry and guidance."),
        Saying("He aliʻi ka ʻāina, he kauwā ke kanaka",
               "The land is chief; the people are its servants",
               "He aliʻi ka ʻāina, he kauwā ke kanaka means the land is of utmost importance.",
               "It teaches respect for nature."),
        Saying("ʻIke aku, ʻike mai, kōkua aku, kōkua mai; pela ihola ka nohona ʻohana",
               "Recognize others, be recognized, help others, be helped – the family way",
               "This saying outlines the values of Hawaiian family life.",
               "It promotes empathy and support."),
    ]
    for s in sample:
        tree.insert(s)
        index_saying(s)
        print("Inserted:", s.key)

    # — IN-ORDER ITERATION —
    print("\nIn-order iteration (Hawaiian collation):")
    for saying in tree:
        print(" •", saying)

    # — LENGTH —
    print("\nLength            →", len(tree))

    # — MEMBER —
    print("\nMember (present)  →", "Aia i ka ʻōpua ke ola" in tree)
    print("Member (absent)   →", "Kākou kākaʻikahi" in tree)

    # — FIRST / LAST —
    print("\nFirst (min key)   →", tree.first())
    print("Last  (max key)   →", tree.last())

    # — PREDECESSOR / SUCCESSOR —
    mid_key = "E ulu nō ka lālā i ke kumu"
    print(f"\nPredecessor of “{mid_key}” →", tree.predecessor(mid_key))
    print(f"Successor   of “{mid_key}” →", tree.successor(mid_key))

    # — REPLACEMENT INSERT —
    updated = Saying("Aia i ka ʻōpua ke ola", "UPDATED – Life abides in the clouds","","")
    tree.insert(updated)
    index_saying(updated)
    print("\nAfter replacement insert:")
    print("New value for key 'Aia i ka ʻōpua ke ola' →", tree[updated.key])

    # — USER INTERACTION —
    print("\n--- Search Mode ---")
    while True:
        mode = input("\nSearch mode ('mehua' for Hawaiian word, 'withword' for English word, 'quit' to exit): ").strip().lower()
        if mode == 'quit':
            print("Exiting search mode.")
            break
        elif mode == 'mehua':
            word = input("Enter Hawaiian word to search for: ").strip()
            results = mehua(word)
            if results:
                print(f"Found {len(results)} result(s):")
                for r in results:
                    print(" •", r)
            else:
                print("No sayings found with that Hawaiian word.")
        elif mode == 'withword':
            word = input("Enter English word to search for: ").strip()
            results = withword(word)
            if results:
                print(f"Found {len(results)} result(s):")
                for r in results:
                    print(" •", r)
            else:
                print("No sayings found with that English word.")
        else:
            print("Invalid mode. Try 'mehua', 'withword', or 'quit'.")

if __name__ == "__main__":
    demo()
