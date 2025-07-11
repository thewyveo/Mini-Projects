# ngl this is pretty messy code. it's just code that's built on solving problems that arise
# rather than optimizing a global solution. either way, the create_sudoku function creates a sudoku
# board from scratch with blanks in between; making sure that there are no horizontal or vertical conflicts.

import random

def create_and_solve_sudoku():
    # function to create the sudoku puzzle
    def grids():
        board = [[0 for _ in range(9)] for _ in range(9)]

        def is_valid(board, row, col, num):
            for i in range(9):
                if board[row][i] == num or board[i][col] == num:
                    return False
            box_row = (row // 3) * 3
            box_col = (col // 3) * 3
            for i in range(3):
                for j in range(3):
                    if board[box_row + i][box_col + j] == num:
                        return False
            return True

        # helper function to fill the board
        def fill_board(board):
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        nums = list(range(1, 10))
                        random.shuffle(nums)
                        for num in nums:
                            if is_valid(board, row, col, num):
                                board[row][col] = num
                                if fill_board(board):
                                    return True
                                board[row][col] = 0
                        return False
            return True

        fill_board(board)

        # helper function to remove random cells to turn the grid into a puzzle
        for _ in range(random.randint(40, 50)):
            r, c = random.randint(0, 8), random.randint(0, 8)
            board[r][c] = 0

        return board

    # function to conceptualize the board and turn into human-understandable format
    def conceptualize(grid):
        all_rows = []
        for row in grid:
            visual_row = ''.join(str(row))
            visual_row2 = []
            for x in visual_row.split(','):
                if int(x.strip().strip('[').strip(']')) == 0:
                    element = ' '
                else:
                    element = x.strip()
                visual_row2.append(element.strip('[').strip(']'))
            visual_row2.insert(0, '|')
            visual_row2.insert(4, '|')
            visual_row2.insert(8, '|')
            visual_row2.insert(12, '|')
            all_rows.append(visual_row2)
        all_rows.insert(0, '-------------')
        all_rows.insert(4, '-------------')
        all_rows.insert(8, '-------------')
        all_rows.insert(12, '-------------')
        return all_rows

    # function to parse the human format into machine-understandable format
    def parse(visualization):
        boxes = [[] for _ in range(9)]
        visual_row_idx = 0
        for row in visualization:
            if isinstance(row, str) or '-' in row:
                continue
            for j in range(len(row)):
                if row[j] == '|':
                    continue
                box_row = visual_row_idx // 3
                box_col = (j - (j // 4 + 1)) // 3
                box_index = box_row * 3 + box_col
                val = row[j]
                num = 0 if val == ' ' else int(val)
                boxes[box_index].append(num)
            visual_row_idx += 1
        return boxes

    # helper function to convert 3x3 boxes back to grid format
    def boxes_to_grid(boxes):
        grid = [[0 for _ in range(9)] for _ in range(9)]
        for b in range(9):
            start_row = (b // 3) * 3
            start_col = (b % 3) * 3
            for i in range(3):
                for j in range(3):
                    grid[start_row + i][start_col + j] = boxes[b][i * 3 + j]
        return grid
    
    # helper function to convert grid to 3x3 boxes format
    def grid_to_boxes(grid):
            boxes = [[] for _ in range(9)]
            for i in range(9):
                for j in range(9):
                    box_idx = (i // 3) * 3 + (j // 3)
                    boxes[box_idx].append(grid[i][j])
            return boxes

    grid = grids()
    visualization = conceptualize(grid)
    parsed = parse(visualization)
    grid = boxes_to_grid(parsed)

    # function to visualize the boxes from the human-readable format
    def visualize_boxes(boxes):
        grid = [[0 for _ in range(9)] for _ in range(9)]
        for b in range(9):
            start_row = (b // 3) * 3
            start_col = (b % 3) * 3
            for i in range(3):
                for j in range(3):
                    val = boxes[b][i * 3 + j]
                    grid[start_row + i][start_col + j] = val
        all_rows = []
        for row in grid:
            visual_row = []
            for i, val in enumerate(row):
                visual_row.append(' ' if val == 0 else str(val))
                if i in [2, 5]:
                    visual_row.append('|')
            all_rows.append(visual_row)
        all_rows.insert(0, ['-' for _ in range(11)])
        all_rows.insert(4, ['-' for _ in range(11)])
        all_rows.insert(8, ['-' for _ in range(11)])
        all_rows.insert(12, ['-' for _ in range(11)])
        for row in all_rows:
            print(' '.join(row))
    visualize_boxes(parsed)

    grid = boxes_to_grid(parsed)

    # helper functions to check for conflicts in the grid
    def horizontal_conflict(cell, number):
        row = cell[0]
        if number in grid[row]:
            return True
        else:
            return False
    def vertical_conflict(cell, number):
        col = cell[1]
        for row in range(9):
            if number == grid[row][col]:
                return True
        return False
    def box_conflict(cell, number):
        row, col = cell[0], cell[1]
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for r in range(3):
            for c in range(3):
                if number == grid[box_row+r][box_col+c]:
                    return True
        return False
    
    # helper function to find an empty cell in the grid
    def empty_cell():
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    return (row, col)
        return None

    # main recursive solving function to finish off the sudoku puzzle
    def solve():
        cell = empty_cell()
        if cell is None:
            return True
        
        row, col = cell
        for number in range(1, 10):
            if not horizontal_conflict((row, col), number) and not vertical_conflict((row, col), number) and not box_conflict((row, col), number):
                grid[row][col] = number

                if solve():
                    return True
                
                grid[row][col] = 0

        return False

    solve()
    solved_boxes = grid_to_boxes(grid)
    visualize_boxes(solved_boxes)

if __name__ == "__main__":
    create_and_solve_sudoku()