from tkinter import *
import customtkinter
import random
import time
from PIL import Image, ImageTk
import pygame



#OPEN SOURCE CODE by Furuuti Ryota & Nishimoto Hikari
#This code was created by the above listed individuals

#Used "CustomTkinter" Library by Tom Schimansky is licensed under CC0 1.0



window = customtkinter.CTk()
customtkinter.set_appearance_mode("Dark")

window.title('エネスク')
window.geometry("1920x1080+10+20")
window.attributes('-fullscreen', True)


#                            _
#            ,---.          U
#           ;     \         ;
#       .==\"/==.  `-.___.-'
#      ((+) .  .:)
#      |`.-(o)-.'|
#      \/  \_/  \/              Coding Time 25h+ ...help


#-----------------------------------------------------------------------------------------------------------------------


# ============ Loading Sounds ============

pygame.mixer.init()

pygame.mixer.music.load("sounds/enesqu_bgm.mp3")

place = pygame.mixer.Sound('sounds/place.wav')
finish = pygame.mixer.Sound('sounds/win.wav')
input_false = pygame.mixer.Sound('sounds/wrong.wav')
mahoujin_start_sound = pygame.mixer.Sound('sounds/start.wav')

place.set_volume(1)
finish.set_volume(1)
input_false.set_volume(1)
mahoujin_start_sound.set_volume(0.5)


# ============ Defining some Colors ============

text_color = ("#4a9147", "#5fb55c")
text_color_disabled = ("black", "white")
text_color_disabled_light = ("#171717", "#f0f0f0")
fg_color_entry = ("#b5b5b5", "#18181a")
fg_color_entry2 = ("#9e9e9e", "#353537")

Ranking = ["#ffd700", "#00ffe5", "#00ff1e", "#ad633e"]



# ============ Global Variables ============

_3x3_key_matrix = [
    "a1", "b1", "c1",

    "d1", "e1", "f1",

    "g1", "h1", "i1"
]

_3x3_selected_entry_index = 4

_3x3_second=StringVar()

place_sound = True

animation_finish = [["e"],["b","d","f","h"],["a","c","g","i"]]
counter_animation = 0

_3x3_backup = [[6,1,8,7,5,3,2,9,4],[2,7,6,9,5,1,4,3,8],
                      [4,9,2,3,5,7,8,1,6],[8,3,4,1,5,9,6,7,2],
                      [8,1,6,3,5,7,4,9,2],[6,7,2,1,5,9,8,3,4],
                      [2,9,4,7,5,3,6,1,8],[4,3,8,9,5,1,2,7,6]]

_3x3_possible_mahoujins = _3x3_backup


_4x4_hints = [[12, 0, 1, 5,
           7, 0, 0, 0,
           0,13, 0, 0,
           6, 0,15, 0],
         [0,13,8, 0,
          0, 6, 0, 10,
          2, 0, 14, 15,
          16, 12, 0, 0],
         [9, 12, 0, 0,
          0, 1, 16, 0,
          0, 6, 0, 10,
          0, 0, 2, 13],
         [10, 0, 12, 0,
          0, 4, 0, 2,
          8, 0, 0, 11,
          0, 0, 1, 0],
         [10, 0, 0, 7,
          0, 0, 4, 16,
          0, 15, 14, 0,
          0, 12, 0, 0],
         [0, 0, 15, 6,
          7, 0, 0, 1,
          10, 0, 0, 0,
          0, 8, 2, 0],
         [0, 0, 11, 0,
          3, 15, 0, 0,
          16, 0, 0, 13,
          0, 5, 0, 0],
         [0, 0, 12, 8,
          4, 16, 0, 0,
          0, 3, 2, 0,
          0, 0, 7, 11],
         [16, 0, 0, 1,
          2, 0, 0, 0,
          0, 14, 3, 0,
          7, 11, 0, 0],
         [0, 0, 7, 13,
          5, 15, 0, 0,
          11, 0, 0, 8,
          0, 6, 9, 0],
         [5, 2, 16, 11,
          0, 0, 0, 1,
          0, 0, 3, 0,
          4, 7, 0, 0],
         [0, 15, 0, 0,
          7, 0, 0, 9,
          14, 0, 5, 0,
          0, 2, 0, 13],
         [0, 0, 0, 9,
          5, 0, 2, 11,
          12, 0, 3, 0,
          0, 1, 0, 0]]


_3x3_mahoujinindex = 0
_3x3_backup2 = []

music_on = False
sound_on = True

_3x3_timer_counter = 0
_3x3_timer_running = False

_3x3_index_for_chosen_mahoujin = []


_3x3_start_timer = 0
_3x3_stopwatch = 0




# ============ Checking Validity of Input ============
pygame.init()

_3x3_used_numbers = []

def _3x3_validate(P):
    global _3x3_key_matrix, _3x3_index_for_chosen_mahoujin
    if len(P) == 0:
        # empty Entry is ok
        return True
    elif len(P) == 1 and str(P) != "0" and P.isdigit() and not P in _3x3_used_numbers:
        if int(P) > 0:
            if place_sound:
                place.play()
        return True
        # Entry with 1 digit is ok

    else:
        # Anything else, reject it
        return False


_3x3_vcmd = (window.register(_3x3_validate), '%P')

def _4x4_validate(P):
    if len(P) == 0:
        # empty Entry is ok
        return True
    elif P.isdigit() and int(P) <= 16 and int(P) > 0:
        return True
    else:
        # Anything else, reject it
        return False
_4x4_vcmd = (window.register(_4x4_validate), '%P')


# ============ Functions ============

def change_mahoujin_mode(str_desire):
    if str_desire == "3x3":
        _4x4_mahoujin_frame.grid_remove()
        _4x4_insert.grid_remove()
        _3x3_mahoujin_frame.grid(row=0, column=0, pady=60, padx=30, sticky="e")
        difficulty_slider.grid(row=1, column=1, padx=0, pady=0, sticky="w")
        _3x3_show_hint.grid(row=3, column=0, columnspan=2, padx=20, pady=0, sticky="w")
        ranking.grid(row=2, column=0, rowspan=9,pady=40,padx=20, sticky="ns")
        difficulty.grid(row=1, column=0, padx=20, pady=0)
    elif str_desire == "4x4":
        _4x4_mahoujin_frame.grid(row=0, column=0, pady=60, padx=30, sticky="e")
        _4x4_insert.grid(row=2, column=0, columnspan=2, padx=10, pady=0)
        _3x3_mahoujin_frame.grid_remove()
        difficulty_slider.grid_remove()
        _3x3_show_hint.grid_remove()
        ranking.grid_remove()
        difficulty.grid_remove()

    else:
        pass



def quit_window():
    window.destroy()

