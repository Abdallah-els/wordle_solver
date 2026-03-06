# Wordle Solver

A Python-based Wordle solver that uses **Information Theory** to optimally solve the puzzle in minimal guesses.

## How It Works

The solver applies the concept of **entropy** to evaluate every possible guess and select the one that reveals the most information. Feedback patterns (green, yellow, gray) are encoded and processed through a **precomputed matrix**, which maps every word-guess pair to its resulting pattern — enabling fast and efficient filtering of remaining candidates.

## Approach

- Represent all possible feedback patterns as a matrix
- Compute entropy for each candidate word based on the probability distribution of outcomes
- Select the guess with the highest entropy (maximum information gain)
- Filter the word list based on received feedback
- Repeat until the solution is found

## Performance

Solves the majority of Wordle puzzles in **3–4 attempts**

## Project Structure
```
wordle_solver/
├── dataset/        # Word lists and frequency data
├── generators/     # Matrix and pattern generators
├── utils/          # Helper functions
└── main.py         # Entry point
```

## Usage
```bash
python main.py
```

## Reference

- Open source Wordle: https://hellowordl.net/
