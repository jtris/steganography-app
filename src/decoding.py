from PIL import Image
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

