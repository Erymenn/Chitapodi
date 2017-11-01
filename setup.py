import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["pygame"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32": base = "Win32GUI"

setup(  name = "chitapodi",
        version = "0.1",
		author="Morgane Mahaud",
        description = "Les cavernes de Chitapodi: un jeu de demineur/aventure/exploration !",
        options = {"build_exe": build_exe_options},
        executables = [Executable("chitapodi.py", base=base)])

#pour creer executable: python setup.py build
