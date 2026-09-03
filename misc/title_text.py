import pyfiglet, subprocess
from . import colors

def show_title():
    title_screen = pyfiglet.figlet_format("S U P I N O", font="alligator2")
    
    subprocess.run(['clear'], shell=True)
    print(colors.txt_colors["light_gray"] + f"{pyfiglet.figlet_format("mace's", font='digital')}" + colors.txt_colors["RESET"])
        
    interation = 0
    for line in title_screen.splitlines():
        if interation < 2:
            print(colors.txt_colors["light_gray"] + f"{line}" + colors.txt_colors["RESET"])
        elif interation < 4:
            print(colors.txt_colors["cyan"] + f"{line}" + colors.txt_colors["RESET"])
        elif interation < 5:
            print(colors.txt_colors["blue"] + f"{line}" + colors.txt_colors["RESET"])
        elif interation < 8:
            print(colors.txt_colors["light_blue"] + f"{line}" + colors.txt_colors["RESET"])
        interation += 1
    print("\n")