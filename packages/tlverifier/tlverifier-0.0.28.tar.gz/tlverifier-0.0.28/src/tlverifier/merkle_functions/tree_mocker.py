from pymerkle_logsTransparentes import MerkleTree


def make_tree(list_of_data):
    m_tree = MerkleTree()
    for data in list_of_data:
        m_tree.append_entry(data)
    return m_tree


def make_all_trees():
    tree_1 = make_tree([b'leaf11', b'leaf12', b'leaf13', b'leaf14'])
    tree_2 = make_tree([b'leaf21', b'leaf22', b'leaf23'])
    tree_3 = make_tree([b'leaf31', b'leaf32'])
    tree_g = make_tree([tree_1.root, tree_2.root, tree_3.root])

    return tree_1, tree_2, tree_3, tree_g


if __name__ == '__main__':
    t1, t2, t3, tg = make_all_trees()
    proof = tg.prove_inclusion(t1.root)
    print(t1.root)
