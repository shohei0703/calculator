import PySimpleGUI as sg
import math

# サイズとフォントは使い回すので変数で設定
size = (4, 2)
font = ('Arial', 20)

# 以下グローバル変数の設定
displayed_num = 0 # 表示される数字
holded_num = 0 # 演算子を押す前に作成した数字
decimal_point = 1 # 小数点第何位か
decimal_flag = False # 少数フラグ（False =整数）
memory = 0 # メモリー

# 四則演算子または[=]を押すまで数字キーを押すごとに桁数を増やしながら数字を並べる関数
def stack_num(number):
    # グローバル変数の宣言をしないとdisplayed_numがローカル変数扱いされてしまう
    global displayed_num
    displayed_num = displayed_num * 10 + number
    return displayed_num

# 数字キーを押すごとに小数点以下の数字を並べていく関数
def add_decimal(number):
    # グローバル変数の宣言をしないとdisplayed_numがローカル変数扱いされてしまう
    global displayed_num, decimal_point
    displayed_num = displayed_num + number * 1 / 10**decimal_point 
    decimal_point += 1
    return displayed_num

# 表示される数、小数点第何位、小数点フラグの３つの変数をリセットする関数
# (使いまわすためコードが長くなるので関数にした）
def reset_var():
    global displayed_num, decimal_point, decimal_flag
    displayed_num = 0
    decimal_flag = False
    decimal_point = 1

# 表示される数、小数点第何位、小数点フラグの３つの変数をリセットする関数
def off_var():
    global displayed_num, decimal_point, decimal_flag
    displayed_num = ''
    decimal_flag = False
    decimal_point = 1

# 税抜計算
def calculate_tax_exclusive():
    global displayed_num
    displayed_num *= 0.9
    window['-出力-'].update(displayed_num)

# 税込計算
def calculate_tax_inclusive():
    global displayed_num
    displayed_num *= 1.1
    window['-出力-'].update(displayed_num)