def _3x3_show_tutorial(value):
    if value == 1:
        help = customtkinter.CTkTextbox(info_frame, text_font=("MS Mincho", 14),
                                        text_color=text_color_disabled_light, width=300, height=450,
                                        fg_color=fg_color_entry, corner_radius=0)

        help.tag_configure("bold", font="Mincho 14 bold", foreground=highlight)
        help.insert("end", "     \n")
        help.insert("end", "ゲームの説明\n", "bold")
        help.insert("end", "     \n")
        help.insert("end", "魔方陣とは〇×〇の正方形のマス目に数字を置いていき、縦、横、斜めのいずれにおいても、その列の合計が同じになるパズルである。\n", "")
        help.insert("end", "     \n")
        help.insert("end", "（その時使っていい数字は自然数であり各数字を入れられるのは一度だけです）\n", "")
        help.insert("end", "     \n")
        help.insert("end", "-------------------------------\n")
        help.insert("end", "     \n")
        help.insert("end", "アイコンの下にある")
        help.insert("end", "モードチェンジ", "bold")
        help.insert("end", "では3次魔方陣や４次魔法陣などモードの切り換えができる。\n")
        help.insert("end", "     \n")
        help.insert("end", "その下にある")
        help.insert("end", "カラーチェンジ", "bold")
        help.insert("end", "は黒と白の2色のモードの切り換えができます。\n")
        help.insert("end", "     \n")
        help.insert("end", "その下にある")
        help.insert("end", "タイマー", "bold")
        help.insert("end", "はスタートを押すことで自動的にタイムを測定し、終わったときのタイムを小数第2位まで出してくれます。\n")
        help.insert("end", "     \n")
        help.insert("end", "魔方陣に正解したときは")
        help.insert("end", "正解", "bold")
        help.insert("end", "と出て不正解だと")
        help.insert("end", "やり直し", "bold")
        help.insert("end", "と出て間違っているマスに赤色のエラーが出ます。\n")
        help.insert("end", "     \n")
        help.insert("end", "魔方陣の下にある")
        help.insert("end", "確認", "bold")
        help.insert("end", "は押すことで正解か不正解かを判定してくれます。")
        help.insert("end", "エンター", "bold")
        help.insert("end", "や")
        help.insert("end", "スペース", "bold")
        help.insert("end", "でも確認判定になるます。\n")
        help.insert("end", "     \n")
        help.insert("end", "説明の下にある")
        help.insert("end", "難易度のバー", "bold")
        help.insert("end", "は")
        help.insert("end", "簡単、普通、難しい", "bold")
        help.insert("end", "の三段階に分かれてます。\n")
        help.insert("end", "     \n")
        help.insert("end", "その下にある")
        help.insert("end", "スタート", "bold")
        help.insert("end", "は文字通り押すと開始されます。")
        help.insert("end", "シフト", "bold")
        help.insert("end", "でも同じ扱いになります。\n")
        help.insert("end", "     \n")
        help.insert("end", "説明の右隣りにある")
        help.insert("end", "スコア値", "bold")
        help.insert("end", "難易度に応じて目標タイムが設定され、")
        help.insert("end", "プロ、１級、２級、３級", "bold")
        help.insert("end", "の４段階に分かれています。上を目指して頑張ろう。\n")
        help.insert("end", "     \n")
        help.insert("end", "     \n")
        help.insert("end","3x3魔方陣のヒント\n","bold")
        help.insert("end", "1. 縦、横、斜め、どこを足しても")
        help.insert("end", "　15\n", "bold")
        help.insert("end", "\n")
        help.insert("end", "　　⬜⬜⬜ → 15\n")
        help.insert("end", "　　⬜⬜⬜ → 15\n")
        help.insert("end", "　　⬜⬜⬜ → 15\n")
        help.insert("end", "　　↓ ↓ ↓ ↘\n ")
        help.insert("end", "　15 15 15  15\n")
        help.insert("end", "\n")
        help.insert("end", "2. 中心は常に")
        help.insert("end", "5\n", "bold")
        help.insert("end", "\n")
        help.insert("end", "3. 角に入る数は")
        help.insert("end", "2,4,6,8の偶数\n　", "bold")
        help.insert("end", " 十字のマスに入る数は\n")
        help.insert("end", "   1,3,(5),7,9の奇数\n", "bold")
        help.insert("end", "\n")
        help.insert("end", "4. 答え\n")
        help.insert("end", "\n")
        help.insert("end", "　　2　7　6\n")
        help.insert("end", "　　9　5　1\n")
        help.insert("end", "　　4　3　8\n")
        help.insert("end", "   \n")
        help.insert("end", "   回転、鏡像は")
        help.insert("end", "可\n", "bold")
        help.insert("end", "   \n")
        help.insert("end", "   \n")
        help.insert("end", "(栃木県立小山高等学校\n")
        help.insert("end", "数理科学科・課題研究\n")
        help.insert("end", "柳田先生・\n")
        help.insert("end", "古内　良汰、西本　光)\n")
        help.insert("end", "     \n")
        help.insert("end", "2023\n")
        help.configure(state="disabled")
        help.grid(row=0, column=1, columnspan=1, sticky="nswe")
        help.configure(yscrollcommand=help_textbox_scrollbar.set)
    else:
        help = customtkinter.CTkTextbox(info_frame, text_font=("MS Mincho", 14),
                                        text_color=text_color_disabled_light, width=300, height=450,
                                        fg_color=fg_color_entry, corner_radius=0)

        help.tag_configure("bold", font="Mincho 14 bold", foreground=highlight)
        help.insert("end", "     \n")
        help.insert("end", "ゲームの説明\n", "bold")
        help.insert("end", "     \n")
        help.insert("end", "魔方陣とは〇×〇の正方形のマス目に数字を置いていき、縦、横、斜めのいずれにおいても、その列の合計が同じになるパズルである。\n", "")
        help.insert("end", "     \n")
        help.insert("end", "（その時使っていい数字は自然数であり各数字を入れられるのは一度だけです）\n", "")
        help.insert("end", "     \n")
        help.insert("end", "-------------------------------\n")
        help.insert("end", "     \n")
        help.insert("end", "アイコンの下にある")
        help.insert("end", "モードチェンジ", "bold")
        help.insert("end", "では3次魔方陣や４次魔法陣などモードの切り換えができる。\n")
        help.insert("end", "     \n")
        help.insert("end", "その下にある")
        help.insert("end", "カラーチェンジ", "bold")
        help.insert("end", "は黒と白の2色のモードの切り換えができます。\n")
        help.insert("end", "     \n")
        help.insert("end", "その下にある")
        help.insert("end", "タイマー", "bold")
        help.insert("end", "はスタートを押すことで自動的にタイムを測定し、終わったときのタイムを小数第2位まで出してくれます。\n")
        help.insert("end", "     \n")
        help.insert("end", "魔方陣に正解したときは")
        help.insert("end", "正解", "bold")
        help.insert("end", "と出て不正解だと")
        help.insert("end", "やり直し", "bold")
        help.insert("end", "と出て間違っているマスに赤色のエラーが出ます。\n")
        help.insert("end", "     \n")
        help.insert("end", "魔方陣の下にある")
        help.insert("end", "確認", "bold")
        help.insert("end", "は押すことで正解か不正解かを判定してくれます。")
        help.insert("end", "エンター", "bold")
        help.insert("end", "や")
        help.insert("end", "スペース", "bold")
        help.insert("end", "でも確認判定になるます。\n")
        help.insert("end", "     \n")
        help.insert("end", "説明の下にある")
        help.insert("end", "難易度のバー", "bold")
        help.insert("end", "は")
        help.insert("end", "簡単、普通、難しい", "bold")
        help.insert("end", "の三段階に分かれてます。\n")
        help.insert("end", "     \n")
        help.insert("end", "その下にある")
        help.insert("end", "スタート", "bold")
        help.insert("end", "は文字通り押すと開始されます。")
        help.insert("end", "シフト", "bold")
        help.insert("end", "でも同じ扱いになります。\n")
        help.insert("end", "     \n")
        help.insert("end", "説明の右隣りにある")
        help.insert("end", "スコア値", "bold")
        help.insert("end", "難易度に応じて目標タイムが設定され、")
        help.insert("end", "プロ、１級、２級、３級", "bold")
        help.insert("end", "の４段階に分かれています。上を目指して頑張ろう。\n")
        help.insert("end", "     \n")
        help.insert("end", "     \n")
        help.insert("end", "(栃木県立小山高等学校\n")
        help.insert("end", "数理科学科・課題研究\n")
        help.insert("end", "柳田先生・\n")
        help.insert("end", "古内　良汰、西本　光)\n")
        help.insert("end", "     \n")
        help.insert("end", "2023\n")
        help.configure(state="disabled")
        help.grid(row=0, column=1, columnspan=1, sticky="nswe")
        help.configure(yscrollcommand=help_textbox_scrollbar.set)
    return


def empty():
    a1.configure(state= "normal", text_color=text_color)
    a1.delete(0, END)
    a1.configure(state="disabled", text_color=text_color_disabled)
    b1.configure(state="normal", text_color=text_color)
    b1.delete(0, END)
    b1.configure(state="disabled", text_color=text_color_disabled)
    c1.configure(state="normal", text_color=text_color)
    c1.delete(0, END)
    c1.configure(state="disabled", text_color=text_color_disabled)

    d1.configure(state="normal", text_color=text_color)
    d1.delete(0, END)
    d1.configure(state="disabled", text_color=text_color_disabled)
    e1.configure(state="normal", text_color=text_color)
    e1.delete(0, END)
    e1.configure(state="disabled", text_color=text_color_disabled)
    f1.configure(state="normal", text_color=text_color)
    f1.delete(0, END)
    f1.configure(state="disabled", text_color=text_color_disabled)

    g1.configure(state="normal", text_color=text_color)
    g1.delete(0, END)
    g1.configure(state="disabled", text_color=text_color_disabled)
    h1.configure(state="normal", text_color=text_color)
    h1.delete(0, END)
    h1.configure(state="disabled", text_color=text_color_disabled)
    i1.configure(state="normal", text_color=text_color)
    i1.delete(0, END)
    i1.configure(state="disabled", text_color=text_color_disabled)

    a2.configure(state="normal", text_color=text_color)
    a2.delete(0, END)
    a2.configure(state="disabled", text_color=text_color_disabled)
    b2.configure(state="normal", text_color=text_color)
    b2.delete(0, END)
    b2.configure(state="disabled", text_color=text_color_disabled)
    c2.configure(state="normal", text_color=text_color)
    c2.delete(0, END)
    c2.configure(state="disabled", text_color=text_color_disabled)
    d2.configure(state="normal", text_color=text_color)
    d2.delete(0, END)
    d2.configure(state="disabled", text_color=text_color_disabled)

    e2.configure(state="normal", text_color=text_color)
    e2.delete(0, END)
    e2.configure(state="disabled", text_color=text_color_disabled)
    f2.configure(state="normal", text_color=text_color)
    f2.delete(0, END)
    f2.configure(state="disabled", text_color=text_color_disabled)
    g2.configure(state="normal", text_color=text_color)
    g2.delete(0, END)
    g2.configure(state="disabled", text_color=text_color_disabled)
    h2.configure(state="normal", text_color=text_color)
    h2.delete(0, END)
    h2.configure(state="disabled", text_color=text_color_disabled)

    i2.configure(state="normal", text_color=text_color)
    i2.delete(0, END)
    i2.configure(state="disabled", text_color=text_color_disabled)
    j2.configure(state="normal", text_color=text_color)
    j2.delete(0, END)
    j2.configure(state="disabled", text_color=text_color_disabled)
    k2.configure(state="normal", text_color=text_color)
    k2.delete(0, END)
    k2.configure(state="disabled", text_color=text_color_disabled)
    l2.configure(state="normal", text_color=text_color)
    l2.delete(0, END)
    l2.configure(state="disabled", text_color=text_color_disabled)

    m2.configure(state="normal", text_color=text_color)
    m2.delete(0, END)
    m2.configure(state="disabled", text_color=text_color_disabled)
    n2.configure(state="normal", text_color=text_color)
    n2.delete(0, END)
    n2.configure(state="disabled", text_color=text_color_disabled)
    o2.configure(state="normal", text_color=text_color)
    o2.delete(0, END)
    o2.configure(state="disabled", text_color=text_color_disabled)
    p2.configure(state="normal", text_color=text_color)
    p2.delete(0, END)
    p2.configure(state="disabled", text_color=text_color_disabled)
    return



