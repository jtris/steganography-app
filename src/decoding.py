from PIL import Image
import numpy as np
import piexif


def decode_file_appending(image_path: str):
    
    if 'png' in image_path[-4:]:
        EOF_BYTES = 'IEND\\xaeB`\\x82' # png option
        CONTENT_OFFSET = 14
    else:
        EOF_BYTES = '\\xff\\xd9' # default: jpg
        CONTENT_OFFSET = 8


    with open(image_path, 'rb') as f:
        contents = str(f.read())

    text_start_index = contents.index(EOF_BYTES) + CONTENT_OFFSET

    return contents[text_start_index:-1]


def decode_file_metadata(image_path: str):
    image = Image.open(image_path)
    contents = piexif.load(image.info['exif'])['0th'][piexif.ImageIFD.ImageDescription].decode('utf-8')
    return contents


def decode_file_lsb(image_path: str):

    with Image.open(image_path) as image:
        image_width, image_height = image.size
        image_numpy_array = np.array(image)

    image_numpy_array = np.reshape(image_numpy_array, image_width*image_height*3)
    image_numpy_array = image_numpy_array & 1
    image_numpy_array = np.packbits(image_numpy_array)

    contents = ''

    for x in image_numpy_array:
        if chr(x) == '\r':
            break;

        if chr(x).isprintable():
            contents += chr(x)

    return contents

