from lib.Simulation import Simulation
import math

def motion(t):

    omega = 2*math.pi*t*0.1

    # define motion here
    pos_x = 0.025*math.sin(omega*t)
    pos_y = 0.025*math.cos(omega*t)
    pos_z = 0

    # between 0 and 1 s: increase motion from zero linearly
    if(t < 1):
        pos_x *= t
        pos_y *= t
        pos_z *= t

    return pos_x, pos_y, pos_z

# create simulation
#sim = Simulation()
#sim.T_end = 30
#sim.dp = 0.01
#sim.motion = motion
#sim.name = 'linear_increasing_angular_velocity'
#sim.execute()
#exit()

# create simulation for default motion
sim = Simulation()
sim.T_end = 10
sim.dp = 0.0006
sim.name = 'const-freq-0.5Hz'
sim.motion_omega = 2*math.pi*0.5
sim.execute()

# create simulation for default motion
sim = Simulation()
sim.T_end = 10
sim.dp = 0.006
sim.name = 'const-freq-1.0Hz'
sim.motion_omega = 2*math.pi*1
sim.execute()

# create simulation for default motion
sim = Simulation()
sim.T_end = 10
sim.dp = 0.006
sim.name = 'const-freq-1.5Hz'
sim.motion_omega = 2*math.pi*1.5
sim.execute()



# create simulation for default motion
sim = Simulation()
sim.T_end = 10
sim.dp = 0.006
sim.name = 'const-freq-2.0Hz'
sim.motion_omega = 2*math.pi*2.0
sim.execute()



# create simulation for default motion
sim = Simulation()
sim.T_end = 10
sim.dp = 0.006
sim.name = 'const-freq-2.5Hz'
sim.motion_omega = 2*math.pi*2.5
sim.execute()



# create simulation for default motion
sim = Simulation()
sim.T_end = 10
sim.dp = 0.006
sim.name = 'const-freq-3.0Hz'
sim.motion_omega = 2*math.pi*3
sim.execute()

