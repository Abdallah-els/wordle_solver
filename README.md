# Wordle Solver

A Python-based Wordle solver that uses **Information Theory** to optimally 
solve the puzzle in minimal guesses.

## How It Works

The solver applies **entropy** to evaluate every possible guess and select 
the one that reveals the most information. Feedback patterns (green, yellow, 
gray) are encoded and processed through a **precomputed matrix**, which maps 
every word-guess pair to its resulting pattern — enabling fast and efficient 
filtering of remaining candidates.

## Optimization

The core bottleneck in any Wordle solver is the repeated computation of 
feedback patterns across thousands of word pairs. We tackled this by:

- **Precomputing a full pattern matrix** — all word-guess feedback patterns 
  are calculated once and stored, eliminating redundant computation during 
  solving
- **Entropy-based pruning** — at each step, only the guess with the highest 
  information gain is chosen, minimizing the expected number of remaining 
  candidates
- **Vectorized filtering** — the candidate word list is sliced directly from 
  the matrix row, avoiding full list rescans
- **Early termination** — the solver exits as soon as the candidate pool 
  drops to 1, skipping unnecessary entropy calculations

This reduces the average solving time significantly while keeping the 
solution count to **3–4 guesses**.

## Project Structure

​```
wordle_solver/
├── dataset/        # Word lists and frequency data
├── generators/     # Matrix and pattern generators
├── utils/          # Helper functions
└── main.py         # Entry point
​```

## Usage

​```bash
python main.py
​```

## Reference
- Open source Wordle: https://hellowordl.net/
