import math as m
import tkinter
from tkinter import ttk
import gpiozero
import random

class Plot_Object():
    def __init__(self, canvas):
        self.objects = {}

        self.canvas = canvas
        self.draw_border()

    def draw_border(self):
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        self.canvas.create_line(5, 5, width-5, 5, fill='black', width='4')
        self.canvas.create_line(width-5, 5, width-5, height-5, fill='black', width='4')
        self.canvas.create_line(width-5, height-5, 5, height-5, fill='black', width='4')
        self.canvas.create_line(5, height-5, 5, 5, fill='black', width='4')

    def update(self, name, len1, theta, len2, phi, **kwargs):
        # Add or update 
        self.objects[name] = (len1, theta, len2, phi, kwargs['color'])

        # Revise plot
        self.canvas.delete('all')
        self.draw_border()

        wid = self.canvas.winfo_width()
        hei = self.canvas.winfo_height()

        for item in self.objects:
            len1, theta, len2, phi, color = self.objects[item]

            x1 = len1 * m.cos(theta + m.pi/2)
            y1 = len1 * m.sin(theta + m.pi/2)

            x2 = x1 + len2 * m.sin(theta + phi)
            y2 = y1 - len2 * m.cos(theta + phi)
        
            self.canvas.create_line(wid/2, 5, wid/2 + x1, 5 + y1, fill = color, width='4')
            self.canvas.create_line(wid/2 + x1, 5 + y1, wid/2 + x2, 5 + y2, fill = color, width='4')

class Servo_Object():
    def __init__(self, section_1_pin, section_2_pin):
        #TODO
        pass

    def update(self, name, len1, theta, len2, phi):
        #TODO
        pass

class Body():
    def __init__(self, body_orders, window):
        '''Represents a collection of legs. Locomotion only works with legs of the same lengths.
           Assign legs, servos and a canvas, then call Body.initialize().'''
        # Prepare a single, shared plot for each leg.
        self.my_plot = None

        # Prepare a list of legs.
        self.legs = []
        
        # Prepare a dictionary of servos. Dictionary key will be leg name.
        self.servos = {}
        self.update_time = 10 # milliseconds
        self.body_orders = body_orders
        self.window = window

    def assign_leg(self, name, section_1_len, section_2_len, direction):
        '''Assign a leg to the body.'''
        self.legs.append(Leg(name, section_1_len, section_2_len, direction))
        self.servos[name] = []

    def assign_canvas(self, canvas_obj):
        '''Assign a canvas to the legs.'''
        self.my_plot = Plot_Object(canvas_obj)

    def assign_servo(self, leg_name, servo_obj):
        '''Assign a servo to a leg.'''
        self.servos[leg_name].append(servo_obj)

    def initialize(self):
        '''Perform any actions required to set the legs '''
        pass
        #TODO: Initial move to halfway between min and max of both joints.
        #TODO: Any preparations to the canvas
        self.window.after(self.update_time, self.update)

    def update(self):
        ''''''
        pass
        # check orders
        # perform orders
        self.window.after(self.update_time, self.update)

        def stop_now():
            '''Body retains its current position. Move each leg where it is to right above 0, after a delay by leg so they don't all move at once.'''
            pass

        def stop_late(dist):
            '''Just call stop_soon() once dist < 1 step.'''
            pass

        def stop_soon(dist):
            '''Body advances until provided point (dist) is above body. Plan each leg to be in the correct position exactly when that happens.'''
            pass

            '''For a point z ahead of 0, there are 4 states:
            1) leg in the air - land @ z, adjusted for how long it takes to get there
            2) leg already at exactly z - slide to 0
            3) leg behind z - lift and move ahead
            4) leg ahead of z - lift and move back
            
            For all, stop slide once @ z and slide to 0.'''

