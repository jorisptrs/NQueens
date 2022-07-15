import sys
import random
import math # exp()

MAXQ = 100

"""
------------------ Problem Helpers ------------------
"""

def in_conflict(column, row, other_column, other_row):
    """
    Checks if two locations are in conflict with each other.
    :param column: Column of queen 1.
    :param row: Row of queen 1.
    :param other_column: Column of queen 2.
    :param other_row: Row of queen 2.
    :return: True if the queens are in conflict, else False.
    """
    if column == other_column:
        return True  # Same column
    if row == other_row:
        return True  # Same row
    if abs(column - other_column) == abs(row - other_row):
        return True  # Diagonal

    return False


def in_conflict_with_another_queen(row, column, board):
    """
    Checks if the given row and column correspond to a queen that is in conflict with another queen.
    :param row: Row of the queen to be checked.
    :param column: Column of the queen to be checked.
    :param board: Board with all the queens.
    :return: True if the queen is in conflict, else False.
    """
    for other_column, other_row in enumerate(board):
        if in_conflict(column, row, other_column, other_row):
            if row != other_row or column != other_column:
                return True
    return False


def count_conflicts(board):
    """
    Counts the number of queens in conflict with each other.
    :param board: The board with all the queens on it.
    :return: The number of conflicts.
    """
    cnt = 0

    for queen in range(0, len(board)):
        for other_queen in range(queen+1, len(board)):
            if in_conflict(queen, board[queen], other_queen, board[other_queen]):
                cnt += 1

    return cnt


def evaluate_state(board):
    """
    Evaluation function. The maximal number of queens in conflict can be 1 + 2 + 3 + 4 + .. +
    (nquees-1) = (nqueens-1)*nqueens/2. Since we want to do ascending local searches, the evaluation function returns
    (nqueens-1)*nqueens/2 - countConflicts().

    :param board: list/array representation of columns and the row of the queen on that column
    :return: evaluation score
    """
    return (len(board)-1)*len(board)/2 - count_conflicts(board)


def print_board(board):
    """
    Prints the board in a human readable format in the terminal.
    :param board: The board with all the queens.
    """
    print("\n")

    for row in range(len(board)):
        line = ''
        for column in range(len(board)):
            if board[column] == row:
                line += 'Q' if in_conflict_with_another_queen(row, column, board) else 'q'
            else:
                line += '.'
        print(line)


def init_board(nqueens):
    """
    :param nqueens integer for the number of queens on the board
    :returns list/array representation of columns and the row of the queen on that column
    """

    board = []

    for _ in range(nqueens):
        board.append(random.randint(0, nqueens-1))

    return board


"""
------------------ Search ------------------
"""


def random_search(board):
    """
    This function is an example and not an efficient solution to the nqueens problem. What it essentially does is flip
    over the board and put all the queens on a random position.
    :param board: list/array representation of columns and the row of the queen on that column
    """

    i = 0
    optimum = (len(board) - 1) * len(board) / 2

    while evaluate_state(board) != optimum:
        i += 1
        print('iteration ' + str(i) + ': evaluation = ' + str(evaluate_state(board)))
        if i == 1000:  # Give up after 1000 tries.
            break

        for column, row in enumerate(board):  # For each column, place the queen in a random row
            board[column] = random.randint(0, len(board)-1)

    if evaluate_state(board) == optimum:
        print('Solved puzzle!')

    print('Final state is:')
    print_board(board)

# creates a copy and changes the state according to row and column
def neighbor(row, column, board):
    newBoard = board[:]
    newBoard[column] = row
    return newBoard

def hill_climbing(board):
    """
    Implement this yourself.
    :param board:
    :return:
    """
    i = sidewalks = 0
    optimum = (len(board) - 1) * len(board) / 2
    while evaluate_state(board) != optimum:
        i += 1
        print('iteration ' + str(i) + ': evaluation = ' + str(evaluate_state(board)))
        if i == 1000 or sidewalks == 50:  # Give up after 1000 tries or 50 sidewalks.
            break
        bestNeighbors = [board] # keeps track of the highest-valued neighbors
        bestNeighborValue = evaluate_state(board) #stores the value of the highest-valued neighbors
        for column, row in enumerate(board): # iterate through each possible neighbor state
            for newRow in range(len(board)):
                newNeighbor = neighbor(newRow, column, board)
                if newRow != row and evaluate_state(newNeighbor) > bestNeighborValue:
                    bestNeighbors = [newNeighbor] # overwrite list
                    bestNeighborValue = evaluate_state(newNeighbor)
                elif newRow != row and evaluate_state(newNeighbor) == bestNeighborValue:
                    bestNeighbors.append(newNeighbor)
        if bestNeighborValue == evaluate_state(board): # if at a plateau or shoulder
            sidewalks += 1
        else:
            sidewalks = 0
        board = bestNeighbors[random.randint(0, len(bestNeighbors) - 1)] # chose a best neighbor
    if evaluate_state(board) == optimum:
        print('Solved puzzle!')
    print('Final state is:')
    print_board(board)

