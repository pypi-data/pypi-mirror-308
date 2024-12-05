import json
import random

import pkg_resources    # use in package

from pymerkle_logsTransparentes import MerkleProof


def get_dummie_proof():
    file_path = _get_dummie_file_path("t1_proof_leaf11.json")
    file = open(file_path, "r")     # open file
    json_file = json.loads(file.read())
    file.close()
    proof = json_file
    return proof


def get_dummie_proof_global_tree():
    file_path = _get_dummie_file_path("tg_proof_root1.json")
    file = open(file_path, "r")
    json_file = json.loads(file.read())
    file.close()
    proof = json_file['proof']
    return proof


def get_dummie_trusted_global_root():
    file_path = _get_dummie_file_path("tg_root.json")
    file = open(file_path, "r")
    json_file = json.loads(file.read())
    file.close()
    root_global = json_file['value']
    return root_global


def get_dummie_partial_global_roots():
    file_path = _get_dummie_file_path("partial_global_roots.json")
    file = open(file_path, "r")
    json_file = json.loads(file.read())
    file.close()
    return json_file


def get_dummie_middle_last_roots_from_partial_global():
    # get partial roots with tree_sizes
    partial_global_roots = get_dummie_partial_global_roots()
    roots = partial_global_roots["roots"]

    # select a middle root randomly
    random_middle_index = random.randint(1, len(roots) - 2)
    random_middle_root = roots[random_middle_index]
    middle_root_value = random_middle_root["value"]

    # select last root
    random_last_index = random_middle_index + 1
    last_root = roots[random_last_index]
    last_root_value = last_root["value"]

    # get consistency proof of middle root
    proofs = get_dummie_all_consistency_proof_global()["proofs"]   # get proofs from all_consistency_proof_global
    middle_merkle_proof = None
    for proof in proofs:
        if proof["root"]["value"] == last_root_value:
            middle_proof = proof["consistency_proof"]
            middle_merkle_proof = MerkleProof.deserialize(middle_proof)
            break

    # transform roots to bytes
    middle_root_bytes = bytes(middle_root_value, "utf_8")
    last_root_bytes = bytes(last_root_value, "utf_8")

    return middle_root_bytes, middle_merkle_proof, last_root_bytes


def get_dummie_local_root():
    file_path = _get_dummie_file_path("t1_root.json")
    file = open(file_path, "r")
    json_file = json.loads(file.read())
    file.close()
    root_global = json_file['value']
    return root_global


def get_dummie_all_leaf_global_tree():
    file_path = _get_dummie_file_path("all_leaf_global_tree.json")
    file = open(file_path, "r")
    json_file = json.loads(file.read())
    file.close()
    return json_file


def get_dummie_all_consistency_proof():
    file_path = _get_dummie_file_path("all_consistency_proof_tree1.json")
    file = open(file_path, "r")
    json_file = json.loads(file.read())
    file.close()
    return json_file


def get_dummie_all_consistency_proof_global():
    file_path = _get_dummie_file_path("all_consistency_proof_global.json")
    file = open(file_path, "r")
    json_file = json.loads(file.read())
    file.close()
    return json_file


def get_dummie_tree_name():
    return "tree1"


def get_dummie_data():
    return b"leaf11"


def _get_dummie_file_path(file_name):
    # To run locally
    # file_path = "../mock/mock_dev/v3/" + file_name  # use in development

    # To generate package
    file_path = pkg_resources.resource_filename('tlverifier', "/mock/mock_dev/v3/" + file_name)  # use in package

    return file_path
