import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import random
import json
import time
import os
from datetime import datetime

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game v1.5")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.full_board = self.generate_full_board()
        self.difficulty = "easy"  # Default difficulty
        self.grid = self.remove_numbers_to_create_puzzle(self.full_board)
        self.undo_stack = []  # Stack to store moves for undo
        self.redo_stack = []  # Stack to store moves for redo
        self.start_time = time.time()  # Start the timer
        self.create_widgets()

    def generate_full_board(self):
        board = [[0 for _ in range(9)] for _ in range(9)]

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

        def fill_board():
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        numbers = list(range(1, 10))
                        random.shuffle(numbers)
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

    def remove_numbers_to_create_puzzle(self, board):
        num_holes = {
            "easy": 30,
            "medium": 40,
            "hard": 50
        }[self.difficulty]

        puzzle = [row[:] for row in board]
        holes = 0
        while holes < num_holes:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if puzzle[row][col] != 0:
                puzzle[row][col] = 0
                holes += 1

        return puzzle

    def create_widgets(self):
        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.grid(row=0, column=0, columnspan=9, pady=10)

        tk.Button(difficulty_frame, text="Easy", command=lambda: self.set_difficulty("easy")).pack(side="left")
        tk.Button(difficulty_frame, text="Medium", command=lambda: self.set_difficulty("medium")).pack(side="left")
        tk.Button(difficulty_frame, text="Hard", command=lambda: self.set_difficulty("hard")).pack(side="left")

        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=2, font=("Arial", 18), justify="center")
                if self.grid[row][col] != 0:
                    entry.insert(0, str(self.grid[row][col]))
                    entry.config(state="disabled")
                else:
                    entry.bind("<FocusOut>", lambda event, r=row, c=col: self.validate_entry(event, r, c))
                entry.grid(row=row + 1, column=col, padx=5, pady=5)
                self.entries[row][col] = entry

        check_button = tk.Button(self.root, text="Check Solution", command=self.check_solution)
        check_button.grid(row=10, column=0, columnspan=4, pady=10)

        hint_button = tk.Button(self.root, text="Get Hint", command=self.give_hint)
        hint_button.grid(row=10, column=5, columnspan=4, pady=10)

        undo_button = tk.Button(self.root, text="Undo", command=self.undo_move)
        undo_button.grid(row=11, column=0, columnspan=4, pady=10)

        redo_button = tk.Button(self.root, text="Redo", command=self.redo_move)
        redo_button.grid(row=11, column=5, columnspan=4, pady=10)

        save_button = tk.Button(self.root, text="Save Game", command=self.save_game)
        save_button.grid(row=12, column=0, columnspan=4, pady=10)

        load_button = tk.Button(self.root, text="Load Game", command=self.load_game)
        load_button.grid(row=12, column=5, columnspan=4, pady=10)

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.grid = self.remove_numbers_to_create_puzzle(self.full_board)
        self.update_grid()

    def update_grid(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].config(state="normal")
                self.entries[row][col].delete(0, "end")
                if self.grid[row][col] != 0:
                    self.entries[row][col].insert(0, str(self.grid[row][col]))
                    self.entries[row][col].config(state="disabled")

    def validate_entry(self, event, row, col):
        try:
            value = self.entries[row][col].get()
            if value:
                self.undo_stack.append((row, col, self.entries[row][col].get()))
                self.redo_stack.clear()

            if int(value) != self.full_board[row][col]:
                self.entries[row][col].config(fg="orange")
            else:
                self.entries[row][col].config(fg="black")
        except ValueError:
            self.entries[row][col].config(fg="orange")

    def give_hint(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0 and self.entries[row][col].get() == "":
                    self.entries[row][col].insert(0, str(self.full_board[row][col]))
                    self.entries[row][col].config(state="disabled")
                    return

    def undo_move(self):
        if self.undo_stack:
            row, col, value = self.undo_stack.pop()
            self.redo_stack.append((row, col, self.entries[row][col].get()))
            self.entries[row][col].delete(0, "end")
            self.entries[row][col].insert(0, value)
            self.entries[row][col].config(fg="black")

    def redo_move(self):
        if self.redo_stack:
            row, col, value = self.redo_stack.pop()
            self.undo_stack.append((row, col, self.entries[row][col].get()))
            self.entries[row][col].delete(0, "end")
            self.entries[row][col].insert(0, value)
            self.entries[row][col].config(fg="black")

    def generate_file_name(self):
        return datetime.now().strftime("%Y%m%d_%I.%M%p") + ".json"

    def save_to_json(self, data, folder="saves"):
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_name = os.path.join(folder, self.generate_file_name())
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)
        return file_name

    def load_from_json(self, file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            return None

    def save_game(self):
        data = {
            "grid": self.grid,
            "undo_stack": self.undo_stack,
            "redo_stack": self.redo_stack,
            "elapsed_time": time.time() - self.start_time,
        }
        file_name = self.save_to_json(data)
        messagebox.showinfo("Sudoku", f"Game saved successfully as {file_name}!")

    def get_save_file_path(self):
        return askopenfilename(
            title="Select Saved Game",
            filetypes=[("JSON Files", "*.json")],
            initialdir="saves"
        )

    def load_game(self):
        file_path = self.get_save_file_path()
        if not file_path:
            return

        data = self.load_from_json(file_path)
        if data:
            self.grid = data["grid"]
            self.undo_stack = data["undo_stack"]
            self.redo_stack = data["redo_stack"]
            self.start_time = time.time() - data["elapsed_time"]
            self.update_grid()
            messagebox.showinfo("Sudoku", "Game loaded successfully!")
        else:
            messagebox.showerror("Error", "Failed to load game. The file might be corrupted or missing.")

    def check_solution(self):
        try:
            for row in range(9):
                for col in range(9):
                    if self.grid[row][col] == 0:
                        value = int(self.entries[row][col].get())
                        if not (1 <= value <= 9) or not self.is_valid(row, col, value):
                            raise ValueError("Invalid number or placement")
            score = self.calculate_score()
            messagebox.showinfo("Sudoku", f"Congratulations! You solved the puzzle! Your score: {score}")
        except ValueError:
            messagebox.showerror("Error", "Invalid number or placement. Please try again.")

    def calculate_score(self):
        elapsed_time = time.time() - self.start_time
        hints_used = len(self.undo_stack)
        score = max(1000 - int(elapsed_time) - (hints_used * 10), 0)
        return score

    def is_valid(self, row, col, num):
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
