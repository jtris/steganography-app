from Crypto.Cipher import AES
from binascii import unhexlify
from PIL import Image
import numpy as np
import jpeglib
import piexif


''' appending '''

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


''' metadata'''

def decode_file_metadata(image_path: str):
    image = Image.open(image_path)
    contents = piexif.load(image.info['exif'])['0th'][piexif.ImageIFD.ImageDescription].decode('utf-8')
    return contents


''' lsb matching'''

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


''' aes + lsb matching '''

def _get_16_bit_value_from_encrypted_message(data_index, encrypted_message):
    values_list = []
    data_length_bits = 16 * 8 # 16 bytes
    
    for i in range(16):

        start_offset = i * 8
        start_index = data_length_bits * data_index + start_offset

        end_offset = (i + 1) * 8
        end_index = data_length_bits * data_index + end_offset

        binary_value = encrypted_message[start_index : end_index]
        values_list.append(binary_value)

    return values_list


def _binary_to_byte_string(binary_list: list):
    result = b''

    for value in binary_list:
        int_value = int(value, 2)

        if int_value < 127:
            char_value = chr(int_value)
            byte_value = bytes(char_value, encoding='utf-8')
        else:
            hex_value = hex(int_value)
            hex_value = hex_value[2:] # remove the '0x' prefix
            byte_value = unhexlify(hex_value) # convert to bytes

        result += byte_value
    
    return result


def _get_aes_lsb_encrypted_value(index, encrypted_message):

    value = _get_16_bit_value_from_encrypted_message(data_index=index, encrypted_message=encrypted_message)
    value = _binary_to_byte_string(value)
    return value


def _transform_ciphertext_into_list_of_binary_values(ciphertext):

    ciphertext_list = []
    number_of_bytes = len(ciphertext)//8

    for i in range(number_of_bytes):
        ciphertext_list.append(ciphertext[:8])
        ciphertext = ciphertext[8:]
    
    return ciphertext_list


def decode_file_aes_lsb(image_path: str):

    if image_path[-3:] in ['png', 'bmp']:
        encrypted_message = decode_png_file_lsb(image_path)
    else:
        encrypted_message = decode_jpg_file_lsb(image_path)

    key = _get_aes_lsb_encrypted_value(index=0, encrypted_message=encrypted_message)
    nonce = _get_aes_lsb_encrypted_value(index=1, encrypted_message=encrypted_message)
    tag = _get_aes_lsb_encrypted_value(index=2, encrypted_message=encrypted_message)

    component_length = 16 * 8 # length of the key, nonce, or tag in bits, each 16 bytes
    ciphertext = encrypted_message[3*component_length:]
    ciphertext = _transform_ciphertext_into_list_of_binary_values(ciphertext)
    ciphertext = _binary_to_byte_string(ciphertext)

    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
