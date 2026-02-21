import pathlib
import json
import random



class GameLogic:
    """
    Game logic
    1 - Randomize json file and choose one word
    2 - loop in range 6.
    """

    def __init__(self, path_of_3k, path_of_13k):
        """Importing the path location."""
        self.path_of_3k = pathlib.Path(path_of_3k)
        self.path_of_13k = pathlib.Path(path_of_13k)

    def json_file(self):
        """Reading json file"""
        file_data1 = self.path_of_3k.read_text()
        file_data2 = self.path_of_3k.read_text()
        self.content_of_3k = json.loads(file_data1)
        self.content_of_13k = json.loads(file_data2)


    def randomize_file(self):
        """Randomize the file and get 1 possible answer."""
        self.answer = random.choice(self.content_of_3k)
        print(self.answer)

    def  main_logic(self):
        """Implment the main logic of the game."""
        max_guess = 6

        print("\nWelcome in Hello wordl!\n")

        while max_guess:
            self.guess = input("Enter your guess: ")
            
            if (self.guess not in self.content_of_3k and 
                self.guess not in self.content_of_13k):
                print("Please enter an english word\n")
                continue
            
            if(self.answer == self.guess):
                print(f"\nYou Won, The answer is {self.answer}\n")
                break
            
            else:
                print("Wrong answer, Try again!\n")
                max_guess -=1

        if self.answer != self.guess:
            print("\nSorry you lost!")
            print(f"The answer is: {self.answer}")


def start_the_game():
    """Starting the game"""
    
    start_game = GameLogic("dataset/targets_5_letter.json",
                       "dataset/dictionary_5_letter.json")
    start_game.json_file()
    start_game.randomize_file()
    start_game.main_logic()



start_the_game()