def _3x3_insertnumbers(difficulty):
    global start_timer, timer_running, timer_counter, stopwatch, used_numbers, auto_jump_cache
    empty()
    used_numbers = []
    auto_jump_cache = []
    _3x3_reset_colors("")
    Timer.delete(0, 'end')
    start_timer = time.time()
    timer_running = True
    stopwatch = 0
    timer_counter = 0
    Timer.configure(text_color="white")
    _3x3_second.set("...")
    if difficulty == 0:
        nhints = 6
    elif difficulty == 1:
        nhints = 4
    else:
        nhints = 2
    global mahoujinindex
    mahoujinindex = random.randint(0,7)
    global chosen_mahoujin
    chosen_mahoujin = _3x3_possible_mahoujins[mahoujinindex] #the mahoujin we will use as a puzzle


    wow = [0,1,2,3, 5,6,7,8] #array
    index_wowowowow = random.sample(range(0,7), nhints) #array #example: easy => [0,1,5,2,6,7], normal>[1,5,7,0], hard>[0,7]
    global index_for_chosen_mahoujin
    index_for_chosen_mahoujin = []
    index_for_chosen_mahoujin = [wow[i] for i in index_wowowowow] #array has nhints*indexes for choosing numbers as hints for mhj
    global backup2
    backup2 = list(chosen_mahoujin)
    puzzle = list(chosen_mahoujin)
    counter1 = 0
    for i in puzzle:
        if counter1 in index_for_chosen_mahoujin:
            pass
        else:
            puzzle[counter1]=puzzle[counter1]-i
        counter1+=1
    global place_sound
    place_sound = False
    if puzzle[0] != 0:
        a1.configure(state="normal", text_color=text_color)
        a1.insert(0, str(puzzle[0]))
        a1.configure(state= "disabled", text_color=text_color_disabled)
        used_numbers.append(a1.get())
    else:
        a1.configure(state="normal", text_color=text_color)
    if puzzle[1] != 0:
        b1.configure(state="normal", text_color=text_color)
        b1.insert(0, str(puzzle[1]))
        b1.configure(state= "disabled", text_color=text_color_disabled)
        used_numbers.append(b1.get())
    else:
        b1.configure(state="normal", text_color=text_color)
    if puzzle[2] != 0:
        c1.configure(state="normal", text_color=text_color)
        c1.insert(0, str(puzzle[2]))
        c1.configure(state= "disabled", text_color=text_color_disabled)
        used_numbers.append(c1.get())
    else:
        c1.configure(state="normal", text_color=text_color)

    if puzzle[3] != 0:
        d1.configure(state="normal", text_color=text_color)
        d1.insert(0, str(puzzle[3]))
        d1.configure(state= "disabled", text_color=text_color_disabled)
        used_numbers.append(d1.get())
    else:
        d1.configure(state="normal", text_color=text_color)
    if puzzle[4] != 0:
        e1.configure(state="normal", text_color=text_color)
        e1.insert(0, str(puzzle[4]))
        e1.configure(state= "disabled", text_color=text_color_disabled)
        used_numbers.append(e1.get())
    else:
        e1.configure(state="normal", text_color=text_color)
    if puzzle[5] != 0:
        f1.configure(state="normal", text_color=text_color)
        f1.insert(0, str(puzzle[5]))
        f1.configure(state= "disabled", text_color=text_color_disabled)
        used_numbers.append(f1.get())
    else:
        f1.configure(state="normal", text_color=text_color)

    if puzzle[6] != 0:
        g1.configure(state="normal", text_color=text_color)
        g1.insert(0, str(puzzle[6]))
        g1.configure(state= "disabled", text_color=text_color_disabled)
        used_numbers.append(g1.get())
    else:
        g1.configure(state="normal", text_color=text_color)
    if puzzle[7] != 0:
        h1.configure(state="normal", text_color=text_color)
        h1.insert(0, str(puzzle[7]))
        h1.configure(state= "disabled", text_color=text_color_disabled)
        used_numbers.append(h1.get())
    else:
        h1.configure(state="normal", text_color=text_color)
    if puzzle[8] != 0:
        i1.configure(state="normal", text_color=text_color)
        i1.insert(0, str(puzzle[8]))
        i1.configure(state= "disabled", text_color=text_color_disabled)
        used_numbers.append(i1.get())
    else:
        i1.configure(state="normal", text_color=text_color)
    mahoujin_start_sound.play()
    place_sound = True
    global _3x3_selected_entry_index
    _3x3_selected_entry_index = 4
    return


def _4x4_insertnumbers():
    empty()
    random_number = random.randint(0, 12)
    chosen_mahoujin = list(_4x4_hints[random_number])
    print(chosen_mahoujin)
    if chosen_mahoujin[0] != 0:
        a2.configure(state="normal", text_color=text_color)
        a2.insert(0, str(chosen_mahoujin[0]))
        a2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        a2.configure(state="normal", text_color=text_color)
    if chosen_mahoujin[1] != 0:
        b2.configure(state="normal", text_color=text_color)
        b2.insert(0, str(chosen_mahoujin[1]))
        b2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        b2.configure(state="normal", text_color=text_color)
    if chosen_mahoujin[2] != 0:
        c2.configure(state="normal", text_color=text_color)
        c2.insert(0, str(chosen_mahoujin[2]))
        c2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        c2.configure(state="normal", text_color=text_color)
    if chosen_mahoujin[3] != 0:
        d2.configure(state="normal", text_color=text_color)
        d2.insert(0, str(chosen_mahoujin[3]))
        d2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        d2.configure(state="normal", text_color=text_color)

    if chosen_mahoujin[4] != 0:
        e2.configure(state="normal", text_color=text_color)
        e2.insert(0, str(chosen_mahoujin[4]))
        e2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        e2.configure(state="normal", text_color=text_color)
    if chosen_mahoujin[5] != 0:
        f2.configure(state="normal", text_color=text_color)
        f2.insert(0, str(chosen_mahoujin[5]))
        f2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        f2.configure(state="normal", text_color=text_color)
    if chosen_mahoujin[6] != 0:
        g2.configure(state="normal", text_color=text_color)
        g2.insert(0, str(chosen_mahoujin[6]))
        g2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        g2.configure(state="normal", text_color=text_color)
    if chosen_mahoujin[7] != 0:
        h2.configure(state="normal", text_color=text_color)
        h2.insert(0, str(chosen_mahoujin[7]))
        h2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        h2.configure(state="normal", text_color=text_color)

    if chosen_mahoujin[8] != 0:
        i2.configure(state="normal", text_color=text_color)
        i2.insert(0, str(chosen_mahoujin[8]))
        i2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        i2.configure(state="normal", text_color=text_color)
    if chosen_mahoujin[9] != 0:
        j2.configure(state="normal", text_color=text_color)
        j2.insert(0, str(chosen_mahoujin[9]))
        j2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        j2.configure(state="normal", text_color=text_color)
    if chosen_mahoujin[10] != 0:
        k2.configure(state="normal", text_color=text_color)
        k2.insert(0, str(chosen_mahoujin[10]))
        k2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        k2.configure(state="normal", text_color=text_color)
    if chosen_mahoujin[11] != 0:
        l2.configure(state="normal", text_color=text_color)
        l2.insert(0, str(chosen_mahoujin[11]))
        l2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        l2.configure(state="normal", text_color=text_color)

    if chosen_mahoujin[12] != 0:
        m2.configure(state="normal", text_color=text_color)
        m2.insert(0, str(chosen_mahoujin[12]))
        m2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        m2.configure(state="normal", text_color=text_color)
    if chosen_mahoujin[13] != 0:
        n2.configure(state="normal", text_color=text_color)
        n2.insert(0, str(chosen_mahoujin[13]))
        n2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        n2.configure(state="normal", text_color=text_color)
    if chosen_mahoujin[14] != 0:
        o2.configure(state="normal", text_color=text_color)
        o2.insert(0, str(chosen_mahoujin[14]))
        o2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        o2.configure(state="normal", text_color=text_color)
    if chosen_mahoujin[15] != 0:
        p2.configure(state="normal", text_color=text_color)
        p2.insert(0, str(chosen_mahoujin[15]))
        p2.configure(state= "disabled", text_color=text_color_disabled)
    else:
        p2.configure(state="normal", text_color=text_color)
    return


def _3x3_animate(color, animation, counter_animation):
    animationlist = list(animation)
    if counter_animation < len(animationlist):
        a1.configure(text_color=text_color)
        b1.configure(text_color=text_color)
        c1.configure(text_color=text_color)

        d1.configure(text_color=text_color)
        e1.configure(text_color=text_color)
        f1.configure(text_color=text_color)

        g1.configure(text_color=text_color)
        h1.configure(text_color=text_color)
        i1.configure(text_color=text_color)
        frame = list(animationlist)[counter_animation]
        for i in frame:
            if i == "a":
                a1.configure(text_color=color)
            if i == "b":
                b1.configure(text_color=color)
            if i == "c":
                c1.configure(text_color=color)

            if i == "d":
                d1.configure(text_color=color)
            if i == "e":
                e1.configure(text_color=color)
            if i == "f":
                f1.configure(text_color=color)

            if i == "g":
                g1.configure(text_color=color)
            if i == "h":
                h1.configure(text_color=color)
            if i == "i":
                i1.configure(text_color=color)
        window.update_idletasks()
        window.after(1, _3x3_animate(color, animation, counter_animation+1))
    else:
        a1.configure(text_color=text_color)
        b1.configure(text_color=text_color)
        c1.configure(text_color=text_color)

        d1.configure(text_color=text_color)
        e1.configure(text_color=text_color)
        f1.configure(text_color=text_color)

        g1.configure(text_color=text_color)
        h1.configure(text_color=text_color)
        i1.configure(text_color=text_color)
        return

