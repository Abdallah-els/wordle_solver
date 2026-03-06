import json
import sys
import numpy as np

def load_json(path):
    """ Loading files """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The path {path} was not found.")
        sys.exit(1)  


def load_matrix(path):
    """ Loading matrix """
    matrix = np.load(path)    
    return matrix
