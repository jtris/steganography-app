from PIL import Image
import numpy as np
import piexif
import os


def encode_file_by_appending(file_path: str, data: bytes, save_path: str) -> str:
    with open(file_path, 'rb') as f:
        image_contents = f.read()

    if os.path.isfile(save_path):
        os.remove(save_path)

    with open(save_path, 'ab') as f:
        f.write((image_contents+data).encode('utf-8'))


def encode_file_by_hiding_in_metadata(file_path: str, data: bytes, save_path: str) -> str:
    image = Image.open(file_path)

    if 'exif' in image.info:
        exif_dict = piexif.load(image.info['exif'])
        exif_dict['0th'][piexif.ImageIFD.ImageDescription] = data
        exif_bytes = piexif.dump(exif_dict)

    else:
        exif_bytes = piexif.dump({'0th':{piexif.ImageIFD.ImageDescription:data}})

    image.save(save_path, exif=exif_bytes)


def encode_file_by_lsb(file_path: str, data: bytes, save_path: str) -> str:

    data += b' \r' # include a non-printable char to indicate end of data when decoding

    # encode data as a series of 8 bit values
    data_bytes = ''.join(["{:08b}".format(x) for x in data])
    data_bytes = [int(x) for x in data_bytes]

    with Image.open(file_path) as image:
        image_width, image_height = image.size
        image_numpy_array = np.array(image)

    # flatten pixel arrays
    image_numpy_array = np.reshape(image_numpy_array, image_width*image_height*3)
    
    image_numpy_array[:len(data_bytes)] = image_numpy_array[:len(data_bytes)] & ~1 | data_bytes
    image_numpy_array = np.reshape(image_numpy_array, (image_height, image_width, 3))

    Image.fromarray(image_numpy_array).save(save_path)