def _3x3_animate_wrong(color, animation, counter_animation):
    if counter_animation == 0:
        pass
    animationlist = list(animation)
    if counter_animation < len(animationlist):

        a1.configure(fg_color=fg_color_entry)
        b1.configure(fg_color=fg_color_entry)
        c1.configure(fg_color=fg_color_entry)

        d1.configure(fg_color=fg_color_entry)
        e1.configure(fg_color=fg_color_entry)
        f1.configure(fg_color=fg_color_entry)

        g1.configure(fg_color=fg_color_entry)
        h1.configure(fg_color=fg_color_entry)
        i1.configure(fg_color=fg_color_entry)
        window.update_idletasks()
        frame = animationlist[counter_animation]
        for i in frame:
            if i == "a":
                a1.configure(fg_color=color)
            if i == "b":
                b1.configure(fg_color=color)
            if i == "c":
                c1.configure(fg_color=color)

            if i == "d":
                d1.configure(fg_color=color)
            if i == "e":
                e1.configure(fg_color=color)
            if i == "f":
                f1.configure(fg_color=color)

            if i == "g":
                g1.configure(fg_color=color)
            if i == "h":
                h1.configure(fg_color=color)
            if i == "i":
                i1.configure(fg_color=color)
        window.update_idletasks()
        window.after(1, _3x3_animate_wrong(color, animation, counter_animation+1))
    else:
        frame = list(animationlist)[counter_animation-1]
        for i in frame:
            if i == "a":
                a1.configure(fg_color=fg_color_entry)
            if i == "b":
                b1.configure(fg_color=fg_color_entry)
            if i == "c":
                c1.configure(fg_color=fg_color_entry)

            if i == "d":
                d1.configure(fg_color=fg_color_entry)
            if i == "e":
                e1.configure(fg_color=fg_color_entry)
            if i == "f":
                f1.configure(fg_color=fg_color_entry)

            if i == "g":
                g1.configure(fg_color=fg_color_entry)
            if i == "h":
                h1.configure(fg_color=fg_color_entry)
            if i == "i":
                i1.configure(fg_color=fg_color_entry)
            window.update_idletasks()
        return

def _4x4_animate_wrong(color, animation, counter_animation):
    if counter_animation == 0:
        pass
    animationlist = list(animation)
    if counter_animation < len(animationlist):

        a2.configure(fg_color=fg_color_entry)
        b2.configure(fg_color=fg_color_entry)
        c2.configure(fg_color=fg_color_entry)
        d2.configure(fg_color=fg_color_entry)

        e2.configure(fg_color=fg_color_entry)
        f2.configure(fg_color=fg_color_entry)
        g2.configure(fg_color=fg_color_entry)
        h2.configure(fg_color=fg_color_entry)

        i2.configure(fg_color=fg_color_entry)
        j2.configure(fg_color=fg_color_entry)
        k2.configure(fg_color=fg_color_entry)
        l2.configure(fg_color=fg_color_entry)

        m2.configure(fg_color=fg_color_entry)
        n2.configure(fg_color=fg_color_entry)
        o2.configure(fg_color=fg_color_entry)
        p2.configure(fg_color=fg_color_entry)
        window.update_idletasks()
        frame = animationlist[counter_animation]
        for i in frame:
            if i == "a":
                a2.configure(fg_color=color)
            if i == "b":
                b2.configure(fg_color=color)
            if i == "c":
                c2.configure(fg_color=color)
            if i == "d":
                d2.configure(fg_color=color)

            if i == "e":
                e2.configure(fg_color=color)
            if i == "f":
                f2.configure(fg_color=color)
            if i == "g":
                g2.configure(fg_color=color)
            if i == "h":
                h2.configure(fg_color=color)

            if i == "i":
                i2.configure(fg_color=color)
            if i == "j":
                j2.configure(fg_color=color)
            if i == "k":
                k2.configure(fg_color=color)
            if i == "l":
                l2.configure(fg_color=color)

            if i == "m":
                m2.configure(fg_color=color)
            if i == "n":
                n2.configure(fg_color=color)
            if i == "o":
                o2.configure(fg_color=color)
            if i == "p":
                p2.configure(fg_color=color)
        window.update_idletasks()
        window.after(1, _3x3_animate_wrong(color, animation, counter_animation+1))
    else:
        frame = list(animationlist)[counter_animation-1]
        for i in frame:
            if i == "a":
                a2.configure(fg_color=fg_color_entry)
            if i == "b":
                b2.configure(fg_color=fg_color_entry)
            if i == "c":
                c2.configure(fg_color=fg_color_entry)
            if i == "d":
                d2.configure(fg_color=fg_color_entry)

            if i == "e":
                e2.configure(fg_color=fg_color_entry)
            if i == "f":
                f2.configure(fg_color=fg_color_entry)
            if i == "g":
                g2.configure(fg_color=fg_color_entry)
            if i == "h":
                h2.configure(fg_color=fg_color_entry)

            if i == "i":
                i2.configure(fg_color=fg_color_entry)
            if i == "j":
                j2.configure(fg_color=fg_color_entry)
            if i == "k":
                k2.configure(fg_color=fg_color_entry)
            if i == "l":
                l2.configure(fg_color=fg_color_entry)

            if i == "m":
                m2.configure(fg_color=fg_color_entry)
            if i == "n":
                n2.configure(fg_color=fg_color_entry)
            if i == "o":
                o2.configure(fg_color=fg_color_entry)
            if i == "p":
                p2.configure(fg_color=fg_color_entry)
            window.update_idletasks()
        return


def _3x3_check():
    global index_for_chosen_mahoujin, used_numbers
    if len(e1.get()) != 0:
        if int(e1.get()) == 5:
            e1.configure(state="disabled", text_color=text_color_disabled)
            index_for_chosen_mahoujin.append(4)
            used_numbers.append(e1.get())
    if len(a1.get()) != 0 and len(b1.get()) != 0 and len(c1.get()) != 0:
        if int(a1.get()) + int(b1.get()) + int(c1.get()) == 15:
            a1.configure(state="disabled", text_color=text_color_disabled)
            b1.configure(state="disabled", text_color=text_color_disabled)
            c1.configure(state="disabled", text_color=text_color_disabled)
            index_for_chosen_mahoujin.extend([0,1,2])
            used_numbers.extend([a1.get(), b1.get(), c1.get()])
    if len(d1.get()) != 0 and len(e1.get()) != 0 and len(f1.get()) != 0:
        if int(d1.get()) + int(e1.get()) + int(f1.get()) == 15:
            d1.configure(state="disabled", text_color=text_color_disabled)
            e1.configure(state="disabled", text_color=text_color_disabled)
            f1.configure(state="disabled", text_color=text_color_disabled)
            index_for_chosen_mahoujin.extend([3, 4, 5])
            used_numbers.extend([d1.get(), e1.get(), f1.get() ])
    if len(g1.get()) != 0 and len(h1.get()) != 0 and len(i1.get()) != 0:
        if int(g1.get()) + int(h1.get()) + int(i1.get()) == 15:
            g1.configure(state="disabled", text_color=text_color_disabled)
            h1.configure(state="disabled", text_color=text_color_disabled)
            i1.configure(state="disabled", text_color=text_color_disabled)
            index_for_chosen_mahoujin.extend([6, 7, 8])
            used_numbers.extend([g1.get(), h1.get(), i1.get()])

    if len(a1.get()) != 0 and len(d1.get()) != 0 and len(g1.get()) != 0:
        if int(a1.get()) + int(d1.get()) + int(g1.get()) == 15:
            a1.configure(state="disabled", text_color=text_color_disabled)
            d1.configure(state="disabled", text_color=text_color_disabled)
            g1.configure(state="disabled", text_color=text_color_disabled)
            index_for_chosen_mahoujin.extend([0, 3, 6])
            used_numbers.extend([a1.get(), d1.get(), g1.get()])
    if len(b1.get()) != 0 and len(e1.get()) != 0 and len(h1.get()) != 0:
        if int(b1.get()) + int(e1.get()) + int(h1.get()) == 15:
            b1.configure(state="disabled", text_color=text_color_disabled)
            e1.configure(state="disabled", text_color=text_color_disabled)
            h1.configure(state="disabled", text_color=text_color_disabled)
            index_for_chosen_mahoujin.extend([1, 4, 7])
            used_numbers.extend([b1.get(), e1.get(), h1.get()])
    if len(c1.get()) != 0 and len(f1.get()) != 0 and len(i1.get()) != 0:
        if int(c1.get()) + int(f1.get()) + int(i1.get()) == 15:
            c1.configure(state="disabled", text_color=text_color_disabled)
            f1.configure(state="disabled", text_color=text_color_disabled)
            i1.configure(state="disabled", text_color=text_color_disabled)
            index_for_chosen_mahoujin.extend([2, 5, 8])
            used_numbers.extend([c1.get(), f1.get(), i1.get()])

    if len(a1.get()) != 0 and len(e1.get()) != 0 and len(i1.get()) != 0:
        if int(a1.get()) + int(e1.get()) + int(i1.get()) == 15:
            a1.configure(state="disabled", text_color=text_color_disabled)
            e1.configure(state="disabled", text_color=text_color_disabled)
            i1.configure(state="disabled", text_color=text_color_disabled)
            index_for_chosen_mahoujin.extend([0, 4, 8])
            used_numbers.extend([a1.get(), e1.get(), i1.get()])
    if len(c1.get()) != 0 and len(e1.get()) != 0 and len(g1.get()) != 0:
        if int(c1.get()) + int(e1.get()) + int(g1.get()) == 15:
            c1.configure(state="disabled", text_color=text_color_disabled)
            e1.configure(state="disabled", text_color=text_color_disabled)
            g1.configure(state="disabled", text_color=text_color_disabled)
            index_for_chosen_mahoujin.extend([2, 4, 6])
            used_numbers.extend([c1.get(), e1.get(), g1.get()])

    if len(a1.get()) != 0 and\
        len(b1.get()) != 0 and\
        len(c1.get()) != 0 and\
        len(d1.get()) != 0 and\
        len(e1.get()) != 0 and\
        len(f1.get()) != 0 and\
        len(g1.get()) != 0 and\
        len(h1.get()) != 0 and\
        len(i1.get()) != 0:

        if int(a1.get()) + int(b1.get()) + int(c1.get()) == 15 and \
            int(d1.get()) + int(e1.get()) + int(f1.get()) == 15 and \
            int(g1.get()) + int(h1.get()) + int(i1.get()) == 15 and \
            int(a1.get()) + int(d1.get()) + int(g1.get()) == 15 and \
            int(b1.get()) + int(e1.get()) + int(h1.get()) == 15 and \
            int(c1.get()) + int(f1.get()) + int(i1.get()) == 15 and \
            int(a1.get()) + int(e1.get()) + int(i1.get()) == 15 and \
            int(c1.get()) + int(e1.get()) + int(g1.get()) == 15:
            a1.configure(state="disabled", text_color=text_color_disabled)
            b1.configure(state="disabled", text_color=text_color_disabled)
            c1.configure(state="disabled", text_color=text_color_disabled)

            d1.configure(state="disabled", text_color=text_color_disabled)
            e1.configure(state="disabled", text_color=text_color_disabled)
            f1.configure(state="disabled", text_color=text_color_disabled)

            g1.configure(state="disabled", text_color=text_color_disabled)
            h1.configure(state="disabled", text_color=text_color_disabled)
            i1.configure(state="disabled", text_color=text_color_disabled)

            seikai = customtkinter.CTkLabel(_3x3_mahoujin_frame, text="正解", text_font=('MS Mincho', 50))
            if counter_animation == 0:
                seikai.grid(row=2, column=2)
                seikai.lift()
            print("Code initiated and completed successfully.")
            print(" ")
            global end_timer, timer_running, timer_counter
            timer_running = False

            Timer.delete(0, 'end')
            end_timer = time.time()
            timer_counter = round(end_timer - start_timer,2)
            if int(difficulty_slider.get()) == 0:
                if timer_counter <= 5:
                    Timer.configure(text_color=Ranking[0])
                elif 5 <= timer_counter <= 10:
                    Timer.configure(text_color=Ranking[1])
                elif 10 <= timer_counter <= 30:
                    Timer.configure(text_color=Ranking[2])
                else:
                    Timer.configure(text_color=Ranking[3])
            if int(difficulty_slider.get()) == 1:
                if timer_counter <= 7:
                    Timer.configure(text_color=Ranking[0])
                elif 7 <= timer_counter <= 10:
                    Timer.configure(text_color=Ranking[1])
                elif 10 <= timer_counter <= 20:
                    Timer.configure(text_color=Ranking[2])
                else:
                    Timer.configure(text_color=Ranking[3])
            else:
                if timer_counter <= 10:
                    Timer.configure(text_color=Ranking[0])
                elif 10 <= timer_counter <= 12:
                    Timer.configure(text_color=Ranking[1])
                elif 12 <= timer_counter <= 14:
                    Timer.configure(text_color=Ranking[2])
                else:
                    Timer.configure(text_color=Ranking[3])
            window.update_idletasks()
            _3x3_second.set(str(timer_counter) + " 秒")
            global animation_finish
            finish.play()
            _3x3_animate("white", animation_finish, 0)
            empty()
            print("Iterating code again.")
            seikai.grid_remove()
    else:
        dayum = _3x3_possible_mahoujins[mahoujinindex]
        wrong = []
        if len(a1.get()) == 0 or int(a1.get()) != dayum[0]:
            wrong.append("a")
        if len(b1.get()) == 0 or int(b1.get()) != dayum[1]:
            wrong.append("b")
        if len(c1.get()) == 0 or int(c1.get()) != dayum[2]:
            wrong.append("c")

        if len(d1.get()) == 0 or int(d1.get()) != dayum[3]:
            wrong.append("d")
        if len(e1.get()) == 0 or int(e1.get()) != dayum[4]:
            wrong.append("e")
        if len(f1.get()) == 0 or int(f1.get()) != dayum[5]:
            wrong.append("f")

        if len(g1.get()) == 0 or int(g1.get()) != dayum[6]:
            wrong.append("g")
        if len(h1.get()) == 0 or int(h1.get()) != dayum[7]:
            wrong.append("h")
        if len(i1.get()) == 0 or int(i1.get()) != dayum[8]:
            wrong.append("i")

        yarinaosi = customtkinter.CTkLabel(_3x3_mahoujin_frame, text="やり直し", text_font=('MS Mincho', 50),
                                           text_color="red")
        yarinaosi.grid(row=2, column=1, columnspan=3)
        yarinaosi.lift()
        animation_wrong = []
        animation_wrong.append(wrong)
        animation_wrong.append(wrong)
        animation_wrong.append(wrong)
        input_false.play()
        _3x3_animate_wrong("#ff0000", animation_wrong, 0)
        yarinaosi.grid_remove()
    return

