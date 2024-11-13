import tkinter as tk
from tkinter import messagebox
import random

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game v1.1")
        self.difficulty = "easy"  # Default difficulty
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.grid = self.select_puzzle(self.difficulty)
        self.create_widgets()

    def select_puzzle(self, difficulty):
        # Sample puzzles for each difficulty
        easy_puzzles = [
            [
                [5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]
            ]
        ]

        # Add medium and hard puzzles if needed
        medium_puzzles = [
            # Example medium puzzles
        ]
        hard_puzzles = [
            # Example hard puzzles
        ]

        if difficulty == "easy":
            return random.choice(easy_puzzles)
        elif difficulty == "medium":
            return random.choice(medium_puzzles)
        elif difficulty == "hard":
            return random.choice(hard_puzzles)

    def create_widgets(self):
        # Difficulty selection buttons
        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.grid(row=0, column=0, columnspan=9, pady=10)

        tk.Button(difficulty_frame, text="Easy", command=lambda: self.change_difficulty("easy")).pack(side="left")
        tk.Button(difficulty_frame, text="Medium", command=lambda: self.change_difficulty("medium")).pack(side="left")
        tk.Button(difficulty_frame, text="Hard", command=lambda: self.change_difficulty("hard")).pack(side="left")

        # Create a 9x9 grid of entry widgets
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=2, font=("Arial", 18), justify="center")
                if self.grid[row][col] != 0:
                    entry.insert(0, str(self.grid[row][col]))
                    entry.config(state="disabled")  # Make it read-only
                entry.grid(row=row + 1, column=col, padx=5, pady=5)
                self.entries[row][col] = entry

        # Add a button to check the solution
        check_button = tk.Button(self.root, text="Check Solution", command=self.check_solution)
        check_button.grid(row=10, column=0, columnspan=9, pady=10)

    def change_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.grid = self.select_puzzle(difficulty)
        self.update_grid()

    def update_grid(self):
        # Clear and update the grid with the new puzzle
        for row in range(9):
            for col in range(9):
                self.entries[row][col].config(state="normal")  # Enable all entries
                self.entries[row][col].delete(0, "end")  # Clear existing content
                if self.grid[row][col] != 0:
                    self.entries[row][col].insert(0, str(self.grid[row][col]))
                    self.entries[row][col].config(state="disabled")  # Make it read-only
                else:
                    self.entries[row][col].delete(0, "end")

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
        # Validation logic (same as before)
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