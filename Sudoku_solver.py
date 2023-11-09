import tkinter as tk
from tkinter import messagebox

#create window
window = tk.Tk()
window.title("Sudoku Solver")
x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2
y = (window.winfo_screenheight() - window.winfo_reqheight()) / 2
window.geometry("+%d+%d" % (x, y-200))

#create main frame
main_frame = tk.LabelFrame(window)
main_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=5)

#create 9x9 frames
frames = []
for i in range(3):
    for j in range(3):
        frame = tk.LabelFrame(main_frame)
        frame.grid(row=i, column=j)
        frames.append(frame)

#validate input function
def validate_input(input_string):
    if input_string.isdigit() and int(input_string) in range(1, 10):
        return True
    elif input_string == '':
        return True
    else:
        return False

#create boxes for input
cells = []
for i in range(9):
    for j in range(9):
        frame = frames[int(i / 3) * 3 + int(j / 3)]
        cell = tk.Entry(frame, width=3, justify = tk.CENTER, validate="key", validatecommand=(window.register(validate_input), '%P'))
        cell.grid(row=i % 3, column=j % 3)
        cells.append(cell)

#move with arrows
def move_focus(event):
    current_cell = event.widget
    current_index = cells.index(current_cell)
    row = int(current_index / 9)
    col = int(current_index % 9)
    if event.keysym == 'Right':
        next_index = current_index + 1 if col < 8 else current_index - 8
    elif event.keysym == 'Left':
        next_index = current_index - 1 if col > 0 else current_index + 8
    elif event.keysym == 'Down':
        next_index = current_index + 9 if row < 8 else current_index - 72
    elif event.keysym == 'Up':
        next_index = current_index - 9 if row > 0 else current_index + 72
    next_cell = cells[next_index]
    next_cell.focus_set()

for cell in cells:
    cell.bind("<Right>", move_focus)
    cell.bind("<Left>", move_focus)
    cell.bind("<Up>", move_focus)
    cell.bind("<Down>", move_focus)

#write values in array
arr = [[0]*9 for _ in range(9)]
def write_in_arr():
    for a in range(81):
        x = int(a/9)
        y = int(a%9)
        value = cells[a].get()
        arr[x][y] = 0
        if(value != ''):
            if(correctPosition(x, y, int(value))):
                arr[x][y] = -int(value)
            else:
                messagebox.showinfo("Error", "Invalid input")
                return False
    return True

#write output
def write():
    for a in range(81):
        value = arr[int(a/9)][int(a%9)]
        if(value > 0):
            cells[a].delete(0,tk.END)
            cells[a].insert(0, value)
        else:
            cells[a].configure(bg = 'LightBlue')

#backtracking algorithm
solutionNum = 0
x = 0
y = 0
flag = 1

def checkFrame(i, j, value):
    row = int(i/3)*3
    column = int(j/3)*3
    for x in range(row, row+3):
        for y in range(column, column+3):
            if(abs(arr[x][y]) == value):
                return False
    return True

def checkColumn(y, value):
    for x in range(9):
        if(abs(arr[x][y]) == value):
            return False
    return True

def checkRow(x, value):
    for y in range(9):
        if(abs(arr[x][y]) == value):
            return False
    return True
        
def correctPosition(x, y, value):
    ok1 = checkFrame(x, y, value)
    ok2 = checkRow(x, value)
    ok3 = checkColumn(y, value)
    if(ok1 and ok2 and ok3):
        return True
    return False

def changePrevious():
    global x
    global y
    global flag
    if(y == 0):
        x-=1
        y=8
    else:
        y-=1
    if(arr[x][y] > 0):
        if(arr[x][y] < 9):
            ok = 0
            for value in range(arr[x][y]+1, 10):
                if(correctPosition(x, y, value)):
                    arr[x][y] = value
                    ok = 1
                    return
            if(ok==0):
                if(x != 0 or y != 0):
                    arr[x][y] = 0
                    changePrevious()
                else:
                    flag = 0
                    return
        else:
            if(x != 0 or y != 0):
                arr[x][y] = 0
                changePrevious()
            else:
                flag = 0
                return
    else:
        if(x != 0 or y != 0):
            changePrevious()
        else:
            flag = 0
            return

def solve(): 
    global x
    global y
    global flag
    global solutionNum
    while(x < 9):
        y = 0
        while(y < 9):
            if(arr[x][y] == 0):
                ok = 0
                for value in range(1, 10):
                    if(correctPosition(x, y, value)):
                        arr[x][y] = value
                        ok = 1
                        break
                if(ok == 0):
                    if(x != 0 or y != 0):
                        changePrevious()
                    if(flag == 0):
                        return
            if(x == 8 and y == 8):
                solutionNum+=1
                if(solutionNum > 1):
                    response = messagebox.askyesno("Confirmation", "There are more solutions available. \n Do you want to continue?")
                    if response:
                        write()
                        y+=1
                        changePrevious()
                    else:
                        return
                else:
                    write()
                    y+=1
                    changePrevious()
            if(flag == 0):
                return
            y+=1
        x+=1


#solve button
def solve_button():
    ok = write_in_arr()
    if(ok == 0):
        return
    solve()
b = tk.Button(window, text = "Solve", command=lambda: solve_button())
b.grid(row=1, column=0, padx=10, pady=10, sticky="w")

#reset button
def reset():
    global x
    global y
    global solutionNum
    global flag
    x = 0
    y = 0
    solutionNum = 0
    flag = 1
    for i in range(81):
        cells[i].delete(0,tk.END)
        cells[i].configure(bg = 'White')
        arr[int(i/9)][int(i%9)] = 0


reset_button = tk.Button(window, text = "Reset", command=reset)
reset_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

window.mainloop()    
