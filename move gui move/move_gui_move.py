import tkinter

class Game(): 

    def __init__(self):
        self.height = 500
        self.width  = 500
        self.window = Game.create_window()
        self.canvas = Game.create_canvas(self.window, self.height, self.width)
        self.object_dict = {}
        self.already_won = False

    def create_window():
        window = tkinter.Tk()
        window.title('Move GUI Move')
        window.geometry('+100+0')
        return window

    def create_canvas(window, height, width):
        canvas = tkinter.Canvas(window, bg="black", height=height, width=width)
        canvas.pack()
        return canvas

    def clear_canvas(game):
        global object_dict
        game.canvas.delete("all")

class Game_Object():

    def __init__(self, x0, x1, y0, y1, **kwargs):
        self.rectangle              = game.canvas.create_rectangle(x0, x1, y0, y1, **kwargs)
        self.x0                     = x0
        self.x1                     = x1
        self.y0                     = y0
        self.y1                     = y1
        self.tags                   = game.canvas.gettags(self.rectangle)
        self.fill                   = game.canvas.itemcget(self.rectangle, "fill")
        self.start_position         = game.canvas.bbox(self.rectangle)
        self.collider_object        = None
        game.object_dict[self.rectangle] = self

    def __repr__(self):
        return f'{self.tags[0]}'

    def check_collision(self, x_direction, y_direction):
        hit_box = game.canvas.bbox(self.rectangle)
        canvas_ids_in_hit_box = game.canvas.find_overlapping(hit_box[0], hit_box[1], hit_box[2], hit_box[3])
        objects_in_hit_box = [game.object_dict[canvas_id] for canvas_id in canvas_ids_in_hit_box]
        objects_in_hit_box.remove(self)

        for hit_object in objects_in_hit_box:
            hit_object.collider_object = self
        key_list = list(game.object_dict.keys())
        home_base_list = []
        for key in key_list:
            if type(game.object_dict[key]) == Home_Base:
                home_base_list.append(game.object_dict[key])
        for home_base in home_base_list:
            if home_base in objects_in_hit_box:
                objects_in_hit_box.remove(home_base)
                if type(self) == Switcher:
                    Player.win()
        if objects_in_hit_box:
            print('collision')
            Game_Object.resolve_collision(objects_in_hit_box, x_direction, y_direction)

    def resolve_collision(objects_in_hit_box, x_direction, y_direction):
        for collision_object in objects_in_hit_box:
            print(f'{collision_object.collider_object} moved {collision_object}')
            type(collision_object).move(collision_object, round(x_direction), round(y_direction))
            Game_Object.keep_inbound(collision_object)
            Game_Object.check_collision(collision_object, x_direction, y_direction)
        
    def keep_inbound(object):
        position = game.canvas.coords(object.rectangle)
        width =game.width
        height = game.height
        if position[2] > game.width:
            game.canvas.move(object.rectangle, -(position[2]-width), 0)
        if position[0] < 0:
            game.canvas.move(object.rectangle, abs(position[0]), 0)            
        if position[3] > height:
            game.canvas.move(object.rectangle, 0, -(position[3]-height))
        if position[1] < 0:
            game.canvas.move(object.rectangle, 0, abs(position[1]))

    def reset(top=None):
        for game_object in game.object_dict:
            current_position = game.canvas.bbox(game.object_dict[game_object].rectangle)
            game.canvas.move(
            game.object_dict[game_object].rectangle,
            game.object_dict[game_object].start_position[0] - current_position[0],
            game.object_dict[game_object].start_position[3] - current_position[3]
                        )
            game.object_dict[game_object].collider_object = None
        if top:
            top.destroy()
        game.already_won = False

class Pushed(Game_Object):

    def move(self, x_direction, y_direction):
        game.canvas.move(self.rectangle, x_direction, y_direction)

class Push_Object(Game_Object):

    def move(self, x_direction, y_direction):
        distance = (5 if x_direction == 5 or y_direction == 5 else -5)
        game.canvas.move(self.collider_object.rectangle, -distance, -distance)

class Switcher(Game_Object):

    def move(self, x_direction, y_direction):
        if type(self.collider_object) == Player:
            game.canvas.move(self.collider_object.rectangle, -x_direction, -y_direction)
        self_position = game.canvas.coords(self.rectangle)
        collider_position = game.canvas.coords(self.collider_object.rectangle)
        game.canvas.move(
        self.rectangle, 
        collider_position[0] - self_position[0], 
        collider_position[3] - self_position[3])
        game.canvas.move(
        self.collider_object.rectangle, 
        self_position[0] - collider_position[0], 
        self_position[3] - collider_position[3])

