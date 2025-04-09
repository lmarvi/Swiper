from cx_Freeze import setup,Executable


setup(
    name = "Permutador",
    version = "1.0",
    description = "Permutador",
    executables = [Executable("main.py", base = "Win32GUI", icon = 'Logo.ico')]
)