from os import link
from ursina import *   
from random import randint

import time
import serial
"""
Dieser Teil wird spaeter in eine seperate funktion ausgelagert. Dieser stand dient nur zu demozwecken
"""

arduinoData=serial.Serial('com8',38400)
time.sleep(1)
    
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
        
        dataPacket = arduinoData.readline() #reply
        dataPacket=str(dataPacket,'utf-8')

        splitPacket=dataPacket.split(";")

        splitPacketX=splitPacket[0].split("x00")
        splitPacketY=splitPacket[1].split("\x00")

        y_koordinate = int(float(splitPacketX[0]))
        x_koordinate = int(float(splitPacketY[1]))


        global body, text
        self.x += time.dt * self.dx
        self.y += time.dt * self.dy

        #camera control
        camera_control()

        #update moving speed
        #check if x or y ist greater set lower value to 0
        if (x_koordinate > 30 or y_koordinate > 30) or (x_koordinate < -30 or y_koordinate < -30):
                        if x_koordinate > -30: #also rechts
                                self.dx = -.3
                                self.dy = 0
                        elif x_koordinate < 30:
                                self.dx = .3
                                self.dy = 0



                        if y_koordinate > 30: #hoch runter
                                self.dx = 0
                                self.dy = .3
                        elif y_koordinate < -30:
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

"""
An dieser Stelle wird die Kamera gesteuert
"""
def camera_control():
        field.rotation_z += held_keys["d"]
        field.rotation_z -= held_keys["a"]

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