class Diagonal(Game_Object):

    def move(self, x_direction, y_direction):
        if abs(x_direction) > abs(y_direction):
            game.canvas.move(self.rectangle, x_direction, x_direction)
        elif  abs(x_direction) < abs(y_direction):
            game.canvas.move(self.rectangle, -y_direction, y_direction)

class Wall(Game_Object):

    def move(self, x_direction, y_direction):
        game.canvas.move(self.collider_object.rectangle, -x_direction, -y_direction)

class Y_Mover(Game_Object):

    def move(self, x_direction, y_direction):
        game.canvas.move(self.rectangle, 0, y_direction)

class X_Mover(Game_Object):

    def move(self, x_direction, y_direction):
        game.canvas.move(self.rectangle, x_direction, 0)

class Jumper(Game_Object):

    def move(self, x_direction, y_direction):
        collider_x_size = abs(self.collider_object.x0 - self.collider_object.y0)
        collider_y_size = abs(self.collider_object.x1 - self.collider_object.y1)
        game.canvas.move(self.rectangle, 
        (-x_direction/5)*(collider_x_size + 2 if x_direction != 0 else 0), 
        (-y_direction/5)*(collider_y_size + 2 if y_direction != 0 else 0))

class Home_Base(Game_Object):

    def move(self, x_direction, y_direction):
        pass

class Player(Game_Object):

    def move(self, x_direction, y_direction):
        if type(self.collider_object) == Player: Switcher.move(self, x_direction, y_direction)
        else: game.canvas.move(self.rectangle, -x_direction, -y_direction)

    def left(self):
        game.canvas.move(self.rectangle, -5, 0)
        Game_Object.keep_inbound(self)
        Game_Object.check_collision(self, -5, 0)

    def right(self):
        game.canvas.move(self.rectangle, 5, 0)
        Game_Object.keep_inbound(self)
        Game_Object.check_collision(self, 5, 0)

    def up(self):
        game.canvas.move(self.rectangle, 0, -5)
        Game_Object.keep_inbound(self)
        Game_Object.check_collision(self, 0, -5)

    def down(self):
        game.canvas.move(self.rectangle, 0, 5)
        Game_Object.keep_inbound(self)
        Game_Object.check_collision(self, 0, 5)
        
    def win():
        if game.already_won == False:
            print('you won!')
            game.already_won = True
            top = tkinter.Toplevel(game.window)
            top.geometry("400x200")
            top.title("WINNER WINNER CHICKEN DINNER")
            win_label = tkinter.Label(top, text = 'You won!',font=("Arial", 25))
            win_button = tkinter.Button(
                                top, padx=50, pady=5, text='reset',font=("Arial", 25),
                                command= lambda: Game_Object.reset(top)
                                )
            win_label.pack()
            win_button.pack()


if __name__ == '__main__':
    game = Game()

    home_base          = Home_Base(    480, 480, 520, 520, fill = "pink", tags= "home base")

    player_1           = Player(         5,   5,  35,  35, fill = "green", tags= "player")
    player_2           = Player(       525, 525, 555, 555, fill = "green", tags= "player")

    object_rectangle_1 = Pushed(       100, 120, 130, 150, fill = "red", tags= "pushed")
    object_rectangle_2 = Pushed(       430, 430, 460, 460, fill = "red", tags= "pushed")

    object_rectangle_3 = Push_Object(   40,  40,  70,  70, fill = "blue", tags= "push")
    object_rectangle_4 = Push_Object(   40,  400, 70, 430, fill = "blue", tags= "push")

    object_rectangle_5 = Switcher(     200,  70, 230, 100, fill = "white", tags= "react")
    object_rectangle_6 = Diagonal(      50, 200,  80, 230, fill = "light blue", tags= "diagonal")
    object_rectangle_7 = Wall(         540, 440, 570, 470, fill = "light green", tags= "wall")

    game.window.bind("<KeyPress-Left>",  lambda e: Player.left( player_1))
    game.window.bind("<KeyPress-Right>", lambda e: Player.right(player_1))
    game.window.bind("<KeyPress-Up>",    lambda e: Player.up(   player_1))
    game.window.bind("<KeyPress-Down>",  lambda e: Player.down( player_1))

    game.window.bind("a", lambda e: Player.left( player_2))
    game.window.bind("d", lambda e: Player.right(player_2))
    game.window.bind("w", lambda e: Player.up(   player_2))
    game.window.bind("s", lambda e: Player.down( player_2))

    game.window.bind("R", lambda e: Game_Object.reset())

    game.window.mainloop()

if __name__ != '__main__':
    game = Game()