def _4x4_check():
    if int(a2.get()) + int(b2.get()) + int(c2.get()) + int(d2.get()) == 34:
        a2.configure(state="disabled", text_color=text_color_disabled)
        b2.configure(state="disabled", text_color=text_color_disabled)
        c2.configure(state="disabled", text_color=text_color_disabled)
        d2.configure(state="disabled", text_color=text_color_disabled)
    elif int(e2.get()) + int(f2.get()) + int(g2.get()) + int(h2.get()) == 34:
        e2.configure(state="disabled", text_color=text_color_disabled)
        f2.configure(state="disabled", text_color=text_color_disabled)
        g2.configure(state="disabled", text_color=text_color_disabled)
        h2.configure(state="disabled", text_color=text_color_disabled)
    elif int(i2.get()) + int(j2.get()) + int(k2.get()) + int(l2.get()) == 34:
        i2.configure(state="disabled", text_color=text_color_disabled)
        j2.configure(state="disabled", text_color=text_color_disabled)
        k2.configure(state="disabled", text_color=text_color_disabled)
        l2.configure(state="disabled", text_color=text_color_disabled)
    elif int(m2.get()) + int(n2.get()) + int(o2.get()) + int(p2.get()) == 34:
        m2.configure(state="disabled", text_color=text_color_disabled)
        n2.configure(state="disabled", text_color=text_color_disabled)
        o2.configure(state="disabled", text_color=text_color_disabled)
        p2.configure(state="disabled", text_color=text_color_disabled)
    elif int(a2.get()) + int(f2.get()) + int(k2.get()) + int(p2.get()) == 34:
        a2.configure(state="disabled", text_color=text_color_disabled)
        f2.configure(state="disabled", text_color=text_color_disabled)
        k2.configure(state="disabled", text_color=text_color_disabled)
        p2.configure(state="disabled", text_color=text_color_disabled)
    elif int(d2.get()) + int(g2.get()) + int(j2.get()) + int(m2.get()) == 34:
        d2.configure(state="disabled", text_color=text_color_disabled)
        g2.configure(state="disabled", text_color=text_color_disabled)
        j2.configure(state="disabled", text_color=text_color_disabled)
        m2.configure(state="disabled", text_color=text_color_disabled)
    elif int(f2.get()) + int(g2.get()) + int(j2.get()) + int(k2.get()) == 34:
        f2.configure(state="disabled", text_color=text_color_disabled)
        g2.configure(state="disabled", text_color=text_color_disabled)
        j2.configure(state="disabled", text_color=text_color_disabled)
        k2.configure(state="disabled", text_color=text_color_disabled)
    elif int(a2.get()) + int(d2.get()) + int(m2.get()) + int(p2.get()) == 34:
        a2.configure(state="disabled", text_color=text_color_disabled)
        d2.configure(state="disabled", text_color=text_color_disabled)
        m2.configure(state="disabled", text_color=text_color_disabled)
        p2.configure(state="disabled", text_color=text_color_disabled)
    elif int(b2.get()) + int(c2.get()) + int(n2.get()) + int(o2.get()) == 34:
        b2.configure(state="disabled", text_color=text_color_disabled)
        c2.configure(state="disabled", text_color=text_color_disabled)
        n2.configure(state="disabled", text_color=text_color_disabled)
        o2.configure(state="disabled", text_color=text_color_disabled)
    elif int(e2.get()) + int(i2.get()) + int(h2.get()) + int(l2.get()) == 34:
        e2.configure(state="disabled", text_color=text_color_disabled)
        i2.configure(state="disabled", text_color=text_color_disabled)
        h2.configure(state="disabled", text_color=text_color_disabled)
        l2.configure(state="disabled", text_color=text_color_disabled)

    if int(a2.get()) + int(b2.get()) + int(c2.get()) + int(d2.get()) == 34\
        and int(e2.get()) + int(f2.get()) + int(g2.get()) + int(h2.get()) == 34\
        and int(i2.get()) + int(j2.get()) + int(k2.get()) + int(l2.get()) == 34\
        and int(m2.get()) + int(n2.get()) + int(o2.get()) + int(p2.get()) == 34\
        and int(a2.get()) + int(f2.get()) + int(k2.get()) + int(p2.get()) == 34\
        and int(d2.get()) + int(g2.get()) + int(j2.get()) + int(m2.get()) == 34:
            a2.configure(state="disabled", text_color=text_color_disabled)
            b2.configure(state="disabled", text_color=text_color_disabled)
            c2.configure(state="disabled", text_color=text_color_disabled)
            d2.configure(state="disabled", text_color=text_color_disabled)

            e2.configure(state="disabled", text_color=text_color_disabled)
            f2.configure(state="disabled", text_color=text_color_disabled)
            g2.configure(state="disabled", text_color=text_color_disabled)
            h2.configure(state="disabled", text_color=text_color_disabled)

            i2.configure(state="disabled", text_color=text_color_disabled)
            j2.configure(state="disabled", text_color=text_color_disabled)
            k2.configure(state="disabled", text_color=text_color_disabled)
            l2.configure(state="disabled", text_color=text_color_disabled)

            m2.configure(state="disabled", text_color=text_color_disabled)
            n2.configure(state="disabled", text_color=text_color_disabled)
            o2.configure(state="disabled", text_color=text_color_disabled)
            p2.configure(state="disabled", text_color=text_color_disabled)

            seikai = customtkinter.CTkLabel(_4x4_mahoujin_frame, text="正解", text_font=('MS Mincho', 50))
            if counter_animation == 0:
                seikai.grid(row=2, column=2, rowspan=2, columnspan=2)
                seikai.lift()
            print("Code initiated and completed successfully.")
            print(" ")

            window.update_idletasks()
            global animation_finish
            finish.play()

            empty()
            print("Iterating code again.")
            seikai.grid_remove()
    else:
        wrong=["a","b","c","d", "e","f","g","h", "i","j","k","l", "m","n","o","p",]
        yarinaosi = customtkinter.CTkLabel(_4x4_mahoujin_frame, text="やり直し", text_font=('MS Mincho', 50),
                                           text_color="red")
        yarinaosi.grid(row=2, column=1, columnspan=4,rowspan=2)
        yarinaosi.lift()
        animation_wrong = []
        animation_wrong.append(wrong)
        animation_wrong.append(wrong)
        animation_wrong.append(wrong)
        input_false.play()
        _4x4_animate_wrong("#ff0000", animation_wrong, 0)
        yarinaosi.grid_remove()

    return



