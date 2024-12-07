import sys
import os.path
from .utils import *


def show_help():
    print("Display an image on the terminal")
    print("Usage:")
    print("  icat <image_path>")

def main():
    if len(sys.argv) != 2:
        show_help()
    else:
        if not os.path.isfile(sys.argv[1]):
            print("File does not exist")
            return
        image_path = sys.argv[1]
        imgCat(image_path)

if __name__ == "__main__":
    main()