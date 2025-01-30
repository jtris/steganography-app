from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from PIL import Image
from tkinter import messagebox
import numpy as np
import jpeglib
import piexif
import random
import os

from mode_to_bit_depth import get_bit_depth


''' appending '''

def encode_file_by_appending(file_path: str, data: bytes, save_path: str):
    with open(file_path, 'rb') as f:
        image_contents = f.read()

    if os.path.isfile(save_path):
        os.remove(save_path)

    with open(save_path, 'ab') as f:
        f.write((image_contents+data))


''' metadata '''

def encode_file_by_hiding_in_metadata(file_path: str, data: bytes, save_path: str):
    image = Image.open(file_path)

    if 'exif' in image.info:
        exif_dict = piexif.load(image.info['exif'])
        exif_dict['0th'][piexif.ImageIFD.ImageDescription] = data
        exif_bytes = piexif.dump(exif_dict)

    else:
        exif_bytes = piexif.dump({'0th':{piexif.ImageIFD.ImageDescription:data}})

    image.save(save_path, exif=exif_bytes)


''' lsb matching '''
def _handle_data_too_large_error(controller):
    messagebox.showerror('ERROR', 'Data size is too large to use in conjuction with LSB encoding and this image.')

    controller.show_frame('MenuFrame')
    controller.reset_title()
    controller.clear_data()


def encode_file_by_lsb(file_path: str, data: bytes, save_path: str, controller):
    if save_path[-3:] == 'png':
        encode_png_file_by_lsb(file_path, data, save_path, controller)
        return
    encode_jpg_file_by_lsb(file_path, data, save_path, controller)


def add_character_sequence_to_lsb_data(data: bytes) -> bytes:
    # add special characters to indicate the end of the message when decoding
    data += 10 * b'`'
    return data


def encode_jpg_file_by_lsb(file_path: str, data: bytes, save_path: str, controller):

    img = jpeglib.read_dct(file_path)
    
    data_bytes = []
    data = add_character_sequence_to_lsb_data(data)

    for character in data:
        data_bytes += [(character >> i) & 1 for i in range(8)]

    coefficient = img.Y[::8, ::8]
    original_shape = coefficient.shape
    coefficient = coefficient.flatten()
    coefficient_copy = coefficient.copy()

    try:
        for i in range(len(data_bytes)):
           if coefficient[i] % 2 != data_bytes[i]:
               coefficient_copy[i] = coefficient[i] + random.choice([-1, +1])
    except IndexError:
        _handle_data_too_large_error(controller)
        return

    img.Y[::8, ::8] = coefficient_copy.reshape(original_shape)
    img.write_dct(save_path)


def encode_png_file_by_lsb(file_path: str, data: bytes, save_path: str, controller):
    
    data = add_character_sequence_to_lsb_data(data)

    # encode data as a series of 8 bit values
    data_bytes = ''.join(["{:08b}".format(x) for x in data])

    with Image.open(file_path) as image:
        image_bit_depth = get_bit_depth(image.mode)

        # convert to a suitable format for PIL
        if image_bit_depth < 24:
            image = image.convert() # converts to bit-depth of 32
            image_bit_depth = get_bit_depth(image.mode)

        image_width, image_height = image.size
        image_numpy_array = np.array(image)

    # flatten pixel arrays
    image_numpy_array = np.reshape(image_numpy_array, image_width*image_height*image_bit_depth//8)

    # encode data
    try:
        for x in range(len(data_bytes)):
            binary_value = "{:08b}".format(image_numpy_array[x])
     
            # change the least significant bit (using lsb matching)
            if (binary_value[-1] != data_bytes[x]):
                image_numpy_array[x] = int(binary_value, 2) + random.choice([+1, -1])
    except IndexError:
        _handle_data_too_large_error(controller)
        return

    # resize to original dimensions
    image_numpy_array = np.reshape(image_numpy_array, (image_height, image_width, image_bit_depth//8))

    Image.fromarray(image_numpy_array).save(save_path)


''' aes + lsb matching '''

def encode_file_by_aes_lsb(file_path: str, data: bytes, save_path: str, controller):
    key = get_random_bytes(32)
    aes_cipher = AES.new(key, AES.MODE_EAX)

    encrypted_data, tag = aes_cipher.encrypt_and_digest(data)
    nonce = aes_cipher.nonce

    payload = nonce + tag + encrypted_data
    payload = ''.join(["{:08b}".format(x) for x in payload])

    transformed_data = bytes(payload, encoding='utf-8')
    encode_file_by_lsb(file_path, transformed_data, save_path, controller)

    # export aes key
    key_save_path = os.path.dirname(save_path) + '/aes_key.pem'
    with open(key_save_path, 'wb') as f:
        f.write(key)


''' rsa + aes + lsb matching '''

def _get_save_path_directory(save_path):
    last_slash = save_path.rfind('/')
    return save_path[:last_slash+1]


def encode_file_by_rsa_aes_lsb(file_path: str, data: bytes, rsa_key_path: str, save_path: str, controller):
    # encrypt data with AES
    aes_key = get_random_bytes(16)
    aes_cipher = AES.new(aes_key, AES.MODE_EAX)

    aes_encrypted_data, tag = aes_cipher.encrypt_and_digest(data)
    nonce = aes_cipher.nonce

    rsa_payload = aes_key + nonce + tag
    with open(rsa_key_path, 'rb') as f:
        rsa_public_key = RSA.import_key(f.read())

    rsa_cipher = PKCS1_v1_5.new(rsa_public_key)
    rsa_ciphertext = rsa_cipher.encrypt(rsa_payload) # always ends up being 128 bytes long

    # encode with lsb
    lsb_payload = rsa_ciphertext + aes_encrypted_data
    lsb_payload = bytes(''.join(["{:08b}".format(x) for x in lsb_payload]), encoding='utf-8')
    encode_file_by_lsb(file_path, lsb_payload, save_path, controller)


def generate_and_save_rsa_keys(save_path: str):
    private_rsa_key = RSA.generate(2048)
    public_rsa_key = private_rsa_key.public_key()

    with open(save_path + '/private_rsa_key.pem', 'wb') as f:
        f.write(private_rsa_key.exportKey('PEM'))

    with open(save_path + '/public_rsa_key.pem', 'wb') as f:
        f.write(public_rsa_key.exportKey('PEM'))

