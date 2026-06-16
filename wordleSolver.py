from wordleClasses import WordleSolver


def main():
    ## The function created to solve once game
    wordleSolver = WordleSolver() ## Creating Instance
    for i in range(6):
        wordleSolver.inputSearch()
        wordleSolver.handleGuess()
        for index,outcome in enumerate(wordleSolver.guessResult):
            if outcome =='2':
                wordleSolver.handleGreen(index, wordleSolver.wordleGuess[index])
            elif outcome == '1':
                wordleSolver.handleYellow(index, wordleSolver.wordleGuess[index])
            else:
                wordleSolver.handleGrey(wordleSolver.wordleGuess[index])
        print(wordleSolver.wordlist)


if __name__ == "__main__":
    main()