from PIL import Image
import shutil
import cv2

def block(fc=None, bc=None) -> str:
    """Generate a block character with foreground and background colors."""
    fg_code = f'\033[38;2;{fc[0]};{fc[1]};{fc[2]}m' if fc else ''
    bg_code = f'\033[48;2;{bc[0]};{bc[1]};{bc[2]}m' if bc else ''
    reset_code = '\033[0m'
    return f'{fg_code}{bg_code}\u2584{reset_code}'

def fit_image_to_terminal(image, terminal_size) -> Image.Image:
    """Resize the image to fit within the terminal dimensions."""
    term_height, term_width = terminal_size
    new_height = term_height * 2
    new_width = int(new_height / image.height * image.width)
    
    if new_width > term_width * 2:
        new_width = term_width * 2
        new_height = int(new_width / image.width * image.height)
    
    return image.resize((new_width, new_height))

def __frameCat(img: Image.Image) -> None:
    """Cat image on terminal

    Args:
        img_path (str): _description_
    """
    img = img.convert('RGB')
    terminal_size = shutil.get_terminal_size(fallback=(80, 24))
    resized_img = fit_image_to_terminal(img, (terminal_size.lines-1, (terminal_size.columns - 4) // 2))
    output = '\033[1;1H'
    for y in range(0, resized_img.height, 2):
        for x in range(resized_img.width):
            fc = resized_img.getpixel((x, min(y + 1, resized_img.height - 1)))
            bc = resized_img.getpixel((x, y))
            output += block(fc, bc)   
        output += "\r\n"
    output = output.rstrip("\r\n")
    print(output, end="")
    
def __imgCat(img: Image.Image) -> None:
    """Cat image on terminal
    Args:
        img_path (str): _description_
    """
    img = img.convert('RGB')
    terminal_size = shutil.get_terminal_size(fallback=(80, 24))
    resized_img = fit_image_to_terminal(img, (terminal_size.lines, (terminal_size.columns - 4) // 2))
    for y in range(0, resized_img.height, 2):
        output = ""
        for x in range(resized_img.width):
            fc = resized_img.getpixel((x, min(y + 1, resized_img.height - 1)))
            bc = resized_img.getpixel((x, y))
            output += block(fc, bc)   
        print(output)


def imgCat(image_path: str) -> None:
    try:
        img = Image.open(image_path)
    except Image.UnidentifiedImageError:
        print(f"Error: The file at {image_path} is not a valid image file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    __imgCat(img)
    

def videoCat(video_path: str) -> None:
    """Cats a video file

    Args:
        video_path (str)
    """
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened() == False:
        print("Error opening video stream or file")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # bgr2rgb
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        __frameCat(Image.fromarray(frame))
        cv2.waitKey(0)