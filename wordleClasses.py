class WordList: 
    def __init__(self) -> None:
        with open('5letterdoc.txt', 'r') as file:
            lines = file.readlines()
        self.wordLst = [line.strip() for line in lines]

class WordleSolver: 
    def __init__(self) -> None:
        self.wordlist = WordList().wordLst 
    
    def inputSearch(self):
        ### This is code for handling and reading in the user input for the search string
        self.wordleGuess = ''
        print('For this search to work, it must contain 5 lowercase English letter that correspond to a wordle guess')
        validSearch = False
        while validSearch == False: 
            attemptedSearch = input('Input your wordle guess: ')
            if len(attemptedSearch)==5 and attemptedSearch.isalpha() and attemptedSearch.islower():
                self.wordleGuess = attemptedSearch
                validSearch = True
            else: 
                print('Invalid search')
    
    def handleGuess(self):
        ### This code handles the reading the guessed string. 
        self.guessResult = ''
        for letter in range(5):
            inputString = f'''What is the result of {letter + 1} value:
            if Green (Full Match) = 2
            if Yellow (Partial Match) = 1
            if Grey (No Match) = 0
            '''
            validInput = False
            while validInput == False:
                result = input(inputString)
                if result in ['0', '1', '2']:
                    validInput = True
                    self.guessResult += result
        

    def handleGreen(self,matchIndex, matchLetter):
        ## Code to handle Perfect Matches
        updateWordList = []
        for word in self.wordlist:
            if word[matchIndex] == matchLetter:
                updateWordList += [word]
        self.wordlist = updateWordList

    def handleYellow(self, matchedIndex, matchLetter):
        ##Code to handle partial matches
        updateWordList = []
        for word in self.wordlist:
            if matchLetter in word:
                if word[matchedIndex] != matchLetter:
                    updateWordList += [word]
        self.wordlist = updateWordList

    def handleGrey(self, matchLetter):
        ## Code to handle no Match
        updateWordList = []
        for word in self.wordlist:
            if matchLetter not in word:
                updateWordList += [word]
        self.wordlist = updateWordList
                
