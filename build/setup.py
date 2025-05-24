from cx_Freeze import setup,Executable

files = ['img']

exe = Executable(script=".py", base="Win32GUI")

setup(
    name = "Swiper",
    version = "0.1",
    description = "Intercambiador de canales",
    author="Luis Martin",
    options={'build.exe': {'include_files': files}},
    executables = [exe],
)