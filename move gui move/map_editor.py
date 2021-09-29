import numpy
from tkinter import Tk, Button, Entry, filedialog, StringVar, Label
import move_gui_move

class Board():
    def __init__(self, board_x, board_y):
        self.board_x = board_x 
        self.board_y = board_y 
        self.board_size = (board_x,board_y)
        self.board = numpy.zeros(self.board_size, dtype=numpy.int8)

    def clear_board(self):
        self.board = numpy.zeros(self.board_size, dtype=numpy.int8)

class Editor():
    def __init__(self):
        self.window = Editor.create_editor_window()
        self.placeable_objects = Editor.get_placeable_objects()
        self.selected_object = 'None'
        self.grid_buttons = []
        self.option_buttons = None
        self.name_entry = None
        self.level_name = None

    def get_placeable_objects():
        placeable_objects = [cls.__name__ for cls in move_gui_move.Game_Object.__subclasses__()]
        placeable_objects.insert(0, 'empty')
        return placeable_objects

    def create_editor_window():
        window = Tk()
        window.title('Map Editor')
        window.geometry('+100+0')
        return window

def color_button(button):
    color_dict = {'Wall':"light green",
                  'Pushed': "red",
                  'Push_Object': "blue",
                  'Switcher': "white",
                  'Diagonal':"light blue",
                  'Home_Base':"pink",
                  'Player':"green",
                  'X_Mover':"orange",
                  'Y_Mover':"purple",
                  'Jumper':"grey",
                  'empty': "black"}
    button['bg'] = color_dict[button['text']]

def create_grid_buttons():
    b = 0
    buttons = []
    for x in range(board.board_x):
        for y in range(board.board_y):
            b += 1
            buttons.append(
            Button(editor.window, text='empty', bg='black', borderwidth=1, height=3, width=11, 
                    command= lambda num=b-1: become_object(num)))
            buttons[-1].grid(row = x, column = y)
    return buttons

def create_option_buttons():
    option_buttons = []
    for option in enumerate(editor.placeable_objects):
        option_buttons.append(
            Button(editor.window, text=str(option[1]), borderwidth=1, height=3, width=11,
                     command= lambda num=option[0]: select(num)))
        color_button(option_buttons[-1])
        option_buttons[-1].grid(row = option[0], column = 10)

    create_button = Button(editor.window, text='Create', bg='white', borderwidth=1, command= lambda : create_level(board))
    clear_button = Button(editor.window, text='Clear', bg='white', borderwidth=1, command= lambda : clear_level())
    save_button = Button(editor.window, text='Save', borderwidth=1, command= lambda : save_level())
    load_button = Button(editor.window, text='Load', bg='white', borderwidth=1, command= lambda : load_level())

    level_name = StringVar()
    editor.name_label = Label(editor.window, text = 'Level Name', font=('calibre',10, 'bold'))
    editor.name_entry = Entry(editor.window,textvariable = level_name, font=('calibre',10, 'bold'))

    create_button.grid(row = 11, column = len(editor.placeable_objects)-3)
    clear_button.grid(row = 11, column = len(editor.placeable_objects)-4)
    load_button.grid(row = 11, column = len(editor.placeable_objects)+1)
    editor.name_label.grid(row = 11, column = len(editor.placeable_objects)-2)
    editor.name_entry.grid(row = 11, column = len(editor.placeable_objects)-1)
    save_button.grid(row = 11, column = len(editor.placeable_objects))
    return option_buttons

def select(button):
    editor.selected_object = editor.option_buttons[button]

def become_object(button):
    if editor.selected_object['text'] == 'None': return
    editor.grid_buttons[button]['text'] = editor.selected_object['text']
    editor.grid_buttons[button]['bg'] = editor.selected_object['bg']
    x,y = editor.grid_buttons[button].grid_info()['row'], editor.grid_buttons[button].grid_info()['column']
    board.board[x][y] = editor.placeable_objects.index(editor.grid_buttons[button]['text']) 

def save_level():
    name = editor.name_entry.get()  
    numpy.save(f'{name}', board.board)
    print(f'saved level {name}.npy to current directory')
    editor.level_name.set('')

def load_level():
    clear_level()
    file = filedialog.askopenfilename(initialdir= "\\Users\win 10\Desktop\mapmap\python\moveguimovelevels",
                                      title     = "Select a File",
                                      filetypes = (('numpy files', '*.npy'),('All files', '*.*')))
    if not file: return
    board.board = numpy.load(file)
    create_level(board)
    
