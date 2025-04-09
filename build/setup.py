import sys
import os
from cx_Freeze import setup,Executable

files = ['img']

exe = Executable(script="ui_Permutador.py", base="Win32GUI")

setup(
    name = "Permutador de Canales",
    version = "0.1",
    description = "Permutador",
    author="Luis Martin",
    options={'build.exe': {'include_files': files}},
    executables = [exe],
)