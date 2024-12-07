import sys
import os
from .utils import videoCat


    
        
def show_help():
    print("Display an video on the terminal")
    print("Usage:")
    print("  vcat <image_path>")


def main() -> None:
    if len(sys.argv) != 2:
        show_help()
    else:
        if not os.path.isfile(sys.argv[1]):
            print("File does not exist")
            return
        video_path = sys.argv[1]
        videoCat(video_path)
        
if __name__ == "__main__":
    main()