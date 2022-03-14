import math as m
import matplotlib.pyplot as plt
from itertools import product

class Leg():
    '''Represents one two-segement leg with members of lengths a and b with minimum angles t_0 and p_0, respectively.'''

    '''
    x1 = a*m.cos(t_0 + t)
    y1 = a*m.sin(t_0 + t)

    x2 = x1 + b*m.sin(t_0 + t - p_0 - p)
    y2 = y1 + b*m.cos(t_0 + t - p_0 - p)
    '''

    def __init__(self, a, b, t_0, p_0):
        self.a = a
        self.b = b
        self.t_0 = t_0
        self.p_0 = p_0

        self.f_x = lambda t, p: a*m.cos(t_0 + t) + b*m.sin(t_0 + t + p_0 + p - m.pi/2)
        self.f_y = lambda t, p: a*m.sin(t_0 + t) - b*m.cos(t_0 + t + p_0 + p - m.pi/2)

    def solve(self, x, y, a, b):
        
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

    def plot_range(self, x, y):
        num_points = 40
        t_range = [i*m.pi/2/num_points for i in range(num_points)]
        p_range = [i*m.pi/2/num_points for i in range(num_points)]
        
        tp_s = [(t, p) for t, p in product(t_range, p_range)]
        t_s = [item[0] for item in tp_s]
        p_s = [item[1] for item in tp_s]

        g1_s = [self.f_x(t, p)-x for t, p in tp_s]
        g2_s = [self.f_y(t, p)-y for t, p in tp_s]

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        ax.clear()
        ax.scatter(t_s, p_s, g1_s, marker='o', color='g', label='g1')
        ax.scatter(t_s, p_s, g2_s, marker='o', color='r', label='g2')

        ax.set_xlabel('t')
        ax.set_ylabel('p')
        ax.set_zlabel('g')

        fig.show()
        print('aaa')

if __name__ == '__main__':
    a = 1.5
    b = 0.5
    leg = Leg(a, b, 0, 0)

    target_x = 1.1
    target_y = -0.5

    (A1, A2), (B1, B2) = leg.solve(target_x, target_y, a, b)
    print(f'x: {target_x} vs {leg.f_x(A1, A2)} and {leg.f_x(B1, B2)}')
    print(f'y: {target_y} vs {leg.f_y(A1, A2)} and {leg.f_y(B1, B2)}')

'''Position 0 for any leg is directly above/below the leg base. It's the resting position for all legs.'''


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