def manage_settings():


    settings = customtkinter.CTkToplevel(window)
    settings.geometry("400x300")

    settings.title("⚙ 設定")

    settings.grid_rowconfigure(0,minsize=10)


    toggle_music = customtkinter.CTkButton(settings, text="BGM on/off", command=lambda: manage_sounds("Music"))
    toggle_sounds = customtkinter.CTkButton(settings, text="音 on/off", command=lambda: manage_sounds("Sounds"))

    turn_on_timer_and_countdown = customtkinter.CTkSwitch(settings, text="タイマーとカウントダウン")
    toggle_timer_countdown = customtkinter.CTkOptionMenu(settings, values=["なし", "タイマー", "カウントダウン"])



    toggle_music.grid(row=1, column=0, padx=20, pady=10, sticky="w")
    toggle_sounds.grid(row=2, column=0, padx=20, pady=10, sticky="w")
    turn_on_timer_and_countdown.grid(row=3, column=0, padx=20, pady=10, sticky="w")
    toggle_timer_countdown.grid(row=4, column=0, padx=20, pady=10, sticky="w")
    return

def manage_sounds(which):
    if which == "Music":
        global music_on
        if music_on:
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(0)
            music_on = not music_on
        else:
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(0.05)
            music_on = not music_on
    else:
        global sound_on
        if sound_on:
            place.set_volume(0)
            finish.set_volume(0)
            input_false.set_volume(0)
            mahoujin_start_sound.set_volume(0)
            sound_on = not sound_on
        else:
            place.set_volume(1)
            finish.set_volume(1)
            input_false.set_volume(1)
            mahoujin_start_sound.set_volume(0.5)
            sound_on = not sound_on


# ============ Creating 3 Frames/Sections ============
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)

frame_left = customtkinter.CTkFrame(master=window, fg_color=fg_color_entry, width=150, corner_radius=0)
frame_middle = customtkinter.CTkFrame(master=window, corner_radius=0)
frame_right = customtkinter.CTkFrame(master=window, fg_color=fg_color_entry, width=150, corner_radius=0)



frame_left.grid(row=0, column=0, sticky="nswe")
frame_middle.grid(row=0, column=1, sticky="nswe")
frame_right.grid(row=0, column=2, sticky="nswe")



# ============ Left Frame/Section ============
frame_left.grid_rowconfigure(0, minsize=10)
frame_left.grid_rowconfigure(5, weight=1)
frame_left.grid_rowconfigure(8, minsize=20)
frame_left.grid_rowconfigure(11, minsize=10)




name = customtkinter.CTkLabel(frame_left, text="Ennea Squares", text_font=("Bahnschrift", 14), justify="center")
name.grid(row=1, column=0, pady=10, padx=0)

SetMode3x3 = customtkinter.CTkButton(frame_left, text="3x3", text_font=("Bahnschrift", 14), fg_color=fg_color_entry, command=lambda:change_mahoujin_mode("3x3"))
SetMode3x3.grid(row=3, column=0, pady=10, padx=0)
SetMode4x4 = customtkinter.CTkButton(frame_left, text="4x4", text_font=("Bahnschrift", 14), fg_color=fg_color_entry, command=lambda:change_mahoujin_mode("4x4"))
SetMode4x4.grid(row=4, column=0, pady=10, padx=0)


def change_appearance_mode(new_appearance_mode):
    global text_color, text_color_disabled, entry_bg, fg_color_entry
    if new_appearance_mode == "白":
        customtkinter.set_appearance_mode("Light")
    else:
        customtkinter.set_appearance_mode("Dark")
    return

themechanger = customtkinter.CTkOptionMenu(master=frame_left, fg_color=text_color,text_color="black", button_color=text_color, button_hover_color="#448038",  values=["黒","白"], command=change_appearance_mode)
themechanger.grid(row=10, column=0, pady=10, padx=0)


if themechanger.get() == "黒":
    logo_raw = (Image.open("mahoujin_white.png"))
    resized_image_logo = logo_raw.resize((200, 200), Image.Resampling.LANCZOS)
    logo_raw = ImageTk.PhotoImage(resized_image_logo)
    logo = customtkinter.CTkLabel(frame_left, image=logo_raw, fg_color=fg_color_entry)
    logo.grid(row=0, column=0, pady=10, padx=10)
else:

    logo_raw = (Image.open("mahoujin_black.png"))
    resized_image_logo = logo_raw.resize((200, 200), Image.Resampling.LANCZOS)
    logo_raw = ImageTk.PhotoImage(resized_image_logo)
    logo = customtkinter.CTkLabel(frame_left, image=logo_raw, fg_color=fg_color_entry)
    logo.grid(row=0, column=0, pady=10, padx=10)


Timer = customtkinter.CTkEntry(frame_left, text_color=text_color_disabled,width=150, text_font=('Bahnschrift', 14),textvariable=_3x3_second, fg_color=fg_color_entry[1], justify="center", corner_radius=0)
Timer.configure(state="disabled")
Timer.grid(row=11, column=0, pady=10, padx=10)


# ============ Middle Frame/Section ============
frame_middle.grid_columnconfigure(0, weight=1)
frame_middle.grid_columnconfigure(1, weight=1)


_3x3_mahoujin_frame = customtkinter.CTkFrame(frame_middle,
                               fg_color=fg_color_entry,
                               width=500,
                               height=600,
                               corner_radius=20)
_3x3_mahoujin_frame.grid(row=0, column=0, pady=60, padx=30, sticky="e")

_4x4_mahoujin_frame = customtkinter.CTkFrame(frame_middle,
                               fg_color=fg_color_entry,
                               width=500,
                               height=600,
                               corner_radius=20)

#_4x4_mahoujin_frame.lower()

info_frame = customtkinter.CTkFrame(frame_middle,
                                fg_color=fg_color_entry,
                                width=300,
                                height=600,
                                corner_radius=0)
info_frame.grid(row=0, column=1, pady=60, padx=20, sticky="w")



# ============ The 3x3 Mahoujin table ============
_3x3_mahoujin_frame.grid_rowconfigure(0, minsize=105)
_3x3_mahoujin_frame.grid_rowconfigure(4, minsize=70)
_3x3_mahoujin_frame.grid_rowconfigure(6, minsize=70)
_3x3_mahoujin_frame.grid_columnconfigure(0, minsize=50)
_3x3_mahoujin_frame.grid_columnconfigure(4, minsize=50)

a1 = customtkinter.CTkEntry(_3x3_mahoujin_frame, width=130, height=130, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_3x3_vcmd, state="normal")
b1 = customtkinter.CTkEntry(_3x3_mahoujin_frame, width=130, height=130, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_3x3_vcmd, state="normal")
c1 = customtkinter.CTkEntry(_3x3_mahoujin_frame, width=130, height=130, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_3x3_vcmd, state="normal")

d1 = customtkinter.CTkEntry(_3x3_mahoujin_frame, width=130, height=130, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_3x3_vcmd, state="normal")
e1 = customtkinter.CTkEntry(_3x3_mahoujin_frame, width=130, height=130, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_3x3_vcmd, state="normal")
f1 = customtkinter.CTkEntry(_3x3_mahoujin_frame, width=130, height=130, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_3x3_vcmd, state="normal")

g1 = customtkinter.CTkEntry(_3x3_mahoujin_frame, width=130, height=130, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_3x3_vcmd, state="normal")
h1 = customtkinter.CTkEntry(_3x3_mahoujin_frame, width=130, height=130, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_3x3_vcmd, state="normal")
i1 = customtkinter.CTkEntry(_3x3_mahoujin_frame, width=130, height=130, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_3x3_vcmd, state="normal")


space_between_entries = 3

a1.grid(row=1, column=1, pady=space_between_entries, padx=space_between_entries)
b1.grid(row=1, column=2, pady=space_between_entries, padx=space_between_entries)
c1.grid(row=1, column=3, pady=space_between_entries, padx=space_between_entries)

d1.grid(row=2, column=1, pady=space_between_entries, padx=space_between_entries)
e1.grid(row=2, column=2, pady=space_between_entries, padx=space_between_entries)
f1.grid(row=2, column=3, pady=space_between_entries, padx=space_between_entries)

g1.grid(row=3, column=1, pady=space_between_entries, padx=space_between_entries)
h1.grid(row=3, column=2, pady=space_between_entries, padx=space_between_entries)
i1.grid(row=3, column=3, pady=space_between_entries, padx=space_between_entries)

a1.configure(state="disabled", text_color=text_color_disabled)
b1.configure(state="disabled", text_color=text_color_disabled)
c1.configure(state="disabled", text_color=text_color_disabled)

d1.configure(state="disabled", text_color=text_color_disabled)
e1.configure(state="disabled", text_color=text_color_disabled)
f1.configure(state="disabled", text_color=text_color_disabled)

