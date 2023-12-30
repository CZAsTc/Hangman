import tkinter as tk
from tkinter import messagebox, simpledialog
import tkinter.font as tkFont
import random

class HangmanGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")

        self.word_list_100 = ["a", "an"]  # Add more words as needed
        self.word_list_1000 = ["apple", "banana"]  # Add more words as needed
        self.word_list_10000 = ["programming", "python"]  # Add more words as needed

        self.word_list = self.word_list_10000  # Default to the hardest level

        self.original_word = ""
        self.secret_word = ""
        self.missed_letters = ''
        self.correct_letters = ''

        self.HANGMAN_PICS = ['''  +----+
       |
       |
       |
      ===''', '''      
  +----+
  0    |
       |
       |
      ===''', '''      
  +----+
  0    |
  |    |
       |
      ===''', '''      
  +----+
  0    |
 /|    |
       |
      ===''', '''      
  +----+
  0    |
 /|\\   |
       |
      ===''', '''      
  +----+
  0    |
 /|\\   |
 /     |
      ===''', '''      
  +----+
  0    |
 /|\\   |
 / \\   |
      ===''']

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="H A N G M A N", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.difficulty_label = tk.Label(self.master, text="请选择难度：", font=("Helvetica", 12))
        self.difficulty_label.pack()

        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("3")  # Default to the hardest level

        self.difficulty_menu = tk.OptionMenu(self.master, self.difficulty_var, "1", "2", "3")
        self.difficulty_menu.pack()

        self.start_button = tk.Button(self.master, text="开始游戏", command=self.start_game)
        self.start_button.pack()

        self.canvas = tk.Canvas(self.master, width=300, height=200)
        self.canvas.pack()

        # Use a fixed-width font for display
        self.font = tkFont.Font(family="Courier New", size=16)

        self.message_label = tk.Label(self.master, text="", font=self.font)
        self.message_label.pack()

        self.entry_label = tk.Label(self.master, text="猜一个字母：")
        self.entry_label.pack()

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.master, textvariable=self.entry_var, font=self.font)
        self.entry.pack()

        self.guess_button = tk.Button(self.master, text="猜", command=self.make_guess)
        self.guess_button.pack()

        self.restart_button = tk.Button(self.master, text="重新开始", command=self.restart_game)
        self.restart_button.pack()

        self.missed_letters_label = tk.Label(self.master, text="错误的字母：", font=self.font)
        self.missed_letters_label.pack()

        self.start_game()

    def start_game(self):
        selected_difficulty = self.difficulty_var.get()
        if selected_difficulty == "1":
            self.word_list = self.word_list_100
        elif selected_difficulty == "2":
            self.word_list = self.word_list_1000
        elif selected_difficulty == "3":
            self.word_list = self.word_list_10000
        else:
            self.word_list = self.word_list_10000  # 默认选择最困难的难度

        self.restart_game()

    def restart_game(self):
        self.original_word = random.choice(self.word_list)
        self.secret_word = self.original_word.lower()
        self.missed_letters = ''
        self.correct_letters = ''
        self.update_display()

    def update_display(self):
        self.canvas.delete("all")
        self.canvas.create_text(150, 50, text=self.HANGMAN_PICS[len(self.missed_letters)], font=self.font)
        self.canvas.create_text(150, 150, text=self.get_display_word(), font=self.font, tags="word")

        self.missed_letters_label.config(text=f"错误的字母： {', '.join(self.missed_letters)}", font=self.font)

        if self.is_game_over():
            if self.is_winner():
                messagebox.showinfo("恭喜！", f"你猜对了！这个单词是 {self.original_word}。")
            else:
                messagebox.showinfo("游戏结束", f"抱歉，正确的单词是 {self.original_word}。\n祝你下次好运。")

    def get_display_word(self):
        display_word = ''
        for letter in self.secret_word:
            if letter in self.correct_letters:
                display_word += letter + ' '
            else:
                display_word += '_ '
        return display_word.strip()

    def is_game_over(self):
        return self.is_winner() or len(self.missed_letters) == len(self.HANGMAN_PICS) - 1

    def is_winner(self):
        return all(letter in self.correct_letters for letter in self.secret_word)

    def make_guess(self):
        guess = self.entry_var.get().lower()
        self.entry_var.set('')  # Clear the entry after getting the guess
        if guess and guess.isalpha():
            if guess in self.correct_letters or guess in self.missed_letters:
                messagebox.showinfo("无效猜测", "你已经猜过这个字母了，请换一个。")
            else:
                if guess in self.secret_word:
                    self.correct_letters += guess
                else:
                    self.missed_letters += guess

                self.update_display()

                if self.is_game_over():
                    self.restart_game()
        else:
            messagebox.showinfo("无效输入", "请输入有效的字母。")

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()
