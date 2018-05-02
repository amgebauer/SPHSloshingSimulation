import platform
import os

class DualSPHysicsExecutables:
    
    # path to executables (relative to the root of the repository)
    if platform.system() == 'Windows':
        out_prefix = '.'
        GenCase = os.path.join('execs', 'GenCase4_win64.exe')
        DualSPHysics = os.path.join('execs', 'DualSPHysics4_win64.exe')
        PartVTK = os.path.join('execs', 'PartVTK4_win64.exe')
        PartVTKOut = os.path.join('execs', 'PartVTKOut4_win64.exe')
        IsoSurface = os.path.join('execs', 'IsoSurface4_win64.exe')
    elif platform.system() == 'Darwin':
        out_prefix = os.path.join(os.path.sep, 'run')
        GenCase = 'docker run -v "{0}":/run dualsphysics ./GenCase4_linux64'.format(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        DualSPHysics = 'docker run -v "{0}":/run dualsphysics ./DualSPHysics4.2CPU_linux64'.format(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        PartVTK = 'docker run -v "{0}":/run dualsphysics ./PartVTK4_linux64'.format(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        PartVTKOut = 'docker run -v "{0}":/run dualsphysics ./PartVTKOut4_linux64'.format(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        IsoSurface = 'docker run -v "{0}":/run dualsphysics ./IsoSurface4_linux64'.format(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    elif platform.system() == 'Linux':
        out_prefix = '.'
        GenCase = os.path.join('execs', 'GenCase4_linux64')
        DualSPHysics = os.path.join('execs', 'DualSPHysics4CPU_linux64')
        PartVTK = os.path.join('execs', 'PartVTK4_linux64')
        PartVTKOut = os.path.join('execs', 'PartVTKOut4_linux64')
        IsoSurface = os.path.join('execs', 'IsoSurface4_linux64')
    else:
        raise RuntimeError("Unknown os "+platform.system())

