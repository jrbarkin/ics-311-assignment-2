from avl_tree import AVLDict, Saying

def demo():
    tree = AVLDict()

    # — INSERT five sayings —
    sample = [
        Saying("ʻAʻohe hana nui ke alu ʻia",
               "No task is too big when done together","", ""),
        Saying("Aia i ka ʻōpua ke ola",
               "Life is in the clouds", "",""),
        Saying("E ulu nō ka lālā i ke kumu",
               "The branches grow because of the trunk", "",""),
        Saying("He aliʻi ka ʻāina, he kauwā ke kanaka",
               "The land is chief; the people are its servants", "",""),
        Saying("ʻIke aku, ʻike mai, kōkua aku, kōkua mai; pela ihola ka nohona ʻohana",
               "Recognise others, be recognised, help others, be helped – the family way", "",""),
    ]
    for s in sample:
        tree.insert(s)
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
    print("\nAfter replacement insert:")
    print("New value for key 'Aia i ka ʻōpua ke ola' →", tree[updated.key])

if __name__ == "__main__":
    demo()