def time_to_temperature(t):
    return 0.4 - t / 60000 - 1000 * (0.99 ** t) # linear version: 0.4-(t)/(60000)

def simulated_annealing(board):
    optimum = (len(board) - 1) * len(board) / 2
    t = 0
    while 1:
        print('iteration ' + str(t) + ': evaluation = ' + str(evaluate_state(board)))
        T = time_to_temperature(t)
        if T == 0 or evaluate_state(board) == optimum: # T == 0 at around 24000 iterations
            break
        next = neighbor(random.randint(0, len(board) - 1), random.randint(0, len(board) - 1), board)
        dE = evaluate_state(next) - evaluate_state(board)
        if dE > 0:
            board = next
        elif random.uniform(0, 1) < math.exp(dE/T):
            board = next
        t += 1
    if evaluate_state(board) == optimum:
        print('Solved puzzle!')
        return 1
    print('Final state is:')
    print_board(board)
    return 0

def random_selection(population, populationSize, optimum):
    p = []
    sum = 0
    for individual in population: # cumulative sum of fitnesses gets stored in p for each state
        currentFitness = evaluate_state(individual)
        sum += currentFitness
        p.append(sum)
    selector = random.randint(0, sum)
    for i, fitness in enumerate(p):
        if fitness >= selector: # when the corresponding section of p is found
            return population[i][:]

def crossover(mamaBoard, daddyBoard, boardSize):
    cuttingPoint = random.randint(0, boardSize - 1)
    return mamaBoard[:cuttingPoint] + daddyBoard[cuttingPoint:]

def mutate(board):
    returnBoard = board[:]
    returnBoard[random.randint(0, len(board) - 1)] = random.randint(0, len(board) - 1)
    if returnBoard == board: # make sure the mutation led to a change
        return mutate(board)
    return returnBoard

def genetic_algorithm(population):
    boardSize = len(population[0])
    optimum = (boardSize - 1) * boardSize / 2
    populationSize = len(population)
    sum = 0
    for individual in population:
        sum += evaluate_state(individual)
    for limit in range(2001): # give up at 2000 iterations
        print('iteration ' + str(limit) + ': mean evaluation = ' + str(sum / populationSize))
        sum = 0
        newPopulation = []
        for i in range(populationSize):
            mamaBoard = random_selection(population, populationSize, optimum)
            daddyBoard = random_selection(population, populationSize, optimum)
            childBoard = crossover(mamaBoard, daddyBoard, boardSize)
            if evaluate_state(childBoard) == optimum: # if a solution was generated
                return 1
            sum += evaluate_state(childBoard) # for mean calculation
            if random.uniform(0, 1) < 0.07:
                childBoard = mutate(childBoard)
            newPopulation.append(childBoard)
        else:
            population = newPopulation[:]
            continue # continue the for loop only if the iteration was not broken prematurely
    print('Final state is:')
    print_board(childBoard)
    return 0


def main():
    """
    Main function that will parse input and call the appropriate algorithm. You do not need to understand everything
    here!
    """

    try:
        if len(sys.argv) != 2:
            raise ValueError

        n_queens = int(sys.argv[1])
        if n_queens < 1 or n_queens > MAXQ:
            raise ValueError

    except ValueError:
        print('Usage: python n_queens.py NUMBER')
        return False

    print('Which algorithm to use?')
    algorithm = input('1: random, 2: hill-climbing, 3: simulated annealing, 4: genetic algorithm\n')

    try:
        algorithm = int(algorithm)

        if algorithm not in range(1, 5):
            raise ValueError

    except ValueError:
        print('Please input a number in the given range!')
        return False
    
    board = init_board(n_queens)
    print('Initial board(s): \n')
    print_board(board)

    if algorithm == 1:
        random_search(board)
    if algorithm == 2:
        print_board(board)
        hill_climbing(board)
    if algorithm == 3:
        print_board(board)
        simulated_annealing(board)
    if algorithm == 4:
        # generate first population
        population = [board]
        populationSize = 50
        for _ in range(int(populationSize) - 1):
            population.append(init_board(n_queens))
        

# This line is the starting point of the program.
if __name__ == "__main__":
    main()