g1.configure(state="disabled", text_color=text_color_disabled)
h1.configure(state="disabled", text_color=text_color_disabled)
i1.configure(state="disabled", text_color=text_color_disabled)

_3x3_kakunin = customtkinter.CTkButton(_3x3_mahoujin_frame, corner_radius=1, fg_color=text_color,
                                       text="確認", text_color="black", hover_color="#448038", command=lambda:_3x3_check())
_3x3_kakunin.grid(row=5, column=2)



# ============ The 4x4 Mahoujin table ============
_4x4_mahoujin_frame.grid_rowconfigure(0, minsize=105)
_4x4_mahoujin_frame.grid_rowconfigure(5, minsize=70)
_4x4_mahoujin_frame.grid_rowconfigure(7, minsize=70)
_4x4_mahoujin_frame.grid_columnconfigure(0, minsize=50)
_4x4_mahoujin_frame.grid_columnconfigure(5, minsize=50)


a2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")
b2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")
c2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")
d2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")

e2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")
f2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")
g2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")
h2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")

i2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")
j2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")
k2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")
l2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")

m2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")
n2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")
o2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")
p2 = customtkinter.CTkEntry(_4x4_mahoujin_frame, width=100, height=100, text_color=(text_color), fg_color=fg_color_entry, corner_radius=1, text_font=('Bahnschrift', 50), justify='center', validate="key", validatecommand=_4x4_vcmd, state="normal")


space_between_entries = 1

a2.grid(row=1, column=1, pady=space_between_entries, padx=space_between_entries)
b2.grid(row=1, column=2, pady=space_between_entries, padx=space_between_entries)
c2.grid(row=1, column=3, pady=space_between_entries, padx=space_between_entries)
d2.grid(row=1, column=4, pady=space_between_entries, padx=space_between_entries)

e2.grid(row=2, column=1, pady=space_between_entries, padx=space_between_entries)
f2.grid(row=2, column=2, pady=space_between_entries, padx=space_between_entries)
g2.grid(row=2, column=3, pady=space_between_entries, padx=space_between_entries)
h2.grid(row=2, column=4, pady=space_between_entries, padx=space_between_entries)

i2.grid(row=3, column=1, pady=space_between_entries, padx=space_between_entries)
j2.grid(row=3, column=2, pady=space_between_entries, padx=space_between_entries)
k2.grid(row=3, column=3, pady=space_between_entries, padx=space_between_entries)
l2.grid(row=3, column=4, pady=space_between_entries, padx=space_between_entries)

m2.grid(row=4, column=1, pady=space_between_entries, padx=space_between_entries)
n2.grid(row=4, column=2, pady=space_between_entries, padx=space_between_entries)
o2.grid(row=4, column=3, pady=space_between_entries, padx=space_between_entries)
p2.grid(row=4, column=4, pady=space_between_entries, padx=space_between_entries)

a2.configure(state="disabled", text_color=text_color_disabled)
b2.configure(state="disabled", text_color=text_color_disabled)
c2.configure(state="disabled", text_color=text_color_disabled)
d2.configure(state="disabled", text_color=text_color_disabled)

e2.configure(state="disabled", text_color=text_color_disabled)
f2.configure(state="disabled", text_color=text_color_disabled)
g2.configure(state="disabled", text_color=text_color_disabled)
h2.configure(state="disabled", text_color=text_color_disabled)

i2.configure(state="disabled", text_color=text_color_disabled)
j2.configure(state="disabled", text_color=text_color_disabled)
k2.configure(state="disabled", text_color=text_color_disabled)
l2.configure(state="disabled", text_color=text_color_disabled)

m2.configure(state="disabled", text_color=text_color_disabled)
n2.configure(state="disabled", text_color=text_color_disabled)
o2.configure(state="disabled", text_color=text_color_disabled)
p2.configure(state="disabled", text_color=text_color_disabled)

_4x4_kakunin = customtkinter.CTkButton(_4x4_mahoujin_frame, corner_radius=1, fg_color=text_color,
                                       text="確認", text_color="black", hover_color="#448038", command=lambda:_4x4_check())
_4x4_kakunin.grid(row=6, column=2, columnspan = 2)


# ============ Info Frame ============
info_frame.grid_rowconfigure(0, minsize=450)
info_frame.grid_rowconfigure(1, minsize=230)
info_frame.grid_columnconfigure(0, minsize=20)
info_frame.grid_columnconfigure(2, minsize=20)

manualfor3x3 = ""
if themechanger.get() == "白":
    highlight = text_color[1]
else:
    highlight = text_color[0]



help = customtkinter.CTkTextbox(info_frame, text_font=("MS Mincho", 14),
                              text_color=text_color_disabled_light, width=300, height=450,
                              fg_color=fg_color_entry, corner_radius=0)

help.tag_configure("bold", font="Mincho 14 bold", foreground=highlight)
help.insert("end", "     \n")
help.insert("end", "ゲームの説明\n", "bold")
help.insert("end", "     \n")
help.insert("end", "魔方陣とは〇×〇の正方形のマス目に数字を置いていき、縦、横、斜めのいずれにおいても、その列の合計が同じになるパズルである。\n", "")
help.insert("end", "     \n")
help.insert("end", "（その時使っていい数字は自然数であり各数字を入れられるのは一度だけです）\n", "")
help.insert("end", "     \n")
help.insert("end", "-------------------------------\n")
help.insert("end", "     \n")
help.insert("end", "アイコンの下にある")
help.insert("end", "モードチェンジ", "bold")
help.insert("end", "では3次魔方陣や４次魔法陣などモードの切り換えができる。\n")
help.insert("end", "     \n")
help.insert("end", "その下にある")
help.insert("end", "カラーチェンジ", "bold")
help.insert("end", "は黒と白の2色のモードの切り換えができます。\n")
help.insert("end", "     \n")
help.insert("end", "その下にある")
help.insert("end", "タイマー", "bold")
help.insert("end", "はスタートを押すことで自動的にタイムを測定し、終わったときのタイムを小数第2位まで出してくれます。\n")
help.insert("end", "     \n")
help.insert("end", "魔方陣に正解したときは")
help.insert("end", "正解", "bold")
help.insert("end", "と出て不正解だと")
help.insert("end", "やり直し", "bold")
help.insert("end", "と出て間違っているマスに赤色のエラーが出ます。\n")
help.insert("end", "     \n")
help.insert("end", "魔方陣の下にある")
help.insert("end", "確認", "bold")
help.insert("end", "は押すことで正解か不正解かを判定してくれます。")
help.insert("end", "エンター", "bold")
help.insert("end", "や")
help.insert("end", "スペース", "bold")
help.insert("end", "でも確認判定になるます。\n")
help.insert("end", "     \n")
help.insert("end", "説明の下にある")
help.insert("end", "難易度のバー", "bold")
help.insert("end", "は")
help.insert("end", "簡単、普通、難しい", "bold")
help.insert("end", "の三段階に分かれてます。\n")
help.insert("end", "     \n")
help.insert("end", "その下にある")
help.insert("end", "スタート", "bold")
help.insert("end", "は文字通り押すと開始されます。")
help.insert("end", "シフト", "bold")
help.insert("end", "でも同じ扱いになります。\n")
help.insert("end", "     \n")
help.insert("end", "説明の右隣りにある")
help.insert("end", "スコア値", "bold")
help.insert("end", "難易度に応じて目標タイムが設定され、")
help.insert("end", "プロ、１級、２級、３級", "bold")
help.insert("end", "の４段階に分かれています。上を目指して頑張ろう。\n")
help.insert("end", "     \n")
help.insert("end", "     \n")
help.insert("end", "(栃木県立小山高等学校\n")
help.insert("end", "数理科学科・課題研究\n")
help.insert("end", "柳田先生・\n")
help.insert("end", "古内　良汰、西本　光)\n")
help.insert("end", "     \n")
help.insert("end", "2023\n")
help.configure(state="disabled")
help.grid(row=0, column=1, columnspan= 1, sticky="nswe")





help_textbox_scrollbar = customtkinter.CTkScrollbar(info_frame, fg_color=fg_color_entry2,  height=430, command=help.yview)
help.configure(yscrollcommand=help_textbox_scrollbar.set)


help_textbox_scrollbar.grid(row=0, column=2, sticky="nse")

parameter_frame = customtkinter.CTkFrame(info_frame,
                                fg_color=fg_color_entry2,
                                width=300,
                                height=150,
                                corner_radius=0)
parameter_frame.grid(row=1, column=0, columnspan=3, padx=0, pady=0, sticky="nswe")


# ============ Parameter Frame/Section ============

parameter_frame.grid_rowconfigure(0, minsize=30)
parameter_frame.grid_rowconfigure(1, weight=1)
parameter_frame.grid_rowconfigure(2, weight=1)
parameter_frame.grid_rowconfigure(3, weight=1)
parameter_frame.grid_rowconfigure(4, minsize=10)
parameter_frame.grid_columnconfigure(1, weight=1)

difficulty = customtkinter.CTkLabel(parameter_frame, text="難易度: ", fg_color=fg_color_entry2, width=60)
difficulty_slider = customtkinter.CTkSlider(parameter_frame, button_color=text_color, from_=0, to=2, width=200, number_of_steps=2)
difficulty.grid(row=1, column=0, padx=20, pady=0)
difficulty_slider.grid(row=1, column=1, padx=0, pady=0, sticky="w")




_3x3_insert = customtkinter.CTkButton(parameter_frame, text="スタート",fg_color=text_color, hover_color="#448038", text_color="black", text_font=("MS Mincho", 10, "bold"),  command= lambda: _3x3_insertnumbers(difficulty_slider.get()))
_3x3_insert.grid(row=2, column=0, columnspan=2, padx=10, pady=0)

_4x4_insert = customtkinter.CTkButton(parameter_frame, text="スタート4x4",fg_color=text_color, hover_color="#448038", text_color="black", text_font=("MS Mincho", 10, "bold"),  command= lambda: _4x4_insertnumbers())

