import numpy as np
import copy
import time


def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """

    def search(sudoku, possibilities, zeroes):
        """
        Inner recursive function that chooses a random possibility and
        iterates through the possibilities, while updating the constraints.

        Input
            sudoku        : 9x9 numpy array
            possibilities : 9x9x9 numpy array
            zeroes        : array of zero locations

        Output
            9x9 numpy array of integers or None
                It contains the solution. If there is no solution, returns None.
        """

        # Evaluate the constraints
        for blank in copy.copy(zeroes):

            # No possibilities means that branch is not a correct solution
            if np.count_nonzero(possibilities[blank[0], blank[1]]) == 0:
                return None

            # If one possibility - assign it and update the constraints
            elif np.count_nonzero(possibilities[blank[0], blank[1]]) == 1:
                sudoku[blank[0], blank[1]] = sum(possibilities[blank[0], blank[1]])
                for zero in zeroes:
                    if zero == blank:
                        continue

                    # Check if zeroes belong in the same box and update the possibilities
                    if (blank[0] // 3 * 3) == (zero[0] // 3 * 3) \
                            and (blank[1] // 3 * 3 + 3) == (zero[1] // 3 * 3 + 3):
                        possibilities[zero[0]][zero[1]][sudoku[blank[0], blank[1]] - 1] = 0

                    # Check if zeroes belong in the same row or column and update the possibilities
                    if blank[0] == zero[0] or blank[1] == zero[1]:
                        possibilities[zero[0]][zero[1]][sudoku[blank[0], blank[1]] - 1] = 0
                zeroes.remove(blank)

        # If no zeroes left, we reached a solution
        if len(zeroes) == 0:
            return sudoku

        # Assign a random possibility and call self
        blank = zeroes[0]
        for possibility in copy.deepcopy(possibilities)[blank[0], blank[1]]:
            if possibility == 0:
                continue

            # Assign a random possibility to the grid
            sudoku[blank[0], blank[1]] = possibility

            # Creating backups in case that branch does not have a solution
            cache1 = copy.deepcopy(possibilities)
            cache2 = copy.copy(zeroes)

            # Assuming that the possibility is correct - removing all other possibilities
            possibilities[blank[0], blank[1]] = np.zeros((9,), dtype=int)
            possibilities[blank[0], blank[1]][possibility - 1] = possibility
            zeroes.remove(blank)

            # Update the constraints
            for zero in zeroes:
                # Check if zeroes belong in the same box and update the possibilities
                if (blank[0] // 3 * 3) == (zero[0] // 3 * 3) \
                        and (blank[1] // 3 * 3 + 3) == (zero[1] // 3 * 3 + 3):
                    possibilities[zero[0]][zero[1]][possibility - 1] = 0

                # Check if zeroes belong in the same row or column and update the possibilities
                elif blank[0] == zero[0] or blank[1] == zero[1]:
                    possibilities[zero[0]][zero[1]][possibility - 1] = 0

            # Recursive call
            solution = search(sudoku, possibilities, zeroes)

            # If the results are invalid, assign the values back and move to the next iteration
            if solution is None:
                sudoku[blank[0], blank[1]] = 0
                possibilities = cache1
                zeroes = cache2
            else:
                return solution

        # If all possibilities had been tried and the algorithm didn't reach any solution, the solution doesn't exist
        return None

    # Check if input is a valid sudoku
    # Scan rows
    for row in sudoku:
        # Filtering out zeroes from input
        filtered_row = np.array([cell for cell in row if cell != 0])

        # Checking if the row consists of only unique values
        if len(filtered_row) != len(np.unique(filtered_row)):
            # If it doesn't, the sudoku is wrong
            return np.full((9, 9), -1)

    # Scan columns
    for column in np.transpose(sudoku):
        filtered_column = np.array([cell for cell in column if cell != 0])
        if len(filtered_column) != len(np.unique(filtered_column)):
            return np.full((9, 9), -1)

    # Scan boxes
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            box = sudoku[i:i + 3, j:j + 3].flatten()
            filtered_box = np.array([cell for cell in box if cell != 0])
            if len(filtered_box) != len(np.unique(filtered_box)):
                return np.full((9, 9), -1)

    baseDomain = np.array([i for i in range(1, 10)], dtype=int)  # Number of the cell
    possibilities = np.zeros((9, 9, 9), dtype=int)
    zeroes = []

    # Create an array of possibilities (empty cells * domain)
    for i in range(0, 9):
        for j in range(0, 9):
            if sudoku[i][j] != 0:
                # Solved cells have only one possible value
                possibilities[i][j][0] = sudoku[i][j]
            else:
                # Unsolved cells are initiated with all 9 values assigned
                possibilities[i][j] = baseDomain

    # Evaluate constraints
    for i in range(0, 9):
        for j in range(0, 9):
            if sudoku[i, j] == 0:
                # Cross out values (turn into 0) that are already taken

                # Scan the columns
                for value in sudoku[:, j]:
                    if value in possibilities[i][j] and value != 0:
                        possibilities[i][j][value - 1] = 0

                # Scan the rows
                for value in sudoku[i, :]:
                    if value in possibilities[i][j] and value != 0:
                        possibilities[i][j][value - 1] = 0

                # Scan the box
                for box_row in sudoku[i // 3 * 3: i // 3 * 3 + 3,
                               j // 3 * 3: j // 3 * 3 + 3]:
                    for value in box_row:
                        if value in possibilities[i][j] and value != 0:
                            possibilities[i][j][value - 1] = 0

                # save the coordinates of that cell for future reference
                zeroes.append((i, j))

    # Eliminate the blanks with just one possibility
    for blank in copy.copy(zeroes):

        # If no possibility - sudoku is invalid
        if np.count_nonzero(possibilities[blank[0], blank[1]]) == 0:
            return np.full((9, 9), -1)

        # If one possibility - assign it and update the constraints
        elif np.count_nonzero(possibilities[blank[0], blank[1]]) == 1:
            sudoku[blank[0], blank[1]] = sum(possibilities[blank[0], blank[1]])
            for zero in zeroes:
                if zero == blank:
                    continue

                # Check if zeroes belong in the same box and update the possibilities
                if (blank[0] // 3 * 3) == (zero[0] // 3 * 3) \
                        and (blank[1] // 3 * 3 + 3) == (zero[1] // 3 * 3 + 3):
                    possibilities[zero[0]][zero[1]][sudoku[blank[0], blank[1]] - 1] = 0

                # Check if zeroes belong in the same row or column and update the possibilities
                elif blank[0] == zero[0] or blank[1] == zero[1]:
                    possibilities[zero[0]][zero[1]][sudoku[blank[0], blank[1]] - 1] = 0
            zeroes.remove(blank)

    # Call the search backtracking algorithm
    sudoku = search(sudoku, possibilities, zeroes)

    if sudoku is None:
        return np.full((9, 9), -1)
    else:
        return sudoku


sudoku = np.load("data/hard_puzzle.npy")
puzzle_index = 14
start_time = time.process_time()
solved_sudoku = sudoku_solver(sudoku[puzzle_index])
end_time = time.process_time()
print(solved_sudoku)
print(np.array_equal(np.load("data/hard_solution.npy")[puzzle_index], solved_sudoku))
print("This sudoku took", end_time - start_time, "seconds to solve.\n")