class Leg():
    '''Represents one two-segement leg with members of lengths a and b with minimum angles t_0 and p_0, respectively.
       Angle 0 for the first leg is perpendicular to the surface. Angle 0 for the second leg is on the first leg.
       Angles are in radians.'''

    '''
    x1 = a*m.cos(t)
    y1 = a*m.sin(t)

    x2 = x1 + b*m.sin(t + p - m.pi/2)
    y2 = y1 - b*m.cos(t + + p - m.pi/2)
    '''

    def __init__(self, name, a, b, direction):
        self.name = name
        self.a = a
        self.b = b
        self.direction = direction

        self.f_x = lambda t, p: a*m.cos(t) + b*m.sin(t + p - m.pi/2)
        self.f_y = lambda t, p: a*m.sin(t) - b*m.cos(t + p - m.pi/2)

    def move(self, x, y):
        '''Return the leg angles that result in the provided x and y. Use this leg's direction and lengths.
           ((theta_1, phi_1), (theta_2, phi_2)). 1 and 2 are the two directions. theta is leg 1, phi is leg 2.'''
        (theta_1, phi_1), (theta_2, phi_2) = self.solve_self(x, y)
        if self.direction == 0:
            return (theta_1, phi_1)
        else:
            return (theta_2, phi_2)

    def solve_self(self, x, y):
        '''Return the two sets of leg angles that result in the provided x and y. Use this leg's lengths.
           ((theta_1, phi_1), (theta_2, phi_2)). 1 and 2 are the two directions. theta is leg 1, phi is leg 2.'''
        return self.solve(x, y, self.a, self.b)

    def solve(self, x, y, a, b):
        '''Return the two sets of leg angles that result in the provided x and y.
           ((theta_1, phi_1), (theta_2, phi_2)). 1 and 2 are the two directions. theta is leg 1, phi is leg 2.'''
        x, y = y, x #I have no idea how I mixed these up in the math.

        def get_phi(theta):
            dx = x - a*m.cos(theta)
            dy = y - a*m.sin(theta)
            if dx > 0:
                intermediate = m.asin(dy/b)
            else:
                intermediate = m.pi - m.asin(dy/b)
            return m.pi - theta + intermediate

        numerator = (-x**4 - y**4 - a**4 - b**4 -2*(x**2)*(y**2)
                     + 2*(x**2)*(a**2) + 2*(x**2)*(b**2) + 2*(y**2)*(a**2) + 2*(y**2)*(b**2) + 2*(a**2)*(b**2))
        denominator = x**2 + y**2 + 2*x*a - b**2 + a**2

        ratio_1 = (2*y*a - m.sqrt(numerator))/denominator       
        theta_1 = 2*m.atan(ratio_1)
        phi_1 = get_phi(theta_1)

        ratio_2 = (2*y*a + m.sqrt(numerator))/denominator
        theta_2 = 2*m.atan(ratio_2)
        phi_2 = get_phi(theta_2)

        return (theta_1, phi_1), (theta_2, phi_2)

if __name__ == '__main__':
    window = tkinter.Tk()

    body_orders = []
    body = Body(body_orders, window)

    frame = ttk.Frame(window)
    frame.pack()

    button = ttk.Button(frame, text='Update')
    button.pack()

    options_frame = ttk.Frame(frame)
    options_frame.pack()

    x_label = ttk.Label(options_frame, text='x:')
    x_label.grid(row=0, column=0)
    x_text = tkinter.Entry(options_frame)
    x_text.insert(tkinter.END, '25')
    x_text.grid(row=0, column=1)

    y_label = ttk.Label(options_frame, text='y:')
    y_label.grid(row=1, column=0)
    y_text = tkinter.Entry(options_frame)
    y_text.insert(tkinter.END, '25')
    y_text.grid(row=1, column=1)

    canvas = tkinter.Canvas(frame, bg="white", height=300, width=300)
    canvas.pack()
    canvas.update()

    #TODO: replace controls above with ability to add legs at given positions
    #TODO: add buttons to control the legs once the loop starts. Each button changes body_orders, which Body will read in each .update() cycle.

    def new_update():
        #TODO: scrap this and make it useful. Look at comments above.
        x = float(x_text.get())
        y = float(y_text.get())
        #leg_1.move(x, y)

    button.configure(command = new_update)

    window.after(body.update_time, body.initialize)
    window.mainloop()
