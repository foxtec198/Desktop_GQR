import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages":[
        "os","time",
    ],
    "includes":[
        "tkinter",
    ]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    
setup(
    name = 'template',
    version = '1.5',
    description = '...',
    options = {"build_exe":build_exe_options},
    executables = [Executable(
        'main.py', 
        base=base
        )
                   ]
)