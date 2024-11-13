import tkinter as tk
from tkinter import messagebox
import random

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game v1.2")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.grid = self.generate_puzzle()
        self.create_widgets()

    def generate_full_board(self):
        # Generate an empty 9x9 grid
        board = [[0 for _ in range(9)] for _ in range(9)]

        # Helper function to check if a number is valid
        def is_valid(num, row, col):
            for x in range(9):
                if board[row][x] == num or board[x][col] == num:
                    return False
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(3):
                for j in range(3):
                    if board[start_row + i][start_col + j] == num:
                        return False
            return True

        # Backtracking function to fill the board
        def fill_board():
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        numbers = list(range(1, 10))
                        random.shuffle(numbers)  # Shuffle numbers to add randomness
                        for num in numbers:
                            if is_valid(num, row, col):
                                board[row][col] = num
                                if fill_board():
                                    return True
                                board[row][col] = 0
                        return False
            return True

        fill_board()
        return board

    def generate_puzzle(self, num_holes=40):
        # Generate a complete Sudoku board
        board = self.generate_full_board()

        # Function to check if the board has a unique solution
        def has_unique_solution(board):
            # Simple solver to check if the puzzle has a unique solution
            def solve():
                for row in range(9):
                    for col in range(9):
                        if board[row][col] == 0:
                            for num in range(1, 10):
                                if self.is_valid_for_board(board, num, row, col):
                                    board[row][col] = num
                                    if solve():
                                        return True
                                    board[row][col] = 0
                            return False
                return True

            # Create a copy of the board for solving
            board_copy = [row[:] for row in board]
            return solve()

        # Randomly remove numbers to create holes in the puzzle
        holes = 0
        while holes < num_holes:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if board[row][col] != 0:
                temp = board[row][col]
                board[row][col] = 0
                if not has_unique_solution(board):
                    board[row][col] = temp
                else:
                    holes += 1
        return board

    def is_valid_for_board(self, board, num, row, col):
        # Validation logic for the given board
        for x in range(9):
            if board[row][x] == num or board[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def create_widgets(self):
        # Create a 9x9 grid of entry widgets
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=2, font=("Arial", 18), justify="center")
                if self.grid[row][col] != 0:
                    entry.insert(0, str(self.grid[row][col]))
                    entry.config(state="disabled")  # Make it read-only
                entry.grid(row=row, column=col, padx=5, pady=5)
                self.entries[row][col] = entry

        # Add a button to check the solution
        check_button = tk.Button(self.root, text="Check Solution", command=self.check_solution)
        check_button.grid(row=10, column=0, columnspan=9, pady=10)

    def check_solution(self):
        try:
            for row in range(9):
                for col in range(9):
                    if self.grid[row][col] == 0:
                        value = int(self.entries[row][col].get())
                        if not (1 <= value <= 9) or not self.is_valid(row, col, value):
                            raise ValueError("Invalid number or placement")
            messagebox.showinfo("Sudoku", "Congratulations! You solved the puzzle!")
        except ValueError:
            messagebox.showerror("Error", "Invalid number or placement. Please try again.")

    def is_valid(self, row, col, num):
        # Validation logic for checking user input
        for x in range(9):
            if x != col and int(self.entries[row][x].get() or 0) == num:
                return False
        for x in range(9):
            if x != row and int(self.entries[x][col].get() or 0) == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if (start_row + i != row or start_col + j != col) and \
                        int(self.entries[start_row + i][start_col + j].get() or 0) == num:
                    return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()