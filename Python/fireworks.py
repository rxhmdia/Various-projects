'''
FIREWORKS SIMULATION WITH TKINTER

*self-containing code
*to run: simply type python simple.py in your console
*compatible with both Python 2 and Python 3
*Dependencies: tkinter, Pillow (only for background image)
*The design is based on high school physics, with some small twists only for aesthetics purpose

'''
import tkinter as tk
#from tkinter import messagebox
#from tkinter import PhotoImage
from PIL import Image, ImageTk
from time import time, sleep
from random import choice, uniform, randint
from math import sin, cos, radians
import numpy as np
# gravity, act as our constant g, you can experiment by changing it
GRAVITY = 0.05
time_sankai=0.5
time_yanhuachixu=1.0
# list of color, can choose randomly or use as a queue (FIFO)
colors = ['red', 'blue', 'yellow', 'white', 'green', 'orange', 'purple', 'seagreen','indigo', 'cornflowerblue']

'''
Generic class for particles

particles are emitted almost randomly on the sky, forming a round of circle (a star) before falling and getting removed
from canvas

Attributes:
    - id: identifier of a particular particle in a star
    - x, y: x,y-coordinate of a star (point of explosion)
    - vx, vy: speed of particle in x, y coordinate
    - total: total number of particle in a star
    - age: how long has the particle last on canvas
    - color: self-explantory
    - cv: canvas
    - lifespan: how long a particle will last on canvas

'''
class part:
    def __init__(self, cv, idx, total, explosion_speed, x=0., y=0., vx = 0., vy = 0., size=2., color = 'red', lifespan = 2,rot=0, **kwargs):
        self.id = idx
        self.x = x
        self.y = y
        self.initial_speed = explosion_speed
        self.vx = vx
        self.vy = vy
        self.total = total
        self.age = 0
        self.color = color
        self.cv = cv
        self.cid = self.cv.create_oval(
            x - size, y - size, x + size,
            y + size, fill=self.color)
        self.lifespan = lifespan
        self.times=int(explosion_speed/0.1)
        self.rot=rot
    def update(self, dt):
        self.age += dt

        # particle expansions
        # if self.alive() and self.expand():
        #     # move_x = cos(radians(self.id*360/self.total))*self.initial_speed
        #     # move_y = sin(radians(self.id*360/self.total))*self.initial_speed
        #     # self.cv.move(self.cid, move_x, move_y)
        #     # self.vx = move_x/(float(dt)*1000)
        #     # for k in np.arange(0.1,self.initial_speed):
        #     # k=randint(30,90)
        #     idtemp=np.mod(self.id,self.times)
        #     if idtemp==0:
        #         idtemp=self.times
        #     move_x = cos(radians((idtemp)*360/self.total+self.rot))*self.initial_speed
        #     move_y = sin(radians((idtemp)*360/self.total+self.rot))*self.initial_speed
        #     self.cv.move(self.cid, move_x, move_y)
        #     self.vx = move_x/(float(dt)*1000)
        #
        #     self.vy = move_y / (float(dt) * 1000)

        # falling down in projectile motion
        if self.alive():
            # move_x = cos(radians(self.id*360/self.total))
            # # we technically don't need to update x, y because move will do the job
            # self.cv.move(self.cid, self.vx + move_x, self.vy+GRAVITY*dt)
            # self.vy += GRAVITY*dt
            # move_x = cos(radians(np.mod(self.id, self.times) * 360 / self.total))*self.initial_speed
            # move_y = sin(radians(np.mod(self.id, self.times) * 360 / self.total))*self.initial_speed
            idtemp=np.mod(self.id,self.times)
            if idtemp==0:
                idtemp=self.times
            move_x = cos(radians((idtemp)*360/self.total+self.rot))*self.initial_speed
            move_y = sin(radians((idtemp)*360/self.total+self.rot))*self.initial_speed
            self.cv.move(self.cid, move_x, move_y)
            # self.vx = move_x / (float(dt) * 1000)
            self.vx = move_x / (float(dt) * 1000)

            self.vy = move_y / (float(dt) * 1000)
            # self.cv.size=self.cv.size*((self.lifespan-self.age)/dt)
            # self.cid=self.cid/2

        # remove article if it is over the lifespan
        elif self.cid is not None:
            cv.delete(self.cid)
            self.cid = None

    # define time frame for expansion
    def expand (self):
        return self.age <= time_sankai

    # check if particle is still alive in lifespan
    def alive(self):
        return self.age <= self.lifespan

'''
Firework simulation loop:
Recursively call to repeatedly emit new fireworks on canvas

a list of list (list of stars, each of which is a list of particles)
is created and drawn on canvas at every call, 
via update protocol inside each 'part' object 
'''
def simulate(cv):
    t = time()
    explode_points = []
    wait_time = randint(10,100)
    numb_explode = randint(6,10)
    # create list of list of all particles in all simultaneous explosion
    for point in range(numb_explode):
        objects = []
        x_cordi = randint(50,550)
        y_cordi = randint(50, 150)
        speed = uniform (1.5, 3.5)
        size = uniform (0.5,2.5)
        color = choice(colors)
        explosion_speed = uniform(7,10)
        # total_particles = randint(10,50)
        total_particles = randint(10,12)
        # lifespan = uniform(1.6, 1.75)
        lifespan = uniform(0.8,0.9)

        for k in range(0,int(explosion_speed/0.1),4):
            for i in range(1,total_particles):
                rotatea = randint(-30, 30)
                r = part(cv, idx = k*total_particles+i, total = total_particles, explosion_speed = (k+1)*0.05, x = x_cordi, y = y_cordi,
                    vx = k, vy = k, color=color, size = size, lifespan = lifespan,rot=rotatea)
                objects.append(r)
        explode_points.append(objects)

    total_time = .0
    # keeps undate within a timeframe of 1.8 second
    while total_time < time_yanhuachixu:
        sleep(0.01)
        tnew = time()
        t, dt = tnew, tnew - t
        for point in explode_points:
            for item in point:
                item.update(dt)
        cv.update()
        total_time += dt
    # recursive call to continue adding new explosion on canvas
    root.after(wait_time, simulate, cv)

def close(*ignore):
    """Stops simulation loop and closes the window."""
    global root
    root.quit()
    
if __name__ == '__main__':
    root = tk.Tk()
    cv = tk.Canvas(root, height=600, width=600)
    # use a nice background image
    image = Image.open("image.jpg")
    photo = ImageTk.PhotoImage(image)
    cv.create_image(0, 0, image=photo, anchor='nw')

    # cv.create_image(0, 0, image=None, anchor='nw')

    cv.pack()
    root.protocol("WM_DELETE_WINDOW", close)

    root.after(100, simulate, cv)

    root.mainloop()
