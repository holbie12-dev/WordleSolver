# WordleSolver

Simple Python CLI tool that helps solve Wordle by filtering a word list based on guess feedback.

## Run

```bash
python wordleSolver.py
```

Interactive loop (up to 6 guesses):
1. Enter your 5-letter lowercase Wordle guess
2. Enter the result for each letter: `2` = green, `1` = yellow, `0` = grey
3. The solver prints the remaining valid words

## Files
```
WordleSolver/
├── wordleSolver.py     ← entry point, runs the interactive loop
├── wordleClasses.py    ← WordList (loads word list) + WordleSolver (filtering logic)
└── 5letterdoc.txt      ← word list (one word per line)
```

## Notes
- Must be run from the `WordleSolver/` directory — `wordleClasses.py` opens `5letterdoc.txt` with a relative path
- No dependencies beyond the Python standard library
