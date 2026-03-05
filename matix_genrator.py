import numpy as np
from pathlib import Path
import json 

from solver import feedback_genrator

def open_json_file(path):
    """
    Reading the file.
    """

    path_of_file = Path(path)
    file = path_of_file.read_text()
    target = json.loads(file)
    return target

def matrix_genrator(guess, targets, feedback_dic):
    """
    Genrate a matrix of len(guess) x len(target).
    We do that to make the programe faster.
    The elements of that matriex will be the buckets.
    At the end we will save that file to put it in the main logic file.  
    """

    G = len(guess)
    A = len(targets)

    matrix = np.zeros((G, A), dtype=np.uint8)

    for k in range(G):
        for j in range(A):
            matrix[k, j] = feedback_genrator(guess[k], targets[j], feedback_dic)

    np.save('pattern_matrix.npy', matrix)

if __name__ == "__main__":
    guess = open_json_file("dataset/dictionary_5_letter.json")
    target = open_json_file("dataset/targets_5_letter.json")
    feedback_dic = open_json_file("dataset/feedbacks.json")

    matrix_genrator(guess, target,feedback_dic)





