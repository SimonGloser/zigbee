from ursina import *   
from random import randint

import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
from ursina import *   
from random import randint



file1 = open('test_output.txt', 'r')

list_x_koordinates = []
list_y_koordinates = []
count = 0
# Strips the newline character
for line in file1:
    count += 1
    koordinates = line.split(';')
    x_koordinate = int(float(koordinates[0]))
    y_koordinate = int(float(koordinates[1]))

    list_x_koordinates.append(x_koordinate)
    list_y_koordinates.append(y_koordinate)
 
# Closing files
file1.close()


class Player(Entity):
    def __init__(self):
        super().__init__()
        self.parent = field
        self.model = "cube"
        self.color = color.black
        self.scale = .05
        self.position = (0,0,-.03)
        self.collider = 'box'
        self.dx = 0
        self.dy = 0
        self.eaten = 0
        self.koordcounter = 0

    def update(self):
        global body, text
        self.x += time.dt * self.dx
        self.y += time.dt * self.dy

        #update moving speed
        #check if x or y ist greater set lower value to 0
        if (list_x_koordinates[self.koordcounter] > list_y_koordinates[self.koordcounter]):
            if list_x_koordinates[self.koordcounter] > 0: #also rechts
                self.dx = .3
                self.dy = 0
            else:
                self.dx = -.3
                self.dy = 0



        if (list_y_koordinates[self.koordcounter] > list_x_koordinates[self.koordcounter]):
            if list_y_koordinates[self.koordcounter] > 0: #also rechts
                self.dx = 0
                self.dy = .3
            else:
                self.dx = 0
                self.dy = -.3



        if self.koordcounter >= 104:
            self.koordcounter = 0
        else:
            self.koordcounter += 1
            
   
        #apple eaten
        hit_info = self.intersects()
        if hit_info.hit:
            Audio('assets/apple_bite.wav')
            self.eaten += 1
            text.y = -1
            text = Text(text=f'Apple Eaten: {self.eaten}', position = (0,.4,3), origin = (0,0), sccale = 1.5, color=color.yellow, background = True)
            apple.x = randint(-4,4) * .1
            apple.y = randint(-4,4) * .1
            new_body = Entity(parent = field, model = "cube", z = -.029, color = color.gray, scale = .05 )
            body.append(new_body)

        for i in range (len(body)-1, 0, -1):
            body[i].position = body[i-1].position

        if len(body) >0:
            body[0].x = self.x
            body[0].y = self.y

        #boundary checking
        if abs(self.x) > .47 or abs(self.y) > .47:
            #Audio("assets/whistle.wav")
            for segment in body:
                segment.position = (10,10)
            body = []
            print_on_screen("you crushed !", position=(0,0), origin=(0,0), scale=2, duration=2)
            self.position=(0,0)
            self.dx=0
            self.dy=0
            self.eaten = 0
            text.y = -1
            text = Text(text=f'Apple Eaten: {self.eaten}', position = (0,.4,3), origin = (0,0), sccale = 1.5, color=color.yellow, background = True)


    """
    def input(self, key):
        if key == "right arrow":
            self.dx =.3
            self.dy = 0
        if key == "left arrow":
            self.dx = -.3
            self.dy = 0
        if key == "up arrow":
            self.dx = 0
            self.dy = .3

        if key == "down arrow":
            self.dx = 0
            self.dy = -.3
    """



app = Ursina()
#Background
Entity(model = 'quad', scale = 60, texture = 'assets/blue_sky.png')

#Field
field_size = 19
field = Entity(model = 'quad', color = color.green, scale = (12, 12), position = (field_size//2, field_size//2, -.01), texture= "white_cube")

camera.position = (field_size//2, -18, -18)
camera.rotation_x = -56

apple = Entity(
    parent = field, 
    model = "sphere", 
    color = color.red, 
    scale = .05, 
    position = (.1,.1,-.03),
    collider = 'box' )

player = Player()
body = []
text = Text(text="")
app.run()