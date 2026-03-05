import json
import sys
from math import log2

import numpy as np

# Total number of possible feedback patterns for 5-letter words (3^5).
N_BRANCHES = 3**5 

def load_json(path):
    """
    Loading files
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The path {path} was not found.")
        sys.exit(1)  


def load_matrix(path):
    """Loading matrix."""
    matrix = np.load(path)    
    
    return matrix

def remaining_entropy(nu_elements=3242):
    """
    calclaute entropy with default = len(targets) 
    parmeter is the number of remeinig elments
    return the entropy 
    """
    if nu_elements == 0:
        return 0.0

    return log2(nu_elements)


def feedback_genrator(guess, target, feedbacksdic):
    """
    Take the guees and the target and compere between all letters.
    Retrurns the code of the feedback from feedbackdic
    """

    res = [None] * 5
    target_list = list(target)
    

    for i in range(5):
        if guess[i] == target[i]:
            res[i] = 'g'
            target_list[i] = None 
            
    
    for i in range(5):
        if res[i] is None: 
            if guess[i] in target_list:
                res[i] = 'y'
                target_list[target_list.index(guess[i])] = None
            else:
                res[i] = 'r'
                
 
    feedback = "".join(res)

    return feedbacksdic[feedback]


def calc_word_entropy(row, ): 
    """
    Return each guess entropy
    """
    # Unique returnes a tuple of list  for index = 0 it contains the elments
    # For index = 1 contains ferq of each elemnts 
    counts = np.unique(row, return_counts=True)[1] 
    # / -> in np devied each elemnt in list with couts.sum()
    prob = counts / counts.sum()
    entropy = -np.sum(prob * np.log2(prob))

    return entropy

def calc_all_words_entropy(matrix, guess_list,remainng_idx):
    """
    It will loop in all rows and get the entropy of each guess .
    Return a sorted dictionary by values.
    Keys = word, value = entropy.
    """

    entropy_dic = {}

    for i in range(len(guess_list)):
        entropy = calc_word_entropy(matrix[i, remainng_idx])
        entropy_dic[guess_list[i]] = entropy 

    # Items methode returns tuble.
    # Item: item[1] means sort in values not keys
    # reverse to sort decending
    #dict funcation make the tuplrs again dic
    sorted_entropy = dict(sorted(entropy_dic.items(), 
                                 key=lambda item: item[1], reverse=True))


    return sorted_entropy


def filter_remaining_targets(matrix, guess_idx, feedback_code, remaining_indices):
    """
    This funcation filter the cols based on the feedback_code.
    If the feedbackes are equals so this word wont be filterd
    """
    
    row_view = matrix[guess_idx, remaining_indices]
    equal_idx = (row_view == feedback_code)
    new_remaining_indices = remaining_indices[equal_idx]
    
    return new_remaining_indices

def solver_logic(target_list, matrix, guess_list, feedbackes):
    """
    Compute all funcations here
    """
    
    print(f"\n\n\t\t\t\t\tHello to our wordel solver.\n\n\n")
    print("This app for computing and understanding inforamtion theory " \
    "and entropy concept.")
    print("You have to guess a word of 5 letters in hello wordel website" \
    " and then write the feedback you get from teh website.\n\n")
    
    remaining_idx = np.arange(len(target_list))
    remaining_idx_len = len(target_list)
    
    while(remaining_idx_len > 1):
        current_entropy = remaining_entropy(remaining_idx_len)
        print(f"You need about {current_entropy:.8f} bits/symbole")

        print("Best words to guess: ")
        sorted_entropy = calc_all_words_entropy(matrix,guess_list,remaining_idx)
        best = ""

        for i, (key, value) in enumerate(sorted_entropy.items()):
            if i > 10:
                break
            if i == 0:
                best = key
            print(f"{i + 1} - {key}  entropy = {value}")

        print(f"\nBest = {best}")
        guess = input(f"\nEnter your guess: ")
        feedback = input(f"Enter your feedback (r->grey, y->yellow, g->green)" 
                         "(eg. rggry): ")
        
        feedback_code = feedbackes[feedback]
        guess_idx = guess_list.index(guess)
        remaining_idx = filter_remaining_targets(
            matrix, guess_idx, feedback_code, remaining_idx
        )
        remaining_idx_len = len(remaining_idx)


    print(f"The final answer is: {target_list[remaining_idx[0]]}")




    

if __name__ == "__main__":
    target_list = load_json('dataset/targets_5_letter.json')
    guess_list = load_json('dataset/dictionary_5_letter.json')
    feedbacks = load_json('dataset/feedbacks.json')
    matrix = load_matrix("pattern_matrix.npy")

    solver_logic(target_list, matrix,guess_list, feedbacks)

    