import pygame
import json
import random
import sys
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 700
GRID_ROWS = 6
GRID_COLS = 5
CELL_SIZE = 60
CELL_MARGIN = 5
GRID_START_X = (WINDOW_WIDTH - (GRID_COLS * (CELL_SIZE + CELL_MARGIN))) // 2
GRID_START_Y = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
DARK_GRAY = (58, 58, 58)
GREEN = (106, 170, 100)
YELLOW = (181, 159, 59)
RED = (220, 50, 50)
LIGHT_GRAY = (200, 200, 200)

# Fonts
TITLE_FONT = pygame.font.Font(None, 48)
GRID_FONT = pygame.font.Font(None, 36)
INFO_FONT = pygame.font.Font(None, 24)


class WordleGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Wordle Solver")
        self.clock = pygame.time.Clock()
        
        # Load game data
        try:
            with open('dataset/targets_5_letter.json', 'r') as f:
                self.answer_list = json.load(f)
            with open('dataset/dictionary_5_letter.json', 'r') as f:
                self.dictionary = json.load(f)
        except FileNotFoundError as e:
            print(f"Error loading data: {e}")
            sys.exit(1)
        
        self.reset_game()
    
    def reset_game(self):
        """Reset game state"""
        self.answer = random.choice(self.answer_list).upper()
        self.guesses: List[str] = []
        self.feedbacks: List[str] = []
        self.current_input = ""
        self.game_over = False
        self.won = False
        self.message = ""
        self.used_letters = set()
        self.green_letters = {}  # position -> letter
        self.yellow_letters = set()
        self.gray_letters = set()
    
    def get_feedback(self, guess: str, answer: str) -> str:
        """
        Generate feedback for a guess.
        'g' = green (correct position)
        'y' = yellow (wrong position)
        'r' = gray (not in word)
        """
        guess = guess.upper()
        answer = answer.upper()
        feedback = ['r'] * len(guess)
        answer_list = list(answer)
        
        # First pass: mark greens
        for i, (g_char, a_char) in enumerate(zip(guess, answer)):
            if g_char == a_char:
                feedback[i] = 'g'
                answer_list[i] = None
        
        # Second pass: mark yellows
        for i, g_char in enumerate(guess):
            if feedback[i] == 'r' and g_char in answer_list:
                feedback[i] = 'y'
                answer_list[answer_list.index(g_char)] = None
        
        return ''.join(feedback)
    
    def submit_guess(self):
        """Submit the current guess"""
        guess = self.current_input.upper()
        
        if len(guess) != 5:
            self.message = "Word must be 5 letters!"
            return
        
        if guess not in self.dictionary and guess not in self.answer_list:
            self.message = "Not a valid word!"
            return
        
        # Generate feedback
        feedback = self.get_feedback(guess, self.answer)
        
        self.guesses.append(guess)
        self.feedbacks.append(feedback)
        self.current_input = ""
        self.message = ""
        
        # Update letter states
        for i, (letter, fb) in enumerate(zip(guess, feedback)):
            self.used_letters.add(letter)
            if fb == 'g':
                self.green_letters[i] = letter
            elif fb == 'y':
                self.yellow_letters.add(letter)
            elif fb == 'r' and letter not in self.green_letters.values() and letter not in self.yellow_letters:
                self.gray_letters.add(letter)
        
        # Check win/loss
        if guess == self.answer:
            self.game_over = True
            self.won = True
            self.message = f"You Won! The answer was {self.answer}"
        elif len(self.guesses) >= GRID_ROWS:
            self.game_over = True
            self.won = False
            self.message = f"Game Over! The answer was {self.answer}"
    
    def handle_input(self, event):
        """Handle keyboard input"""
        if self.game_over:
            if event.key == pygame.K_RETURN:
                self.reset_game()
            return
        
        if event.key == pygame.K_RETURN:
            self.submit_guess()
        elif event.key == pygame.K_BACKSPACE:
            self.current_input = self.current_input[:-1]
        elif len(self.current_input) < 5 and event.unicode.isalpha():
            self.current_input += event.unicode.upper()
        elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.reset_game()
    
    def draw_grid(self):
        """Draw the guess grid"""
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                x = GRID_START_X + col * (CELL_SIZE + CELL_MARGIN)
                y = GRID_START_Y + row * (CELL_SIZE + CELL_MARGIN)
                
                # Determine cell color and letter
                if row < len(self.guesses):
                    letter = self.guesses[row][col]
                    feedback = self.feedbacks[row][col]
                    
                    if feedback == 'g':
                        color = GREEN
                    elif feedback == 'y':
                        color = YELLOW
                    else:
                        color = GRAY
                elif row == len(self.guesses):
                    letter = self.current_input[col] if col < len(self.current_input) else ""
                    color = LIGHT_GRAY
                else:
                    letter = ""
                    color = DARK_GRAY
                
                # Draw cell
                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE), 2)
                
                # Draw letter
                if letter:
                    text = GRID_FONT.render(letter, True, WHITE)
                    text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    self.screen.blit(text, text_rect)
    
    def draw_keyboard(self):
        """Draw keyboard showing used letters"""
        keyboard_layout = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        ]
        
        start_y = GRID_START_Y + GRID_ROWS * (CELL_SIZE + CELL_MARGIN) + 30
        key_width = 30
        key_height = 30
        key_margin = 4
        
        for row_idx, row in enumerate(keyboard_layout):
            start_x = (WINDOW_WIDTH - sum(key_width + key_margin for _ in row)) // 2
            for col_idx, key in enumerate(row):
                x = start_x + col_idx * (key_width + key_margin)
                y = start_y + row_idx * (key_height + key_margin)
                
                # Determine key color
                if key in self.green_letters.values():
                    color = GREEN
                elif key in self.yellow_letters:
                    color = YELLOW
                elif key in self.gray_letters:
                    color = GRAY
                else:
                    color = LIGHT_GRAY
                
                pygame.draw.rect(self.screen, color, (x, y, key_width, key_height))
                pygame.draw.rect(self.screen, WHITE, (x, y, key_width, key_height), 1)
                
                text = pygame.font.Font(None, 16).render(key, True, WHITE)
                text_rect = text.get_rect(center=(x + key_width // 2, y + key_height // 2))
                self.screen.blit(text, text_rect)
    
    def draw_info(self):
        """Draw game info"""
        # Title
        title = TITLE_FONT.render("WORDLE", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)
        
        # Guesses remaining
        remaining = GRID_ROWS - len(self.guesses)
        info_text = INFO_FONT.render(f"Guesses: {len(self.guesses)}/{GRID_ROWS}", True, WHITE)
        self.screen.blit(info_text, (20, 65))
        
        # Message
        if self.message:
            msg_color = GREEN if self.won else RED
            msg_text = INFO_FONT.render(self.message, True, msg_color)
            msg_rect = msg_text.get_rect(center=(WINDOW_WIDTH // 2, 650))
            self.screen.blit(msg_text, msg_rect)
        
        # Instructions
        if self.game_over:
            inst_text = INFO_FONT.render("Press ENTER to play again", True, LIGHT_GRAY)
            inst_rect = inst_text.get_rect(center=(WINDOW_WIDTH // 2, 675))
            self.screen.blit(inst_text, inst_rect)
    
    def draw(self):
        """Render everything"""
        self.screen.fill(BLACK)
        self.draw_info()
        self.draw_grid()
        self.draw_keyboard()
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_input(event)
            
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = WordleGUI()
    game.run()
