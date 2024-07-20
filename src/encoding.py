from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from PIL import Image
import numpy as np
import jpeglib
import piexif
import random
import os


def encode_file_by_appending(file_path: str, data: bytes, save_path: str):
    with open(file_path, 'rb') as f:
        image_contents = f.read()

    if os.path.isfile(save_path):
        os.remove(save_path)

    with open(save_path, 'ab') as f:
        f.write((image_contents+data))


def encode_file_by_hiding_in_metadata(file_path: str, data: bytes, save_path: str):
    image = Image.open(file_path)

    if 'exif' in image.info:
        exif_dict = piexif.load(image.info['exif'])
        exif_dict['0th'][piexif.ImageIFD.ImageDescription] = data
        exif_bytes = piexif.dump(exif_dict)

    else:
        exif_bytes = piexif.dump({'0th':{piexif.ImageIFD.ImageDescription:data}})

    image.save(save_path, exif=exif_bytes)


def encode_file_by_lsb(file_path: str, data: bytes, save_path: str):
    if save_path[-3:] == 'png':
        encode_png_file_by_lsb(file_path, data, save_path)
        return
    encode_jpg_file_by_lsb(file_path, data, save_path)


def add_character_sequence_to_lsb_data(data: bytes) -> bytes:
    # add special characters to indicate the end of the message when decoding
    data += 10 * b'`'
    return data


def encode_jpg_file_by_lsb(file_path: str, data: bytes, save_path: str):

    img = jpeglib.read_dct(file_path)
    
    data_bytes = []
    data = add_character_sequence_to_lsb_data(data)

    for character in data:
        data_bytes += [(character >> i) & 1 for i in range(8)]

    coefficient = img.Y[::8, ::8]
    original_shape = coefficient.shape
    coefficient = coefficient.flatten()
    coefficient_copy = coefficient.copy()

    for i in range(len(data_bytes)):
        if coefficient[i] % 2 != data_bytes[i]:
            coefficient_copy[i] = coefficient[i] + random.choice([-1, +1])

    img.Y[::8, ::8] = coefficient_copy.reshape(original_shape)
    img.write_dct(save_path)


def encode_png_file_by_lsb(file_path: str, data: bytes, save_path: str):
    
    data = add_character_sequence_to_lsb_data(data)

    # encode data as a series of 8 bit values
    data_bytes = ''.join(["{:08b}".format(x) for x in data])

    with Image.open(file_path) as image:
        image_width, image_height = image.size
        image_numpy_array = np.array(image)

    # flatten pixel arrays
    image_numpy_array = np.reshape(image_numpy_array, image_width*image_height*3)

    # encode data
    for x in range(len(data_bytes)):
        binary_value = "{:08b}".format(image_numpy_array[x])

        # change the least significant bit (using lsb matching)
        if (binary_value[-1] != data_bytes[x]):
            image_numpy_array[x] = int(binary_value, 2) + random.choice([+1, -1])

    # resize to original dimensions
    image_numpy_array = np.reshape(image_numpy_array, (image_height, image_width, 3))

    Image.fromarray(image_numpy_array).save(save_path)


def encode_file_by_aes_lsb(file_path: str, data: bytes, save_path: str):
    
    # encrypt data with AES
    key = get_random_bytes(16)
    aes_cipher = AES.new(key, AES.MODE_EAX)

    encrypted_data, tag = aes_cipher.encrypt_and_digest(data)
    nonce = aes_cipher.nonce

    # put all information necessary for decrypting together as binary
    payload = key + nonce + tag + encrypted_data
    payload = ''.join(["{:08b}".format(x) for x in payload])

    transformed_data = bytes(payload, encoding='utf-8')
    encode_file_by_lsb(file_path, transformed_data, save_path)
