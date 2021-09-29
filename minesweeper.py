import tkinter, configparser, random, os, tkinter.messagebox, tkinter.simpledialog
import time
window = tkinter.Tk()
window.title('Minesweeper')
start_window=tkinter.Tk()
start_window.title('Minesweeper')
buttons = []
board = [[]]
size=-1
ratio=0
num_bombs = 0
num_clicked = 0

def addButtons():
    global board
    global size
    for row in range(size):
        for col in range(size):
            button = tkinter.Label(window, text=(board[row][col]), fg = window.cget('bg'), relief = 'raised', width = 2)
            label_num = str(button).replace('.!label', '')
            if label_num=='': label_num='1'
            buttons.append([label_num,str(row)+'/'+str(col)])
            button.bind('<Button-1>', left_click)
            button.bind('<Button-2>', right_click)
            button.bind('<Button-3>', right_click)
            button.grid(row=row, column=col)
    print(buttons)


def left_click(event):
    global size
    checked = [[0 for x in range(size)]for y in range(size)]
    left_click_helper(event.widget, checked)

def left_click_helper(widget, checked):
    global board
    global num_clicked
    if int(widget.cget('text'))==-1:
        widget.configure(bg = 'red', text='x', fg='black', relief='sunken')
        hahaloser = tkinter.Label(window, text = 'lmao fkin loser, bye', bg='red')
        hahaloser.place(relx=0.5,rely=0.5, anchor='center')
        window.after(5000, endgame)

    if int(widget.cget('text'))>=0:
        num_clicked+=1
        print('clicked on '+str(widget)+': num_clicked='+str(num_clicked))
        widget.configure(bg = window.cget('bg'), fg='black', relief='sunken')
        if num_clicked==size**2-num_bombs:
            hahawinner = tkinter.Label(window, text = 'you win smart boi!', bg='green')
            hahawinner.place(relx=0.5,rely=0.5, anchor='center')
            window.after(5000, endgame)
        if int(widget.cget('text'))>=1:
            return
    else:
        return
    label_num = str(widget).replace('.!label', '')
    if label_num=='': label_num='1'
    for index in range(len(buttons)):
        if buttons[index][0] == label_num:
            pos = buttons[index][1].split('/')
    row = int(pos[0])
    col = int(pos[1])
    checked[row][col]=-2
    for x in range(row-1, row+2):
        for y in range(col-1, col+2):
            if (0<=x<size and 0<=y<size) and checked[x][y]!=-2:
                checked[x][y]=-2
                if board[x][y]>=0:
                    for i in range(len(buttons)):
                        grid_num = str(x*size+y+1)
                        if buttons[i][0]==grid_num:
                            if grid_num=='1': grid_num=''
                            next = window.nametowidget(name = '.!label' + grid_num)
                            next.configure(bg = 'blue')
                            left_click_helper(next,checked)


def right_click(event):
    if event.widget.cget('relief')!='sunken':
        event.widget.configure(bg='red', fg='red')

def endgame():
    quit()


def prepare_board():
    global board
    global num_bombs
    global ratio
    ##create board
    board = [[0 for x in range(size)] for y in range(size)]

    num_bombs = int(size**2/ratio)
    x_positions = random.sample(range(0,size**2), num_bombs)
    y_positions = random.sample(range(0,size**2), num_bombs)
    positions = [[x_positions[i]%size, y_positions[i]%size] for i in range(num_bombs)]
    for pos in positions:
        board[pos[0]][pos[1]] = -1

    #add numbers
    for row in range(size):
        for col in range(size):
            if board[row][col] == -1:
                for x in range(row-1, row+2):
                    for y in range(col-1, col+2):
                        if not (row==x and col==y) and (0<=x<size and 0<=y<size) and board[x][y]!=-1:
                            board[x][y] = board[x][y]+1
    addButtons()

def retrieve(button, input, prompt):
    global size
    global ratio
    if size<0:
        size=int(input.get())
        input.delete(0,'end')
        prompt.configure(text='How many free tiles do you want per bomb? (less than board size^2)')
    else:
        ratio=int(input.get())
        button.destroy()
        input.destroy()
        prompt.destroy()
        start_window.destroy()
        prepare_board()
        window.mainloop()

def start_game():
    get_input=tkinter.Entry(start_window)
    get_input_prompt=tkinter.Label(start_window, text='How big do you want the board to be? (1 number)?')
    enter=tkinter.Button(start_window, text='Enter', command=lambda: retrieve(enter, get_input, get_input_prompt))

    get_input_prompt.grid(row=1,column=0)
    get_input.grid(row=2,column=0)
    enter.grid(row=3,column=0)
    start_window.mainloop()


start_game()
