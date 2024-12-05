import sys 
import os
from pathlib import Path
from random import randint
from colorama import Fore, Style, init

import save_frame as sf
import change_background as cb
import importlib.metadata

def main():

    init(autoreset=True)
    prints_file_path = Path('./output/prints.txt')
    base_path = Path('./output/data')
    status = Path('./assets/current.txt')

    def show_intro():
        print(Fore.CYAN + "-" * 60)
        print(Fore.GREEN + center_text("Video Wallpaper CLI Tool"))
        print(Fore.CYAN + "-" * 60)
        print(Fore.YELLOW + center_text("Welcome! This program allows you to:"))
        print(Fore.YELLOW + center_text("1. Capture frames from a video and save them as images."))
        print(Fore.YELLOW + center_text("2. Set your wallpaper to a frame from a video sequence."))
        print(Fore.YELLOW + center_text("Enjoy creating unique wallpapers from any video of your choice!"))
        print(Fore.CYAN + "-" * 60)

    def MainMenu():
        print("\n" + Fore.CYAN + "-" * 60)
        print(Fore.GREEN + center_text("MAIN MENU"))
        print(Fore.CYAN + "-" * 60)
        print(Fore.MAGENTA + center_text("1 - Capture frames from video"))
        print(Fore.MAGENTA + center_text("2 - Change wallpaper to next frame"))
        print(Fore.MAGENTA + center_text("3 - Exit"))
        print(Fore.CYAN + "-" * 60)

    def capture_frames(path = '../assets/ArcaneSeason2.mp4'):
        sf.screenshot(Path(path))

    def Change(orientation):
        with open(status, 'r') as txt:
            chosen_frame = int(txt.read())
        chosen_frame += orientation
        if orientation > 1:
            chosen_frame = orientation

        print(chosen_frame)
        img = Path(f"./output/data/frame{chosen_frame}.jpg").resolve()
        cb.set_wallpaper(str(img))

        with open(status, 'w') as txt:
            txt.write(str(chosen_frame))

    def ChangeRandom():
        frames = [file for file in os.listdir(Path(f"./output/data/"))]
        Change(randint(0, len(frames)))

    def center_text(text, width=60):
        return text.center(width)

    def display_help():

        help_text= """
Usage: acw [OPTIONS] 

Options:
    -h, --help                  Print this help message and exit
    -v, --version               Print the program version and exit
    -c, --create-frames PATH    Get the video passed and start take screenshots
                                saving in the data folder
    -n, --next                  Change to the next wallpaper in the rotation
    -p, --previous              Change to the previous wallpaper in the rotation
    -s, --spec FRAME            Set a specfic wallpaper from the data folder
    -r, --random                Set a random wallpaper from the data folder

Examples:
    python main.py -c /path/to/video.mp4
    python main.py --next
    python main.py --random

see full documentations at https://github.com/BrunoDantasMoreira/automatically-change-wallpaper#readme
"""
        print(help_text)

    def display_version():
        version = importlib.metadata.version("automatically_change_wallpaper")
        print(f"Version: {version}")



    while True:

        if len(sys.argv) > 1:
            if sys.argv[1].lower().strip() == '--help' or sys.argv[1].lower().strip() == '-h':
                display_help()
                break
            
            if sys.argv[1].lower().strip() == '--version' or sys.argv[1].lower().strip() == '-v':
                display_version()
                break
            
            if sys.argv[1].lower().strip() == '--create-frames' or sys.argv[1].lower().strip() == '-c':
                if len(sys.argv) > 2:
                    capture_frames(sys.argv[2].lower().strip())
                else:
                    capture_frames()
                break

            if sys.argv[1].lower().strip() == '--next' or sys.argv[1].lower().strip() == '-n':
                Change(1)
                break

            if sys.argv[1].lower().strip() == '--previous' or sys.argv[1].lower().strip() == '-p':
                Change(-1)
                break

            if sys.argv[1].lower().strip() == '--spec' or sys.argv[1].lower().strip() == '-s':
                if len(sys.argv) > 2:
                    Change(sys.argv[2].lower().strip())
                else:
                    print('No value passed')
                break

            if sys.argv[1].lower().strip() == '--random' or sys.argv[1].lower().strip() == '-r':
                ChangeRandom()
                break











        MainMenu()

        choice = input("Your option: ")

        if choice == "1":
            capture_frames()

        elif choice == "2":
            Change(1)
            input("Wallpaper changed. Press Enter to continue...")


        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")

main()
