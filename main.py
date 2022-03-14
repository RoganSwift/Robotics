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