def clear_level():
    Board.clear_board(board)
    for button in editor.grid_buttons:
        button['text'] = 'empty'
        button['bg'] = 'black'
    move_gui_move.Game.clear_canvas(move_gui_move.game)
    move_gui_move.game.object_dict = {}

def create_level(board):
    move_gui_move.Game.clear_canvas(move_gui_move.game)
    move_gui_move.game.object_dict = {}
    for row in range(board.board_x):
        for column in range(board.board_y):
            y_pos = column*50
            x_pos = row*50
            create_object(board.board[row][column], x_pos, y_pos)
    print(move_gui_move.game.object_dict)
    key_list = list(move_gui_move.game.object_dict.keys())
    for key in key_list:
        if type(move_gui_move.game.object_dict[key]) == move_gui_move.Player:
            player_1 = move_gui_move.game.object_dict[key]

    move_gui_move.game.canvas.tag_raise('player')

    move_gui_move.game.window.bind("<KeyPress-Left>",  lambda e: move_gui_move.Player.left( player_1))
    move_gui_move.game.window.bind("<KeyPress-Right>", lambda e: move_gui_move.Player.right(player_1))
    move_gui_move.game.window.bind("<KeyPress-Up>",    lambda e: move_gui_move.Player.up(   player_1))
    move_gui_move.game.window.bind("<KeyPress-Down>",  lambda e: move_gui_move.Player.down( player_1))

    move_gui_move.game.window.bind("a", lambda e: move_gui_move.Player.left( player_1))
    move_gui_move.game.window.bind("d", lambda e: move_gui_move.Player.right(player_1))
    move_gui_move.game.window.bind("w", lambda e: move_gui_move.Player.up(   player_1))
    move_gui_move.game.window.bind("s", lambda e: move_gui_move.Player.down( player_1))

    move_gui_move.game.window.bind("R", lambda e: move_gui_move.Game_Object.reset())

def create_object(object_number, y_pos, x_pos):
    index = int(object_number)
    button_grid = numpy.array(editor.grid_buttons).reshape(10,10)
    if editor.placeable_objects[index] == 'empty': return # or choose another default object
        #move_gui_move.Diagonal(x_pos, y_pos, x_pos+48, y_pos+48, fill = "light blue", tags= "diagonal")
    if editor.placeable_objects[index] == 'Wall':
        move_gui_move.Wall(x_pos, y_pos, x_pos+48, y_pos+48, fill = "light green", tags= "wall")
    if editor.placeable_objects[index] == 'Pushed':
        move_gui_move.Pushed(x_pos, y_pos, x_pos+48, y_pos+48, fill = "red", tags= "pushed")
    if editor.placeable_objects[index] == 'Push_Object':
        move_gui_move.Push_Object(x_pos, y_pos, x_pos+48, y_pos+48, fill = "blue", tags= "push")
    if editor.placeable_objects[index] == 'Switcher':
        move_gui_move.Switcher(x_pos, y_pos, x_pos+48, y_pos+48, fill = "white", tags= "switcher")
    if editor.placeable_objects[index] == 'Diagonal':
        move_gui_move.Diagonal(x_pos, y_pos, x_pos+48, y_pos+48, fill = "light blue", tags= "diagonal")
    if editor.placeable_objects[index] == 'Home_Base':
         move_gui_move.Home_Base(x_pos, y_pos, x_pos+48, y_pos+48, fill = "pink", tags= "home base")
    if editor.placeable_objects[index] == 'Player':
        move_gui_move.Player(x_pos, y_pos, x_pos+48, y_pos+48, fill = "green", tags= "player")
    if editor.placeable_objects[index] == 'X_Mover':
        move_gui_move.X_Mover(x_pos, y_pos, x_pos+48, y_pos+48, fill = "orange", tags= "x_mover")
    if editor.placeable_objects[index] == 'Y_Mover':
        move_gui_move.Y_Mover(x_pos, y_pos, x_pos+48, y_pos+48, fill = "purple", tags= "y_mover")
    if editor.placeable_objects[index] == 'Jumper':
        move_gui_move.Jumper(x_pos, y_pos, x_pos+48, y_pos+48, fill = "grey", tags= "jumper")
    button = button_grid[int(y_pos/50)][int(x_pos/50)]
    button['text'] = editor.placeable_objects[index]
    color_button(button)

if __name__ == '__main__':
    board = Board(10,10)
    editor = Editor()
    editor.grid_buttons = create_grid_buttons()
    editor.option_buttons = create_option_buttons()
    editor.window.mainloop()