# 時間計算
def calculate_time():
    try:
        hours = int(displayed_num // 60)
        minutes = int(displayed_num % 60)
        result = f"{hours:02d}:{minutes:02d}"
        window['-出力-'].update(result)
    except ValueError:
        window['-出力-'].update("Error")

# メモリー機能
def memory_plus():
    global memory, displayed_num
    memory += displayed_num

def memory_minus():
    global memory, displayed_num
    memory -= displayed_num

def memory_recall():
    global memory, displayed_num
    displayed_num = memory
    window['-出力-'].update(displayed_num)

def memory_clear():
    global memory
    memory = 0      

# ウィンドウ表示画面
layout = [[sg.Text(' CASIO', font=font, background_color='snow3', text_color='black')],
          
          [sg.Text(key='-出力-', font=('Arial', 50), size=(12, 1), text_color='black', 
                   justification='right', background_color='alice blue', relief=sg.RELIEF_SOLID)],
          
           [sg.Button("",visible=False),
            sg.Button("",visible=False),
            sg.Button("",visible=False),
            sg.Button("",visible=False),
            sg.Button('税抜',size=size, font=font, key='税抜',button_color=('black', 'medium aquamarine')),
            sg.Button('税込',size=size, font=font, key='税込',button_color=('black', 'medium aquamarine'))],
          
          [sg.Button('時間\n計算',size=size, font=font, key='時間計算',button_color=('white', 'LightSlateBlue')),
           sg.Button('M+',size=size, font=font, key='M+'),
           sg.Button('M-',size=size, font=font, key='M-'),
           sg.Button('MR',size=size, font=font, key='MR'),
           sg.Button('MC',size=size, font=font, key='MC'),
           sg.Button('GT',size=size, font=font, key='GT')],
          
          [sg.Button("AC",size=size, font=font, key="AC"),
           sg.Button(7,size=size, font=font, key=7,button_color=('black', 'gray70')),
           sg.Button(8,size=size, font=font, key=8,button_color=('black', 'gray70')),
           sg.Button(9,size=size, font=font, key=9,button_color=('black', 'gray70')),
           sg.Button("%",size=size, font=font, key="%"),
           sg.Button('√',size=size, font=font, key='√')],
          
          [sg.Button("+/-",size=size, font=font, key="+/-"),
           sg.Button(4,size=size, font=font, key=4,button_color=('black', 'gray70')),
           sg.Button(5,size=size, font=font, key=5,button_color=('black', 'gray70')),
           sg.Button(6,size=size, font=font, key=6,button_color=('black', 'gray70')),
           sg.Button('×',size=size, font=font, key='*'),
           sg.Button('÷',size=size, font=font, key='/')],
            
          [sg.Button("R",size=size, font=font, key="R"),
           sg.Button(1,size=size, font=font, key=1,button_color=('black', 'gray70')),
           sg.Button(2,size=size, font=font, key=2,button_color=('black', 'gray70')),
           sg.Button(3,size=size, font=font, key=3,button_color=('black', 'gray70')),
           sg.Button('',size=size, font=font, key=''),
           sg.Button('-',size=size, font=font, key='-')],
            
          [sg.Button('C',size=size, font=font, key='C',button_color=('black', 'PaleVioletRed2')),
           sg.Button(0,size=size, font=font, key=0,button_color=('black', 'gray70')),
           sg.Button("00",size=size, font=font, key="00",button_color=('black', 'gray70')),
           sg.Button('.',size=size, font=font, key='.',button_color=('black', 'gray70')),
           sg.Button('+',size=size, font=font, key='+'),
           sg.Button('=',size=size, font=font, key='=')]]

window = sg.Window('CASIO', layout=layout, margins=(30, 30),resizable=True, 
                   button_color=('black', 'white'),background_color='snow3')
          
while True:
    
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    # 数字キーを押すと小数点以下に数字が表示されるようにするためのフラグの変更
    elif event == '.':
        decimal_flag = True

    # 数字キーを押した場合は、小数点か判断してstack_num関数またはadd_decimal関数を呼び出す
    elif event in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
        # 表示されている数字が少数かどうかで呼び出す関数を変える
        if decimal_flag == False:
            displayed_num = stack_num(event)
        elif displayed_num == '':
            displayed_num = add_decimal(event)
        else: 
            displayed_num = add_decimal(event)
        window['-出力-'].update(displayed_num)

    # 1回目の四則演算子キーを押下時(holded_numが0)はまだ計算しない。
    # 2回目以降、四則演算子キーの押下時(holded_numが0ではない)一旦計算し、
    # operatorsを新しい四則演算子で更新しておく
    elif event in ['/', '*', '-', '+']:
        if holded_num == 0:
            holded_num = displayed_num
            reset_var()
            operators = event
        else:
            if operators == '/':
                holded_num = holded_num / displayed_num
                operators = event
                reset_var()
            elif operators == '*':
                holded_num = holded_num * displayed_num
                operators = event
                reset_var()
            elif operators == '-':
                holded_num = holded_num - displayed_num
                operators = event
                reset_var()
            elif operators == '+':
                holded_num = holded_num + displayed_num
                operators = event
                reset_var()
        window['-出力-'].update(holded_num)

    # [=]キーを押した場合は、表示はholded_numの値を表示し、displayed_numを0にしてリセットしておく
    elif event in ['=']:
        if holded_num == 0:
            holded_num = displayed_num
            reset_var()
        else:
            if operators == '/':
                holded_num = holded_num / displayed_num
                reset_var()
            elif operators == '*':
                holded_num = holded_num * displayed_num
                reset_var()
            elif operators == '-':
                holded_num = holded_num - displayed_num
                reset_var()
            elif operators == '+':
                holded_num = holded_num + displayed_num
                reset_var()
        window['-出力-'].update(holded_num)
        holded_num = 0
  
  
    elif event == 'M+':
        memory_plus()

    # `M-` ボタンを押すと、メモリーから現在表示されている数字を減算する
    elif event == 'M-':
        memory_minus()
  
    # `MR` ボタンを押すと、メモリーに保存されている値を画面に表示する
    elif event == 'MR':
        memory_recall()

    # `MC` ボタンを押すと、メモリーをクリアする
    elif event == 'MC':
        memory_clear()

    # `GT` ボタンを押すと、メモリーに保存されている値を画面に表示し、さらにその値で計算を続行する
    elif event == 'GT':
        try:
            memory_recall()
            window['-出力-'].update(holded_num)
        except TypeError:
            window['-出力-'].update("Error")

    # `√` ボタンを押した場合は、`math.sqrt()` 関数を使って平方根を計算し、
    # `holded_num` と `displayed_num` を更新します。
    elif event == '√':
        try:
            result = math.sqrt(displayed_num)
            holded_num = result
            reset_var()
            window['-出力-'].update(holded_num)
        
        except ValueError:
            window['-出力-'].update("Error")
 
    # 税抜計算
    elif event == '税抜':
        calculate_tax_exclusive()

    # 税込計算
    elif event == '税込':
        calculate_tax_inclusive()
    
    # clearキーを押した場合、全てリセットさせ0を表示する
    elif event in ['C']:
        holded_num = 0
        operators = ''
        reset_var()
        window['-出力-'].update(displayed_num)
    
    # ACキーを押した場合、全てリセットさせ非表示にする
    elif event in ['AC']:
        holded_num = 0
        operators = ''
        off_var()
        window['-出力-'].update(displayed_num)
    


# 画面から削除して終了
window.close()