import math
import shutil
import os
import subprocess
from lib.config import DualSPHysicsExecutables

class Simulation:

    def __init__(self):
        self.R = 0.095
        self.H = 0.4
        self.h = 0.1

        self.dt = 0.001
        self.T_end = 10

        self.motion = self.default_motion
        self.motion_R = 0.00625
        self.motion_omega = 2*math.pi*2*2

        self.dp = 0.01

        self.name = 'unnamed'

    
    def create_input_file(self):
        dict = {}

        dict['def_point_min_x'] = str(-self.R-self.motion_R-0.1)
        dict['def_point_min_y'] = str(-self.R-self.motion_R-0.1)
        dict['def_point_min_z'] = str(-0.1)
        dict['def_point_max_x'] = str(self.R+self.motion_R+0.1)
        dict['def_point_max_y'] = str(self.R+self.motion_R+0.1)
        dict['def_point_max_z'] = str(self.H+0.1)

        dict['sim_min_x'] = str(-self.R-self.motion_R-0.05)
        dict['sim_min_y'] = str(-self.R-self.motion_R-0.05)
        dict['sim_min_z'] = str(-0.05)
        dict['sim_max_x'] = str(self.R+self.motion_R+0.05)
        dict['sim_max_y'] = str(self.R+self.motion_R+0.05)
        dict['sim_max_z'] = str(self.H+0.05)


        dict['R'] = str(self.R)
        dict['H'] = str(self.H)
        dict['h'] = str(self.h)


        dict['dt'] = str(self.dt)
        dict['T_end'] = str(self.T_end)

        rundir = self.get_run_dir()
        if not os.path.isdir(rundir):
            os.makedirs(rundir)
        infile = os.path.join(rundir, 'input.xml')
    
        self.__generate_file_placeholder(os.path.join('input', 'template.xml'), infile, dict)
        self.create_motion_file()


    def create_motion_file(self):
        motion_file = open('run/motion.dat', 'w+')

        motion_file.writelines('#time;dispx;dispy;dispz\r\n')

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

        #return t, 0.0, 0.0

        return pos_x, pos_y, pos_z

    def get_run_dir(self):
        return os.path.join('run', self.name)
    
    def get_out_dir(self):
        return os.path.join('out', self.name)
    

    def execute(self):
        # remove old simulation if it exists
        rundir = self.get_run_dir()
        outdir = self.get_out_dir()

        if os.path.exists(outdir):
            shutil.rmtree(outdir)

        # create directory
        os.makedirs(outdir)

        # create input file
        self.create_input_file()
        shutil.copy(os.path.join('run', 'motion.dat'), os.path.join(outdir, 'motion.dat'))

        # execute Gencase
        cmd = '{0} {1} {2} -save:all -dp:{3}'.format(DualSPHysicsExecutables.GenCase, os.path.join(DualSPHysicsExecutables.out_prefix, rundir, 'input'), os.path.join(DualSPHysicsExecutables.out_prefix, outdir, 'sim'), self.dp)
        print(cmd)
        returncode = 0
        returncode = subprocess.call(cmd, shell=True)
        if returncode != 0:
            print("Gencase failed")
            exit()

        # execute simulation
        print("Simulation...")
        cmd = '{0} {1} {2} -svres -gpu'.format(DualSPHysicsExecutables.DualSPHysics, os.path.join(DualSPHysicsExecutables.out_prefix, outdir, 'sim'), os.path.join(DualSPHysicsExecutables.out_prefix, outdir))
        returncode = subprocess.call(cmd, shell=True)
        if returncode != 0:
            print("Simulation failed")
            exit()

        # execute partvtk
        print("PartVTK...")
        cmd = '{0} -dirin {1} -savevtk {2} -onlytype:-all,+fluid'.format(DualSPHysicsExecutables.PartVTK, os.path.join(DualSPHysicsExecutables.out_prefix, outdir), os.path.join(DualSPHysicsExecutables.out_prefix, outdir, 'PartFluid'))
        returncode = subprocess.call(cmd, shell=True)
        if returncode != 0:
            print("PartVTK failed")
            exit()


        # execute isosurface
        print("PartVTKOut...")
        cmd = '{0} -dirin {1} -saveiso {2}'.format(DualSPHysicsExecutables.IsoSurface, os.path.join(DualSPHysicsExecutables.out_prefix, outdir), os.path.join(DualSPHysicsExecutables.out_prefix, outdir, 'FluidIso'))
        returncode = subprocess.call(cmd, shell=True)
        if returncode != 0:
            print("PartVTKOut failed")
            exit()