_3x3_show_hint = customtkinter.CTkCheckBox(parameter_frame, text="ヒント", hover_color=text_color, borderwidth=0.1, text_color=text_color, text_font=("MS Mincho", 10, "bold"), command=lambda:_3x3_show_tutorial(_3x3_show_hint.get()))
_3x3_show_hint.grid(row=3, column=0, columnspan=2, padx=20, pady=0, sticky="w")



# ============ Right Frame/Section ============

frame_right.grid_rowconfigure(0, minsize=10)
frame_right.grid_rowconfigure(5, weight=1)
frame_right.grid_rowconfigure(8, minsize=20)
frame_right.grid_rowconfigure(11, minsize=10)


quit = customtkinter.CTkButton(frame_right, text="✖", hover_color="#448038", fg_color=fg_color_entry, corner_radius=0, command=lambda:quit_window())
quit.grid(row=0, column=0, pady=10, padx=10)

settings = customtkinter.CTkButton(frame_right, text="⚙", hover_color="#448038", fg_color=fg_color_entry, corner_radius=0, command=lambda:manage_settings())
settings.grid(row=1, column=0, pady=10, padx=10)

ranking = customtkinter.CTkTextbox(frame_right, text_font=("MS Mincho", 14),
                              text_color=text_color_disabled_light, width=150,
                              fg_color=fg_color_entry, corner_radius=0)
ranking.tag_configure("bold", font="Mincho 14 bold", foreground=highlight)
ranking.tag_configure("rank1", font="Mincho 14", foreground=Ranking[0])
ranking.tag_configure("rank2", font="Mincho 14", foreground=Ranking[1])
ranking.tag_configure("rank3", font="Mincho 14", foreground=Ranking[2])
ranking.tag_configure("rank4", font="Mincho 14", foreground=Ranking[3])

ranking.insert("end", "段位\n", "bold")
ranking.insert("end", "\n")
ranking.insert("end", " 簡単\n", "bold")
ranking.insert("end", " プロ: ", "rank1")
ranking.insert("end", "5秒以内\n")
ranking.insert("end", " 1級: ", "rank2")
ranking.insert("end", "5⁓10秒\n")
ranking.insert("end", " 2級: ", "rank3")
ranking.insert("end", "10⁓30秒\n")
ranking.insert("end", " 3級: ", "rank4")
ranking.insert("end", "30秒以上\n")
ranking.insert("end", " \n")
ranking.insert("end", " 普通\n", "bold")
ranking.insert("end", " プロ: ", "rank1")
ranking.insert("end", "7秒以内\n")
ranking.insert("end", " 1級: ", "rank2")
ranking.insert("end", "7⁓10秒\n")
ranking.insert("end", " 2級: ", "rank3")
ranking.insert("end", "10⁓20秒\n")
ranking.insert("end", " 3級: ", "rank4")
ranking.insert("end", "20秒以上\n")
ranking.insert("end", " \n")
ranking.insert("end", " 難しい\n", "bold")
ranking.insert("end", " プロ: ", "rank1")
ranking.insert("end", "10秒以内\n")
ranking.insert("end", " 1級: ", "rank2")
ranking.insert("end", "10⁓12秒\n")
ranking.insert("end", " 2級: ", "rank3")
ranking.insert("end", "12⁓14秒\n")
ranking.insert("end", " 3級: ", "rank4")
ranking.insert("end", "14秒以上\n")

ranking.configure(state="disabled")

ranking.grid(row=2, column=0, rowspan=9,pady=40,padx=20, sticky="ns")




# ============ Key Inputs ============


def _3x3_up(event):
    global _3x3_selected_entry_index, _3x3_key_matrix, _3x3_index_for_chosen_mahoujin
    new_matrix = list(_3x3_key_matrix)
    selected_entry = new_matrix[_3x3_selected_entry_index]
    if _3x3_selected_entry_index >= 3:
        exec(str(selected_entry) + ".configure(fg_color=fg_color_entry)")
    else:
        pass
    if _3x3_selected_entry_index in index_for_chosen_mahoujin: #if the mahoujin before was for the player
        exec(str(selected_entry) + ".configure(text_color=text_color_disabled)")
    else:
        exec(str(selected_entry) + ".configure(text_color=text_color)")

    if _3x3_selected_entry_index < 3:
        exec(str(selected_entry) + ".configure(text_color=text_color_disabled)")
    else:
        pass

    if _3x3_selected_entry_index >= 3: #if
        _3x3_selected_entry_index -= 3
        selected_entry = new_matrix[_3x3_selected_entry_index]
        exec(str(selected_entry) + ".focus()")
        exec(str(selected_entry) + ".configure(fg_color=text_color)")
        exec(str(selected_entry) + ".configure(text_color=text_color_disabled)")
        return
    else:
        return

def _3x3_down(event):
    global _3x3_selected_entry_index, _3x3_key_matrix, _3x3_index_for_chosen_mahoujin
    new_matrix = list(_3x3_key_matrix)
    selected_entry = new_matrix[_3x3_selected_entry_index]
    if _3x3_selected_entry_index <= 5:
        exec(str(selected_entry) + ".configure(fg_color=fg_color_entry)")
    else:
        pass
    if _3x3_selected_entry_index in index_for_chosen_mahoujin:
        exec(str(selected_entry) + ".configure(text_color=text_color_disabled)")
    else:
        exec(str(selected_entry) + ".configure(text_color=text_color)")

    if _3x3_selected_entry_index > 5:
        exec(str(selected_entry) + ".configure(text_color=text_color_disabled)")
    else:
        pass

    if _3x3_selected_entry_index <= 5:
        _3x3_selected_entry_index += 3
        selected_entry = new_matrix[_3x3_selected_entry_index]
        exec(str(selected_entry) + ".focus()")
        exec(str(selected_entry) + ".configure(fg_color=text_color)")
        exec(str(selected_entry) + ".configure(text_color=text_color_disabled)")
        return
    else:
        return

def _3x3_right(event):
    global _3x3_selected_entry_index, _3x3_key_matrix, _3x3_index_for_chosen_mahoujin
    new_matrix = list(_3x3_key_matrix)
    selected_entry = new_matrix[_3x3_selected_entry_index]
    if _3x3_selected_entry_index % 3 != 2:
        exec(str(selected_entry) + ".configure(fg_color=fg_color_entry)")
    else:
        pass
    if _3x3_selected_entry_index in index_for_chosen_mahoujin:
        exec(str(selected_entry) + ".configure(text_color=text_color_disabled)")
    else:
        exec(str(selected_entry) + ".configure(text_color=text_color)")

    if not _3x3_selected_entry_index % 3 != 2:
        exec(str(selected_entry) + ".configure(text_color=text_color_disabled)")
    else:
        pass

    if _3x3_selected_entry_index % 3 != 2:
        _3x3_selected_entry_index += 1
        selected_entry = new_matrix[_3x3_selected_entry_index]
        exec(str(selected_entry) + ".focus()")
        exec(str(selected_entry) + ".configure(fg_color=text_color)")
        exec(str(selected_entry) + ".configure(text_color=text_color_disabled)")
    else:
        return

def _3x3_left(event):
    global _3x3_selected_entry_index, _3x3_key_matrix, _3x3_index_for_chosen_mahoujin
    new_matrix = list(_3x3_key_matrix)
    selected_entry = new_matrix[_3x3_selected_entry_index]
    if _3x3_selected_entry_index % 3 != 0:
        exec(str(selected_entry) + ".configure(fg_color=fg_color_entry)")
    else:
        pass
    if _3x3_selected_entry_index in index_for_chosen_mahoujin:
        exec(str(selected_entry) + ".configure(text_color=text_color_disabled)")
    else:
        exec(str(selected_entry) + ".configure(text_color=text_color)")

    if not _3x3_selected_entry_index % 3 != 0:
        exec(str(selected_entry) + ".configure(text_color=text_color_disabled)")
    else:
        pass

    if _3x3_selected_entry_index % 3 != 0:
        _3x3_selected_entry_index -= 1
        selected_entry = new_matrix[_3x3_selected_entry_index]
        exec(str(selected_entry) + ".focus()")
        exec(str(selected_entry) + ".configure(fg_color=text_color)")
        exec(str(selected_entry) + ".configure(text_color=text_color_disabled)")
    else:
        return


def shift_press(event):
    _3x3_insertnumbers(difficulty_slider.get())
    return


def _3x3_wasd(event):
    if event.char == "w":
        _3x3_up("")
    elif event.char == "s":
        _3x3_down("")
    elif event.char == "d":
        _3x3_right("")
    elif event.char == "a":
        _3x3_left("")
    else:
        pass
    return


def _3x3_reset_colors(event):
    a1.configure(fg_color=fg_color_entry)
    b1.configure(fg_color=fg_color_entry)
    c1.configure(fg_color=fg_color_entry)

    d1.configure(fg_color=fg_color_entry)
    e1.configure(fg_color=fg_color_entry)
    f1.configure(fg_color=fg_color_entry)

    g1.configure(fg_color=fg_color_entry)
    h1.configure(fg_color=fg_color_entry)
    i1.configure(fg_color=fg_color_entry)


window.bind("<Up>", _3x3_up)
window.bind("<Down>", _3x3_down)
window.bind("<Right>", _3x3_right)
window.bind("<Left>", _3x3_left)
window.bind("<KeyPress-Shift_L>", shift_press)



window.bind("<w>", _3x3_wasd)
window.bind("<a>", _3x3_wasd)
window.bind("<s>", _3x3_wasd)
window.bind("<d>", _3x3_wasd)

window.bind("<space>", lambda event: _3x3_check())
window.bind("<Return>", lambda event: _3x3_check())

window.bind("<Button-1>", _3x3_reset_colors)


#=======================================================================================================================

window.mainloop()






