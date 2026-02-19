import json
import sys
import math

N_BRANCHES = 3**5 # total number of possible feedback patterns for 5-letter words (3^5)

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The path {path} was not found.")
        sys.exit(1)  

def remaining_entropy(n_elements):
    """
    Calculate the Shannon entropy of a branch with a given number of elements.
    This represents the uncertainty (in bits) of choosing one element from the branch.
    Parameters:
        n_elements (int): Number of elements in the branch (pattern).
    Returns:
        float: Entropy in bits.
    """
    if n_elements == 0:
        return 0.0
     
    entropy = 0.0
    prob = 1/n_elements 
    for i in range(n_elements):
        entropy -= prob * math.log(prob , 2)
    return entropy


def calc_word_entropy(n_remaining_answers): 
    """
    Calculate the total expected entropy across all possible feedback branches.
    Each branch corresponds to a unique feedback pattern for a guess.
    Parameters:
        n_remaining_answers (list[int]): List of number of remaining answers in each branch.
    Returns:
        float: Total expected entropy.
    """
    entropy = 0.0
    for i in range (N_BRANCHES):
        prob = 1 / n_remaining_answers[i]
        entropy -= prob * math.log(prob , 2)


def get_remaining_answers(current_remaining_answers, guess, feedback):
    """
    Filters remaining answers based on a guess and Wordle-like feedback.
    Parameters:
        current_remaining_answers (list[str]): List of possible words.
        guess (str): The guessed word.
        feedback (str): feedback string with 'g', 'y', 'r' per letter.
    Returns:
        list[str]: Filtered list of possible words.
    """
    remaining = []

    for word in current_remaining_answers:
        match = True
        for i, (g_char, s_char) in enumerate(zip(guess, feedback)):
            if s_char == 'g':  # green: correct letter, correct position
                if word[i] != g_char:
                    match = False
                    break
            elif s_char == 'y':  # yellow: correct letter, wrong position
                if g_char not in word or word[i] == g_char:
                    match = False
                    break
            elif s_char == 'r':  # gray: letter not in word
                # handle repeated letters: only exclude if word has more occurrences than needed
                if g_char in word:
                    # check if guess has repeated letters that are green/yellow
                    required_count = sum(
                        1 for idx, c in enumerate(guess) 
                        if c == g_char and feedback[idx] in ('g', 'y')
                    )
                    if word.count(g_char) > required_count:
                        match = False
                        break
        if match:
            remaining.append(word)

    return remaining

    
    

if __name__ == "__main__":
    answers = load_json('dataset/targets_5_letter.json')
    dictionary = load_json('dataset/dictionary_5_letter.json')
    feedbacks = load_json('dataset/feedbacks.json')

    initial_entropy = remaining_entropy(len(answers))

    print(initial_entropy)

    