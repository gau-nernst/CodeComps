import math
B, L, D, S, N, T, M, books = [0 for i in range(8)]
Nuniques = 0

def loadData(path):
    global B, L, D, S, N, T, M, books, Nuniques
    with open(path) as f:
        line1 = f.readline().rstrip()
        B, L, D = [int(number) for number in line1.split(' ')]
        line2 = f.readline().rstrip()
        S = [int(number) for number in line2.split(' ')]
        N = []
        T = []
        M = []
        books = []
        for i in range(L):
            line = f.readline().rstrip()
            Ni, Ti, Mi = [int(number) for number in line.split(' ')]
            N.append(Ni)
            T.append(Ti)
            M.append(Mi)
            nextLine = f.readline().rstrip()
            books.append(sorted([int(bookId) for bookId in nextLine.split(' ')], key=lambda x: S[x], reverse=True))
    
    Nuniques = [0 for i in range(L)]
    for i in range(B):
        count = 0
        uniqueLib = -1
        for libIndex in range(L):
            if i in books[libIndex]:
                if count == 0:
                    count += 1
                    uniqueLib = libIndex
                else:
                    uniqueLib = -1
                    break
        if uniqueLib != -1:
            Nuniques[uniqueLib] += 1

def printData():
    global B, L, D, S, N, T, M, books
    print(B, L, D, S, N, T, M, books)

def writeOutput(path, A, libList):
    line1 = str(A)
    with open(path, 'w') as f:
        f.write(line1)
        f.write('\n')
        for lib in libList:
            index = lib[0]
            numBook = lib[1]
            signUpBooks = lib[2]
            line = str(index) + ' ' + str(numBook) + '\n'
            f.write(line)
            nextLine = ' '.join(str(book) for book in signUpBooks)
            f.write(nextLine)
            f.write('\n')

paths = [
    # 'a_example',
    # 'b_read_on', 
    # 'c_incunabula',
    # 'd_tough_choices', 
    # 'e_so_many_books', 
    'f_libraries_of_the_world'
    ]

def getScore(fakeIndex):
    actualIndex = indexes[fakeIndex]
    if daysLeft <= T[actualIndex]:
        return 0
    endIndex = min(N[actualIndex], (daysLeft-T[actualIndex])*M[actualIndex])
    total_score = sum([S[bookId] for bookId in books[fakeIndex][:endIndex]])
    # return total_score
    # return endIndex
    return total_score**1.2 * weights[actualIndex]

for PATH in paths:
    print('Doing PATH = ' + PATH)
    loadData(PATH+'.txt')

    libraryList = []
    daysLeft = D
    indexes = [i for i in range(L)]

    weights = [1/math.log(1+Nuniques[i])/T[i] * M[i]**0.8 for i in range(L)]

    while daysLeft > 0 and len(libraryList)<L:
        # print(daysLeft)
        scores = [getScore(fakeIndex) for fakeIndex in range(len(indexes))]
        fakeIndex = scores.index(max(scores))
        actualIndex = indexes[fakeIndex]
        daysLeft -= T[actualIndex]
        # print(sorted(scores, reverse = True)[:10])
        if daysLeft < 0:
            break
        nBooks = min(daysLeft*M[actualIndex], N[actualIndex])
        listBooks = books[fakeIndex][0:nBooks]
        if len(listBooks) == 0:
            continue
        books.pop(fakeIndex)
        indexes.pop(fakeIndex)
        books = [[bookId for bookId in bookIds if not bookId in listBooks] for bookIds in books]

        libraryList.append([actualIndex, len(listBooks), listBooks])

    writeOutput(PATH+'_extended_output.txt', len(libraryList), libraryList)


    print()