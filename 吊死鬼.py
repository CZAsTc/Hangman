import random
import time
mode = input("""请选择难度
简单版（100词）请输入1
普通版（1000词）请输入2
困难版（10000词）请输入3
请输入：""")
if mode == "1":
    with open("100.txt") as f:
        word_list = eval(f.read())
elif mode == "2":
    with open("1000.txt") as f:
        word_list = eval(f.read())
elif mode == "3":
    with open("10000.txt") as f:
        word_list = eval(f.read())
else:
    print("已选择默认困难版")
    with open("10000.txt") as f:
        word_list = eval(f.read())
print(word_list)
original_word = random.choice(word_list)
HANGMAN_PICS = ['''
  +----+
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


def display_board(missed_letters, correct_letters, secret_word):
    print(HANGMAN_PICS[len(missed_letters)])
    time.sleep(1)
    print('错误的字母：', end='')
    for letter in missed_letters:
        print(letter, end=' ')
    print()
    blanks = '_' * len(secret_word)
    for i_1 in range(len(secret_word)):
        if secret_word[i_1].lower() in correct_letters:
            blanks = blanks[:i_1] + secret_word[i_1] + blanks[i_1 + 1:]
    for letter in blanks:
        print(letter, end=' ')
    print()


def get_guess(already_guessed):
    while True:
        guesses = input("猜一个字母：")
        guesses = guesses.lower()
        if len(guesses) != 1:
            print('一次不要写好几个单词！')
            time.sleep(1)
        elif guesses in already_guessed:
            print('你已经猜过了那个字母了，换一个猜！')
            time.sleep(1)
        elif guesses not in 'abcdefghijklmnopqrstuvwxyz':
            print('请写正常的字母！')
            time.sleep(1)
        else:
            return guesses


print('H A N G M A N')
print("游戏开始!")
time.sleep(2)
missedLetters = ''
correctLetters = ''
secretWord = original_word
gameIsDone = False
while True:
    display_board(missedLetters, correctLetters, secretWord)
    guess = get_guess(missedLetters + correctLetters)
    if guess in secretWord.lower():
        correctLetters = correctLetters + guess
        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i].lower() not in correctLetters:
                foundAllLetters = False
                break
        if foundAllLetters:
            print("对了！这个单词就是" + original_word + "，你赢了！")
            gameIsDone = True
    else:
        missedLetters = missedLetters + guess
        if len(missedLetters) == len(HANGMAN_PICS) - 1:
            display_board(missedLetters, correctLetters, secretWord)
            print("你没有猜出来！\n", f"这个词是{original_word}")
            gameIsDone = True
    if gameIsDone:
        time.sleep(3)
        break