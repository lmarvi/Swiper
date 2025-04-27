from cx_Freeze import setup,Executable


setup(
    name = "Swiper",
    version = "1.0",
    description = "Swiper",
    executables = [Executable("main.py", base = "Win32GUI", icon = 'Logo.ico')]
)