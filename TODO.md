# WordleSolver — TODO

## Solver Strategy
- [ ] Add an entropy-based "best next guess" suggestion — rank remaining candidates by expected information gain rather than just listing them
- [ ] Add a hard-mode option that restricts suggestions to words consistent with all previous feedback (Wordle hard mode rules)
- [ ] Precompute starting word ranking and suggest the optimal opener (e.g. "CRANE", "RAISE") on the first guess

## Usability
- [ ] Accept absolute path to `5letterdoc.txt` via a CLI arg so the solver can be run from any directory (currently must be run from the project folder)
- [ ] Add a `--auto` benchmark mode that runs the solver against all words in the list and reports average guesses to completion

## Quality
- [ ] Add a unit test that verifies the filter logic correctly narrows candidates on a known feedback sequence
- [ ] Write a short `README.md` covering how to run the solver and how to enter feedback
