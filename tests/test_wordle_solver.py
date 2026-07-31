"""
Tests for WordleSolver filtering logic.

The WordleSolver's three filtering methods are the core logic:
  handleGreen  — keep words where letter at index matches exactly
  handleYellow — keep words that contain letter but NOT at that index
  handleGrey   — remove words that contain the letter at all

We inject a known word list directly instead of reading 5letterdoc.txt.

Run: pytest tests/test_wordle_solver.py -v
     (from the WordleSolver/ directory)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from wordleClasses import WordleSolver


def make_solver(words: list[str]) -> WordleSolver:
    """Create a WordleSolver with an injected word list (no file I/O)."""
    solver = WordleSolver.__new__(WordleSolver)
    solver.wordlist = list(words)
    return solver


SAMPLE_WORDS = ["crane", "crabs", "brain", "bread", "brave", "braid", "grabs", "trail"]


class TestHandleGreen:
    def test_keeps_words_with_exact_letter_at_index(self):
        solver = make_solver(SAMPLE_WORDS)
        solver.handleGreen(0, "b")  # letter 'b' must be at index 0
        for word in solver.wordlist:
            assert word[0] == "b"

    def test_removes_words_without_letter_at_index(self):
        solver = make_solver(SAMPLE_WORDS)
        solver.handleGreen(0, "b")
        assert "crane" not in solver.wordlist
        assert "grabs" not in solver.wordlist

    def test_green_on_last_index(self):
        solver = make_solver(["crane", "crabs", "stone", "brave"])
        solver.handleGreen(4, "e")  # last letter must be 'e'
        assert solver.wordlist == ["crane", "stone", "brave"]

    def test_green_reduces_to_single_word(self):
        solver = make_solver(["crane", "crabs"])
        solver.handleGreen(4, "s")
        assert solver.wordlist == ["crabs"]

    def test_green_can_empty_list(self):
        solver = make_solver(["crane", "crabs"])
        solver.handleGreen(0, "z")
        assert solver.wordlist == []

    def test_multiple_green_constraints_compound(self):
        solver = make_solver(SAMPLE_WORDS)
        solver.handleGreen(0, "b")
        solver.handleGreen(1, "r")
        for word in solver.wordlist:
            assert word[0] == "b" and word[1] == "r"

    def test_all_words_match_constraint(self):
        solver = make_solver(["crane", "crave", "crimp"])
        solver.handleGreen(0, "c")
        assert len(solver.wordlist) == 3


class TestHandleYellow:
    def test_keeps_words_containing_letter_not_at_index(self):
        solver = make_solver(SAMPLE_WORDS)
        solver.handleYellow(0, "r")  # 'r' exists but not at index 0
        for word in solver.wordlist:
            assert "r" in word
            assert word[0] != "r"

    def test_removes_words_missing_letter(self):
        solver = make_solver(["crane", "trail", "stone"])
        solver.handleYellow(0, "r")
        assert "stone" not in solver.wordlist  # no 'r' at all

    def test_removes_words_with_letter_at_wrong_position(self):
        solver = make_solver(["crane", "robin", "brain"])
        solver.handleYellow(0, "r")
        # "robin" has 'r' at index 0 — should be removed
        assert "robin" not in solver.wordlist
        # "crane" has 'r' at index 2 — keeps it
        assert "crane" in solver.wordlist

    def test_yellow_must_have_letter_somewhere_else(self):
        words = ["racer", "crane", "risen", "blank"]
        solver = make_solver(words)
        solver.handleYellow(0, "r")
        for word in solver.wordlist:
            assert "r" in word and word[0] != "r"

    def test_yellow_on_middle_index(self):
        solver = make_solver(["crane", "trace", "grace"])
        solver.handleYellow(2, "a")  # 'a' must exist but not at index 2
        # "crane"[2] = 'a' — excluded
        assert "crane" not in solver.wordlist
        # "trace"[2] = 'a' — excluded
        assert "trace" not in solver.wordlist
        # "grace"[2] = 'a' — excluded
        assert "grace" not in solver.wordlist


class TestHandleGrey:
    def test_removes_all_words_containing_letter(self):
        solver = make_solver(SAMPLE_WORDS)
        solver.handleGrey("e")
        for word in solver.wordlist:
            assert "e" not in word

    def test_keeps_words_without_letter(self):
        solver = make_solver(["crane", "crabs", "trail"])
        solver.handleGrey("e")
        assert "crabs" in solver.wordlist
        assert "trail" in solver.wordlist
        assert "crane" not in solver.wordlist

    def test_grey_on_absent_letter_keeps_all(self):
        solver = make_solver(["crane", "crabs", "trail"])
        before = list(solver.wordlist)
        solver.handleGrey("z")
        assert solver.wordlist == before

    def test_grey_can_empty_list(self):
        solver = make_solver(["crane", "grape", "trade"])
        solver.handleGrey("a")
        assert solver.wordlist == []

    def test_multiple_grey_constraints_compound(self):
        solver = make_solver(["crane", "brisk", "flops", "grabs"])
        solver.handleGrey("e")
        solver.handleGrey("a")
        for word in solver.wordlist:
            assert "e" not in word and "a" not in word


class TestCombinedFiltering:
    def test_green_yellow_grey_chain(self):
        """Simulate a realistic guess sequence and verify correct candidates remain."""
        words = ["crane", "crabs", "brain", "bread", "brave", "braid", "grabs", "trail", "bland"]
        solver = make_solver(words)
        # Guess "crane": c=grey, r=yellow(pos1), a=yellow(pos2), n=grey, e=grey
        solver.handleGrey("c")
        solver.handleYellow(1, "r")
        solver.handleYellow(2, "a")
        solver.handleGrey("n")
        solver.handleGrey("e")
        # All remaining words must: have 'r' not at index 1, have 'a' not at index 2,
        # and not contain 'c', 'n', or 'e'.
        for word in solver.wordlist:
            assert "c" not in word
            assert "n" not in word
            assert "e" not in word
            assert "r" in word and word[1] != "r"
            assert "a" in word and word[2] != "a"

    def test_green_locks_position_and_grey_removes(self):
        words = ["brain", "bread", "braid", "brisk", "brook"]
        solver = make_solver(words)
        solver.handleGreen(0, "b")
        solver.handleGreen(1, "r")
        solver.handleGrey("e")
        for word in solver.wordlist:
            assert word[0] == "b" and word[1] == "r" and "e" not in word
