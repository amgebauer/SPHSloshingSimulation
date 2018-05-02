import platform
import os

class DualSPHysicsExecutables:
    
    # path to executables (relative to the root of the repository)
    if platform.system() == 'Windows':
        raise RuntimeError("Windows executables not set")
    elif platform.system() == 'Darwin':
        raise RuntimeError("Mac is not supported.")
    elif platform.system() == 'Linux':
        GenCase = os.path.join('execs', 'GenCase4_linux64')
        DualSPHysics = os.path.join('execs', 'DualSPHysics4CPU_linux64')
        PartVTK = os.path.join('execs', 'PartVTK4_linux64')
        PartVTKOut = os.path.join('execs', 'PartVTKOut4_linux64')
        IsoSurface = os.path.join('execs', 'IsoSurface4_linux64')
    else:
        raise RuntimeError("Unknown os "+platform.system())