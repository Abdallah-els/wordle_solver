def filter_remaining_targets(matrix, guess_idx, feedback_code, remaining_indices):
    """
    This funcation filter the cols based on the feedback_code.
    If the feedbackes are equals so this word wont be filterd
    """
    row_view = matrix[guess_idx, remaining_indices]
    equal_idx = (row_view == feedback_code)
    new_remaining_indices = remaining_indices[equal_idx]
    
    return new_remaining_indices


def feedback_genrator(guess, target, feedbacksdic):
    """
    Take the guees and the target and compere between all letters.
    Retrurns the code of the feedback from feedbackdic
    Only used in the matrix genrator.
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

