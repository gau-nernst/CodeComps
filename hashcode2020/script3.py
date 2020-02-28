class Library:
    def __init__(self, index, N, T, M, books):
        self.index = index
        self.N = N
        self.T = T
        self.M = M
        self.books = books

    def updateScore(self, daysLeft):
        # self.score = sum([S[bookIndex] for bookIndex in self.books[0:daysLeft-self.T]])
        self.score = len(self.books[0:daysLeft-self.T])
        return self.score

    def removeBook(self, anotherLib):
        self.books = [book for book in self.books if not book in anotherLib]

def loadData(path):
    with open(path) as f:
        line1 = f.readline().rstrip()
        B, L, D = list(map(int, line1.split(' ')))
        line2 = f.readline().rstrip()
        S = list(map(int, line2.split(' ')))
        Libraries = []
        for i in range(L):
            line = f.readline().rstrip()
            N, T, M = list(map(int, line.split(' ')))
            nextLine = f.readline().rstrip()
            books = list(map(int, nextLine.split(' ')))
            library = Library(i, N, T, M, books)
            Libraries.append(library)

    return B, L, D, S, Libraries        

def printData(B, L, D, S, Libraries):
    print(B, L, D, S)
    for i in range(len(Libraries)):
        print(vars(Libraries[i]))

def getScore(index):
    return S[index]

def sortBooks(library):
    library.books = sorted(library.books, key=getScore)
    library.books.reverse()

def writeOutput(path, A, libList):
    line1 = str(A)
    with open(path, 'w') as f:
        f.write(line1)
        f.write('\n')
        for lib in libList:
            index = lib[0]
            numBook = lib[1]
            signUpBooks = lib[2:]
            line = str(index) + ' ' + str(numBook) + '\n'
            f.write(line)
            nextLine = ' '.join(str(book) for book in signUpBooks)
            f.write(nextLine)
            f.write('\n')

paths = [
    # 'a_example',
    'b_read_on', 
    # 'c_incunabula',
    # 'd_tough_choices', 
    # 'e_so_many_books', 
    # 'f_libraries_of_the_world'
    ]

for PATH in paths:
    B, L, D, S, Libraries = loadData(PATH+'.txt')
    # list(map(sortBooks, Libraries))
    # printData(B, L, D, S, Libraries)

    libraryList = []
    daysLeft = D
    [library.updateScore(daysLeft) for library in Libraries]
    sortedList = sorted(Libraries, key=lambda x: x.score)
    sortedList.reverse()
    
    # while daysLeft > 0 and len(libraryList)<L:
    for nextLib in sortedList:
        # [library.updateScore(daysLeft) for library in Libraries]
        # nextLib = max([library for library in Libraries], key=lambda x: x.score)
        
        # daysLeft -= nextLib.T
        
        libraryList.append([nextLib.index, len(nextLib.books)] + nextLib.books)

        # Libraries.remove(nextLib)
        [library.removeBook(nextLib.books[:nextLib.M*daysLeft]) for library in Libraries]
        
    writeOutput(PATH+'_output_extended.txt', len(libraryList), libraryList)