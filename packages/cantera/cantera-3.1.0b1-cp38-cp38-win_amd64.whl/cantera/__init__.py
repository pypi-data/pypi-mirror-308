# This file is part of Cantera. See License.txt in the top-level directory or
# at https://cantera.org/license.txt for license and copyright information.


# start delvewheel patch
def _delvewheel_patch_1_8_3():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'cantera.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-cantera-3.1.0b1')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-cantera-3.1.0b1')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_8_3()
del _delvewheel_patch_1_8_3
# end delvewheel patch

from ._cantera import *
from ._utils import __version__, __sundials_version__, __git_commit__
from .composite import *
from .liquidvapor import *
from .onedim import *
from .utils import *
from .data import *
import cantera.interrupts  # Helps with standalone packaging (PyInstaller etc.)

import os
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('default', module='cantera')
add_directory(Path(__file__).parent / "data")
add_directory('.')  # Move current working directory to the front of the path

# Python interpreter used for converting mechanisms
if 'PYTHON_CMD' not in os.environ:
    os.environ['PYTHON_CMD'] = sys.executable
