import tkinter as tk
from tkinter import messagebox

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.grid = [
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
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_widgets()

    def create_widgets(self):
        # Create a 9x9 grid of entry widgets
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] != 0:
                    # Initialize the Entry widget with the number and make it read-only
                    entry = tk.Entry(self.root, width=2, font=("Arial", 18), justify="center", state="normal")
                    entry.insert(0, str(self.grid[row][col]))
                    entry.config(state="disabled")  # Make the Entry read-only
                else:
                    # Create an empty Entry widget for user input
                    entry = tk.Entry(self.root, width=2, font=("Arial", 18), justify="center")
                entry.grid(row=row, column=col, padx=5, pady=5)
                self.entries[row][col] = entry

        # Add a button to check the solution
        check_button = tk.Button(self.root, text="Check Solution", command=self.check_solution)
        check_button.grid(row=9, column=0, columnspan=9, pady=10)

    def check_solution(self):
        try:
            # Retrieve and validate the user's input
            for row in range(9):
                for col in range(9):
                    if self.grid[row][col] == 0:  # Only check user-input cells
                        value = int(self.entries[row][col].get())
                        if not (1 <= value <= 9) or not self.is_valid(row, col, value):
                            raise ValueError("Invalid number or placement")

            messagebox.showinfo("Sudoku", "Congratulations! You solved the puzzle!")
        except ValueError:
            messagebox.showerror("Error", "Invalid number or placement. Please try again.")

    def is_valid(self, row, col, num):
        # Check the row
        for x in range(9):
            if x != col and int(self.entries[row][x].get() or 0) == num:
                return False

        # Check the column
        for x in range(9):
            if x != row and int(self.entries[x][col].get() or 0) == num:
                return False

        # Check the 3x3 subgrid
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
