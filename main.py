import math as m
import tkinter
from tkinter import ttk
import time
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
    def __init__(self, servo_1_pin, servo_2_pin):
        #TODO
        pass

    def update(self, name, len1, theta, len2, phi):
        #TODO
        pass

class Body():
    def __init__(self, window):
        '''Represents a collection of legs. Locomotion only works with legs of the same lengths.
           Assign legs, servos and a canvas, then call Body.initialize().'''
        # Prepare a single, shared plot for each leg.
        self.my_plot = None

        # Prepare a list of legs.
        self.legs = []
        
        # Prepare a dictionary of servos. Dictionary key will be leg name.
        self.servos = {}
        self.update_time = 100 # milliseconds
        self.window = window
        print(f'{time.time()}: Body created')

    def assign_leg(self, name, section_1_len, section_2_len, direction):
        '''Assign a leg to the body.'''
        self.legs.append(Leg(name, section_1_len, section_2_len, direction))
        self.servos[name] = []
        print(f'{time.time()}: Leg assigned with ({name}, {section_1_len}, {section_2_len}, {direction})')        

    def assign_canvas(self, canvas_obj):
        '''Assign a canvas to the legs.'''
        self.my_plot = Plot_Object(canvas_obj)
        print(f'{time.time()}: Plot Object assigned')  

    def assign_servo(self, leg_name, servo_obj):
        '''Assign a servo to a leg.'''
        self.servos[leg_name].append(servo_obj)
        print(f'{time.time()}: Servo assigned to leg {leg_name}')  

    def initialize(self):
        '''Perform any actions required to set the legs '''
        print(f'{time.time()}: Initialized!')  
        self.order = 'wait'
        self.details = None
        #TODO: Initial move to halfway between min and max of both joints.
        #TODO: Any preparations to the canvas
        self.window.after(self.update_time, self.update)

    def set_order(self, order, details=None):
        self.order = order
        self.details = details

    def update(self):
        ''''''
        print(f'{self.order} {self.details}')
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

    body = Body(window)

    ##### Window Layout #####
    
    # Frame one - Options to Build Body
    # Initially visible; hidden when Initialize is pressed.

    # .....................................................
    # . Leg Name  . ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.
    # .....................................................
    # . Sec 1 Len . ~~~~~~~~~~ . Servo Pin 1 . ~~~~~~~~~~ .
    # .....................................................
    # . Sec 2 Len . ~~~~~~~~~~ . Servo Pin 2 . ~~~~~~~~~~ .
    # .....................................................
    # . Direction . ~~~~~~~~~~ .                          .
    # .....................................................
    # .    Add Leg (Button)    .    Add Servo (Button)    .
    # .....................................................
    # .                Initialize (Button)                .
    # .....................................................

    frame_1 = ttk.Frame(window)
    frame_1.grid(row=0, column=0)

    # Row 1
    label_1_1 = ttk.Label(frame_1, text='Leg Name')
    label_1_1.grid(row=0, column=0)

    entry_1_2 = ttk.Entry(frame_1)
    entry_1_2.insert(tkinter.END, 'Banana')
    entry_1_2.grid(row=0, column=1, columnspan=3)

    # Row 2
    label_1_3 = ttk.Label(frame_1, text='Sec. 1 Length')
    label_1_3.grid(row=1, column=0)

    entry_1_4 = ttk.Entry(frame_1)
    entry_1_4.insert(tkinter.END, '50')
    entry_1_4.grid(row=1, column=1)

    label_1_5 = ttk.Label(frame_1, text='Servo 1 Pin')
    label_1_5.grid(row=1, column=2)

    entry_1_6 = ttk.Entry(frame_1)
    entry_1_6.insert(tkinter.END, '16')
    entry_1_6.grid(row=1, column=3)

    # Row 3
    label_1_7 = ttk.Label(frame_1, text='Sec. 2 Length')
    label_1_7.grid(row=2, column=0)

    entry_1_8 = ttk.Entry(frame_1)
    entry_1_8.insert(tkinter.END, '50')
    entry_1_8.grid(row=2, column=1)

    label_1_9 = ttk.Label(frame_1, text='Servo 2 Pin')
    label_1_9.grid(row=2, column=2)

    entry_1_a = ttk.Entry(frame_1)
    entry_1_a.insert(tkinter.END, '16')
    entry_1_a.grid(row=2, column=3)

    # Row 4
    label_1_b = ttk.Label(frame_1, text='Direction')
    label_1_b.grid(row=3, column=0)

    variable_1_c = tkinter.StringVar(window)
    variable_1_c.set('Clockwise')
    
    w = ttk.OptionMenu(frame_1, variable_1_c, 'Clockwise', 'Clockwise', 'Counterclockwise')
    w.grid(row=3, column=1)
 
    # Row 5
    def add_leg():
        leg_name = str(entry_1_2.get())
        sec_1_len = float(entry_1_4.get())
        sec_2_len = float(entry_1_8.get())
        if variable_1_c.get() == 'Clockwise':
            direction = 0
        else:
            direction = 1
        body.assign_leg(leg_name, sec_1_len, sec_2_len, direction)

    button_1_d = ttk.Button(frame_1, text='Add Leg', command = add_leg)
    button_1_d.grid(row=4, column=0, columnspan=2)

    def add_servo():
        leg_name = str(entry_1_2.get())
        servo_1_pin = float(entry_1_6.get())
        servo_2_pin = float(entry_1_a.get())
        body.assign_servo(leg_name, Servo_Object(servo_1_pin, servo_2_pin))    

    button_1_e = ttk.Button(frame_1, text='Add Servo', command = add_servo)
    button_1_e.grid(row=4, column=2, columnspan=2)

    # Row 6
    def initialize():
        frame_1.grid_remove()
        frame_2.grid()
        frame_3.grid()
        window.after(body.update_time, body.initialize)

    button_1_f = ttk.Button(frame_1, text='Initialize', command = initialize)
    button_1_f.grid(row=5, column=1, columnspan=2)

    def hardcoded():
        body.assign_leg("Leg 1", 60, 60, 0)
        body.assign_leg("Leg 2", 60, 60, 0)
        body.assign_leg("Leg 3", 60, 60, 0)
        body.assign_leg("Leg 4", 60, 60, 0)
        initialize()

    button_1_g = tkinter.Button(frame_1, text='Hardcoded', bg = 'blue', command = hardcoded)
    button_1_g.grid(row=5, column=3)

    # Frame two - Options to Operate Body
    # Initially hidden; revealed when Initialize is pressed.

    # ....................................................
    # .  Start Walking (Button) .   Stop_Now() (Button)  .
    # ....................................................
    # .  Stop_Later() (Button)  . Dist To Walk . ~~~~~~~ .
    # ....................................................
    # .     Freeze (Button)     .     Resume (Button)    .
    # ....................................................
    # .   Walk_Dist() (Button)  . Dist To Walk . ~~~~~~~ .
    # ....................................................


    frame_2 = ttk.Frame(window)
    frame_2.grid(row=1, column=0)

    #TODO: fade Stop Now/Stop Later until Start Walking is pressed. Same for Freeze -> Resume

    # Row 1
    button_2_1 = ttk.Button(frame_2, text='Start Walking', command = lambda: body.set_order('start_walking'))
    button_2_1.grid(row=0, column=0)

    button_2_2 = ttk.Button(frame_2, text='Stop Now', command = lambda: body.set_order('stop_now'))
    button_2_2.grid(row=0, column=1, columnspan=2)

    # Row 2
    button_2_3 = ttk.Button(frame_2, text='Stop in X')
    button_2_3.grid(row=1, column=0)    

    label_2_4 = ttk.Label(frame_2, text='Dist. to Walk')
    label_2_4.grid(row=1, column=1)

    entry_2_5 = ttk.Entry(frame_2)
    entry_2_5.insert(tkinter.END, '50')
    entry_2_5.grid(row=1, column=2)

    button_2_3.configure(command = lambda: body.set_order('stop_in_x', details = float(entry_2_5.get())))  

    # Row 3
    button_2_6 = ttk.Button(frame_2, text='Freeze', command = lambda: body.set_order('freeze'))
    button_2_6.grid(row=2, column=0)

    button_2_7 = ttk.Button(frame_2, text='Resume', command = lambda: body.set_order('resume'))
    button_2_7.grid(row=2, column=1, columnspan=2)

    # Row 4
    button_2_8 = ttk.Button(frame_2, text='Walk X Distance')
    button_2_8.grid(row=3, column=0)    

    label_2_9 = ttk.Label(frame_2, text='Dist. to Walk')
    label_2_9.grid(row=3, column=1)

    entry_2_a = ttk.Entry(frame_2)
    entry_2_a.insert(tkinter.END, '50')
    entry_2_a.grid(row=3, column=2)

    button_2_8.configure(command = lambda: body.set_order('walk_dist', details = float(entry_2_a.get())))  

    # Frame three - canvas
    # Initially hidden; revealsed when Initialize is pressed

    frame_3 = ttk.Frame(window)
    frame_2.grid(row=2, column=0)

    canvas = tkinter.Canvas(frame_3, bg="white", height=300, width=300)
    canvas.pack()
    canvas.update()
    body.assign_canvas(canvas)

    # Hide frames 2 and 3 until Initialize unhides them

    frame_2.grid_remove()
    frame_3.grid_remove()

    window.mainloop()
