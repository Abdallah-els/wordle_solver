import numpy as np

from utils.load import load_json, load_matrix
from utils.entropy import remaining_entropy, calc_all_words_entropy
from utils.helper import filter_remaining_targets

if __name__ == "__main__":

    target_list = load_json('dataset/targets_5_letter.json')
    guess_list = load_json('dataset/dictionary_5_letter.json')
    feedbacks = load_json('dataset/feedbacks.json')
    matrix = load_matrix("utils/pattern_matrix.npy")

    print(f"\n\t\t\t\t Hello to our wordel solver. \n")
    print("This app for computing and understanding inforamtion theory " \
    "and entropy concept.")
    print("You have to guess a word of 5 letters in hello wordel website" \
    " and then write the feedback you get from teh website.\n\n")
    
    remaining_idx = np.arange(len(target_list))
    remaining_idx_len = len(target_list)
    
    while(remaining_idx_len > 1):

        current_entropy = remaining_entropy(remaining_idx_len)
        print(f"You need about {current_entropy:.8f} bits/symbole")
        print(f"Remaining possible answers: {remaining_idx_len}\n")

        print("Best words to guess: ")
        sorted_entropy = calc_all_words_entropy(matrix,guess_list,remaining_idx)
        best = ""

        for i, (key, value) in enumerate(sorted_entropy.items()):
            if i > 10:
                break
            if i == 0:
                best = key
            print(f"{i + 1} - {key}  entropy = {value}")

        print(f"\nEnter your guess: ")
        guess = input(f"BEST={best}")
        feedback = input(f"Enter your feedback (r->grey, y->yellow, g->green) (eg. rggry): ")
        
        feedback_code = feedbacks[feedback]
        guess_idx = guess_list.index(guess)
        
        remaining_idx = filter_remaining_targets(
            matrix, guess_idx, feedback_code, remaining_idx
        )
        remaining_idx_len = len(remaining_idx)


    answer = target_list[remaining_idx[0]]
    print(f"\nThe final answer is: {answer}")
    print(f"BEST={answer}")

