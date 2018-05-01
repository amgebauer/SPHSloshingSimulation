import numpy as np
import subprocess
import shutil
import os
from lib.Simulation import Simulation

# executables depend on the platform
if os.name == 'nt':
    # if you are using WINDOWS, set the executable names here
    raise RuntimeError("Windows executables are not added yet")
else:
    exec_gencase = "GenCase4_linux64"
    exec_dualsphysics = "DualSPHysics4CPU_linux64"
    exec_partvtk = "PartVTK4_linux64"
    exec_partvtkout = "PartVTKOut4_linux64"
    exec_isosurface = "IsoSurface4_linux64"


# create simulation
sim = Simulation()
sim.T_end = 0.5

# remove old simulation if it exists
dir = os.path.dirname('out/')

if os.path.exists(dir):
    shutil.rmtree(dir)

# create directory
os.mkdir(dir)

# create input file
sim.create_input_file()
shutil.copy('run/motion.dat', 'out/motion.dat')
shutil.copy('run/CaseSloshingMotionData.dat', 'out/CaseSloshingMotionData.dat')

# execute Gencase
print("Gencase...")
cmd = '../execs/{0} {1} ../out/{2} -save:all'.format(exec_gencase, sim.input_name, sim.output_name)
returncode = subprocess.call(cmd, shell=True, cwd='run')
if returncode != 0:
    print("Gencase failed")
    exit()

# execute simulation
print("Simulation...")
cmd = '../execs/{0} ../out/{1}  ../out/ -svres -cpu'.format(exec_dualsphysics, sim.output_name)
returncode = subprocess.call(cmd, shell=True, cwd='run')
if returncode != 0:
    print("Simulation failed")
    exit()

# execute partvtk
print("PartVTK...")
cmd = '../execs/{0} -dirin ../out/ -savevtk ../out/PartFluid -onlytype:-all,+fluid'.format(exec_partvtk)
returncode = subprocess.call(cmd, shell=True, cwd='run')
if returncode != 0:
    print("PartVTK failed")
    exit()

# execute partvtkout
print("PartVTKOut...")
cmd = '../execs/{0} -dirin ../out/ -filexml  ../out/{1}.xml -savevtk ../out/PartFluidOut -SaveResume ../out/ResumeFluidOut'.format(exec_partvtkout, sim.output_name)
returncode = subprocess.call(cmd, shell=True, cwd='run')
if returncode != 0:
    print("PartVTKOut failed")
    exit()


# execute isosurface
print("PartVTKOut...")
cmd = '../execs/{0} -dirin ../out/ -saveiso ../out/FluidIso'.format(exec_isosurface)
returncode = subprocess.call(cmd, shell=True, cwd='run')
if returncode != 0:
    print("PartVTKOut failed")
    exit()