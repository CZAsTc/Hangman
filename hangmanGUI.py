import tkinter
import tkinter.messagebox
import tkinter.font
import random
import pyperclip


class HangmanGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")
        self.word_list_100 = ["a", "an"]
        self.word_list_1000 = ["apple", "banana"]
        self.word_list_10000 = ["python", "program"]
        self.word_list = self.word_list_10000
        self.original_word = ""
        self.secret_word = ""
        self.missed_letters = ""
        self.correct_letters = ""
        self.HANGMAN_PICS = ["""
  +----+
       |
       |
       |
      ===""", """      
  +----+
  0    |
       |
       |
      ===""", """      
  +----+
  0    |
  |    |
       |
      ===""", """      
  +----+
  0    |
 /|    |
       |
      ===""", """      
  +----+
  0    |
 /|\\   |
       |
      ===""", """      
  +----+
  0    |
 /|\\   |
 /     |
      ===""", """      
  +----+
  0    |
 /|\\   |
 / \\   |
      ==="""]

        self.label = tkinter.Label(self.master, text="H A N G M A N", font=("Helvetica", 20, "bold"), fg="blue")
        self.difficulty_label = tkinter.Label(self.master, text="请选择难度：", font=("Helvetica", 16))
        self.difficulty_var = tkinter.StringVar()
        self.difficulty_menu = tkinter.OptionMenu(self.master, self.difficulty_var, "简单（100词）", "普通（1000词）", "困难（10000词）")
        self.start_buttons_frame = tkinter.Frame(self.master)
        self.start_button = tkinter.Button(self.start_buttons_frame, text="开始游戏", command=self.start_game, font=("Helvetica", 14), bg="green", fg="white", activebackground="green", activeforeground="white")
        self.end_button = tkinter.Button(self.start_buttons_frame, text="结束游戏", command=self.confirm_end_game, font=("Helvetica", 14), bg="red", fg="white", activebackground="red", activeforeground="white")
        self.buttons_frame = tkinter.Frame(self.master)
        self.guess_button = tkinter.Button(self.buttons_frame, text="确定", command=self.make_guess, font=("Helvetica", 14), bg="orange", fg="white", activebackground="green", activeforeground="white")
        self.copy_button = tkinter.Button(self.buttons_frame, text="复制单词", command=self.copy_word, font=("Helvetica", 14), fg="white", bg="blue", activebackground="green", activeforeground="white")
        self.canvas = tkinter.Canvas(self.master, width=400, height=300, bg="white")
        self.font = tkinter.font.Font(family="Courier New", size=16)
        self.message_label = tkinter.Label(self.master, text="", font=self.font)
        self.entry_label = tkinter.Label(self.master, text="猜一个字母：", font=("微软雅黑", 14))
        self.entry_var = tkinter.StringVar()
        self.entry = tkinter.Entry(self.master, textvariable=self.entry_var, font=self.font)
        self.create_widgets()

    def create_widgets(self):
        self.label.grid(row=0, column=0, columnspan=2, pady=10)
        self.difficulty_label.grid(row=1, column=0, columnspan=2)
        self.difficulty_var.set("困难（10000词）")
        self.difficulty_menu.grid(row=2, column=0, columnspan=2)
        self.start_buttons_frame.grid(row=3, column=0, columnspan=2, padx=10)
        self.start_button.pack(side="left", padx=10)
        self.end_button.pack(side="left", padx=10)
        self.canvas.grid(row=4, column=0, columnspan=2)
        self.message_label.grid(row=5, column=0, columnspan=2)
        self.entry_label.grid(row=6, column=0, columnspan=2)
        self.entry.grid(row=7, column=0, columnspan=2)
        button_frame_center_x = (self.master.winfo_reqwidth() - self.buttons_frame.winfo_reqwidth()) / 2
        self.buttons_frame.grid(row=8, column=0, columnspan=2, padx=button_frame_center_x)
        self.guess_button.pack(side="left", padx=10)
        self.copy_button.pack(side="left", padx=10)

    def start_game(self):
        selected_difficulty = self.difficulty_var.get()
        if selected_difficulty == "简单（100词）":
            self.word_list = self.word_list_100
        elif selected_difficulty == "普通（1000词）":
            self.word_list = self.word_list_1000
        elif selected_difficulty == "困难（10000词）":
            self.word_list = self.word_list_10000
        else:
            self.word_list = self.word_list_10000

        self.original_word = random.choice(self.word_list)
        self.secret_word = self.original_word.lower()
        self.missed_letters = ""
        self.correct_letters = ""
        self.update_display()

    def restart_game(self):
        self.original_word = random.choice(self.word_list)
        self.secret_word = self.original_word.lower()
        self.missed_letters = ""
        self.correct_letters = ""
        self.update_display()

    def confirm_end_game(self):
        response = tkinter.messagebox.askyesno("确认", "是否结束游戏？")
        if response:
            self.master.destroy()

    def update_display(self):
        self.canvas.delete("all")
        canvas_center_x = self.canvas.winfo_reqwidth() / 2
        self.canvas.create_text(canvas_center_x, 50, text=self.HANGMAN_PICS[len(self.missed_letters)], font=self.font, fill="black")
        self.canvas.create_text(canvas_center_x, 200, text=self.get_display_word(), font=self.font, tags="word", fill="black")
        self.message_label.config(text="")
        if self.is_game_over():
            if self.is_winner():
                self.message_label.config(text=f"恭喜，你猜对了！这个单词是 {self.original_word}。")
            else:
                self.message_label.config(text=f"游戏结束，正确的单词是 {self.original_word}。祝你下次好运。")

    def get_display_word(self):
        display_word = ""
        for letter in self.secret_word:
            if letter in self.correct_letters:
                display_word += letter + " "
            else:
                display_word += "_ "
        return display_word.strip()

    def is_game_over(self):
        return self.is_winner() or len(self.missed_letters) == len(self.HANGMAN_PICS) - 1

    def is_winner(self):
        return all(letter in self.correct_letters for letter in self.secret_word)

    def make_guess(self):
        guess = self.entry_var.get().lower()
        self.entry_var.set("")
        if guess and guess.isalpha():
            if guess in self.correct_letters or guess in self.missed_letters:
                tkinter.messagebox.showinfo("无效猜测", "你已经猜过这个字母了，请换一个。")
            else:
                if guess in self.secret_word:
                    self.correct_letters += guess
                else:
                    self.missed_letters += guess

                self.update_display()

                if self.is_game_over():
                    self.restart_game()
        else:
            tkinter.messagebox.showinfo("无效输入", "请输入有效的字母。")

    def copy_word(self):
        pyperclip.copy(self.secret_word)
        tkinter.messagebox.showinfo("复制成功", "已复制带下划线的单词到剪贴板。")


if __name__ == "__main__":
    root = tkinter.Tk()
    app = HangmanGUI(root)
    root.mainloop()
