from math import log2



def get_entropy(len_possible_answer):
    entropy = log2(len_possible_answer)
    if len_possible_answer <= 0: return 0
    return entropy


def get_feedback_code(guess, word):
    
    code = 0
    for i in range(len(guess)):
        if guess[i] == word[i]:
            code += 2**i
    return code

def get_remaining_words(possible_answer, guess, actual_feedback_code):

    remaining = []
    for word in possible_answer:
        if get_feedback_code(guess, word) == actual_feedback_code:
            remaining.append(word)
    return remaining
def calculate_expected_entropy(guess, possible_answers):
    counts = [0] * 8
    for word in possible_answers:
        code = get_feedback_code(guess, word)
        counts[code] += 1
    
    entropy = 0
    total = len(possible_answers)
    for count in counts:
        if count > 0:
            p = count / total
            entropy += p * log2(1/p)
            
    return entropy

def game():
    words = ["ahm", "alk", "rst", "lno"]
    possible_answer = words[::]
    
    
    feedback_map = {"rrr": 0, "grr": 1, "rgr": 2, "ggr": 3, "rrg": 4, "grg": 5, "rgg": 6, "ggg": 7}
    
    while len(possible_answer) > 1:
        #
        
        suggestions = []

        for g in words: 
            ent = calculate_expected_entropy(g, possible_answer)
            suggestions.append((g, ent))
        
      
        suggestions.sort(key=lambda x: x[1], reverse=True)
        
        print("Top Suggestions:")
        for s_word, s_ent in suggestions[:3]:
            print(f"- {s_word}: {s_ent:.2f} bits")
        
        

        print(f"\nRemaining words ({len(possible_answer)}): {possible_answer}")
        
        current_entropy = get_entropy(len(possible_answer))
        print(f"Current Entropy (Uncertainty): {current_entropy:.2f} bits")
        
        guess = input("Enter your guess: ")
        fb_str = input("Enter the feedback (e.g., rrr, grr): ")
        
        actual_code = feedback_map[fb_str]
        
        
        possible_answer = get_remaining_words(possible_answer, guess, actual_code)
        
    if len(possible_answer) == 1:
        print(f"\nThe answer is: {possible_answer[0]}")
    else:
        print("\nNo words match that feedback!")


if __name__ == "__main__":
    game()



