from PIL import Image
import numpy as np
import jpeglib
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


def filter_message(data: str) -> str:
    # finds end of message indicated by a sequence of special characters
    try:
        return data[:data.index(10*'`')]

    except ValueError:
        return data


def decode_file_lsb(image_path: str):
    if image_path[-3:] == 'png':
        return decode_png_file_lsb(image_path)

    return decode_jpg_file_lsb(image_path)


def decode_jpg_file_lsb(image_path: str):
    img = jpeglib.read_dct(image_path)
    coefficient = img.Y[::8, ::8].flatten()

    message_bytes = [int(byte)%2 for byte in coefficient]

    contents = []
    byte_value = 0

    for i in range(len(message_bytes)):
        if i % 8 == 0 and i != 0:
            contents.append(byte_value)
            byte_value = 0

        byte_value |= message_bytes[i] << i % 8

    contents = ''.join([chr(c) for c in contents])
    return filter_message(contents)


def decode_png_file_lsb(image_path: str):

    with Image.open(image_path) as image:
        image_width, image_height = image.size
        image_numpy_array = np.array(image)

    image_numpy_array = np.reshape(image_numpy_array, image_width*image_height*3)
    image_numpy_array = image_numpy_array & 1
    image_numpy_array = np.packbits(image_numpy_array)

    contents = ''

    for x in image_numpy_array:

        if chr(x).isprintable():
            contents += chr(x)

    return filter_message(contents)

