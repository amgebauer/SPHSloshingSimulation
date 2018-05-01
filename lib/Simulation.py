import math

class Simulation:

    def __init__(self):
        print("Hi Simulation")
        self.R = 0.2
        self.H = 0.4
        self.h = 0.1

        self.dt = 0.01
        self.T_end = 10

        self.motion = self.default_motion
        self.motion_R = 0.02
        self.motion_omega = 2*math.pi*2

        self.input_name = 'def'
        self.output_name = 'sim'

    
    def create_input_file(self):
        dict = {}

        dict['def_point_min_x'] = str(-self.R-0.05)
        dict['def_point_min_y'] = str(-self.R-0.05)
        dict['def_point_min_z'] = str(-0.05)
        dict['def_point_max_x'] = str(self.R+0.05)
        dict['def_point_max_y'] = str(self.R+0.05)
        dict['def_point_max_z'] = str(self.H+0.05)

        dict['R'] = str(self.R)
        dict['H'] = str(self.H)
        dict['h'] = str(self.h)


        dict['dt'] = str(self.dt)
        dict['T_end'] = str(self.T_end)

        self.__generate_file_placeholder('input/template.xml', 'run/{0}.xml'.format(self.input_name), dict)
        self.create_motion_file()


    def create_motion_file(self):
        motion_file = open('run/motion.dat', 'w+')

        motion_file.writelines('time;dispx;dispy;dispz\r\n')

        t = 0.0

        while t <= self.T_end:
            pos_x, pos_y, pos_z = self.motion(t)
            motion_file.writelines('{0}\t{1}\t{2}\t{3}\r\n'.format(t, pos_x, pos_y, pos_z))
            t += self.dt
        
        motion_file.close()


    def __generate_file_placeholder(self, template_file, output_file, placeholders):
        """Generates a file from template_file with replacing all in placehodlers"""
        template_head = open(template_file, 'r')
        input_head = open(output_file, 'w+')

        for line in template_head.readlines():

            # replace all placeholders
            for key, value in placeholders.items():
                line = line.replace('{{{0}}}'.format(key), value)

            input_head.writelines(line)

        template_head.close()
        input_head.close()

    def default_motion(self, t):
        
        # define only circular motion
        pos_x = self.motion_R*math.sin(self.motion_omega*t)
        pos_y = self.motion_R*math.cos(self.motion_omega*t)
        pos_z = 0

        # between 0 and 1 s: increase motion from zero linearly
        if(t < 1):
            pos_x *= t
            pos_y *= t
            pos_z *= t

        return t, 0.0, 0.0

        #return pos_x, pos_y, pos_z
