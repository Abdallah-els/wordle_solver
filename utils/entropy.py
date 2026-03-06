from math import log2
import numpy as np

def remaining_entropy(nu_elements=3242):
    """
    calclaute entropy with default = len(targets) 
    parmeter is the number of remeinig elments
    return the entropy 
    """
    if nu_elements == 0:
        return 0.0

    return log2(nu_elements)


def calc_word_entropy(row): 
    """ Return each guess entropy """

    # Unique returnes a tuple of list  for index = 0 it contains the elments
    # For index = 1 contains ferq of each elemnts 
    counts = np.unique(row, return_counts=True)[1] 
    # / -> in np devied each elemnt in list with counts.sum()
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
    sorted_entropy = dict(sorted(entropy_dic.items(), key=lambda item: item[1], reverse=True))

    return sorted_entropy