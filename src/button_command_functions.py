from os import path
from tkinter import filedialog, messagebox

from encoding import *
from decoding import *


def show_error_msg(message):
    messagebox.showerror('ERROR', message)


def home_button_command(master_frame, controller):
    controller.show_frame('MenuFrame')
    
    # delete inputs and error messages
    frame_name = master_frame.__class__.__name__
    if frame_name in ['ImgPathFrame', 'HideFileFrame', 'SaveFrame']:
        master_frame.error_label.place_forget()
        master_frame.entry.delete(0, 'end')
    elif frame_name == 'EnterMessageFrame':
        master_frame.message_textbox.delete('0.0', 'end')


def button_file_explorer_command(master_frame, controller, current_frame):
    filepath = filedialog.askopenfilename(initialdir = "/", title = "Select a file to use: ")

    if not path.isfile(filepath):
        return

    master_frame.error_label.place_forget()

    if current_frame == 'ImgPathFrame':
        controller.original_image_path = filepath

        if controller.current_process == 'encode':
            img_path_frame_continue_e(controller)
        else:
            img_path_frame_continue_d(controller)

    elif current_frame == 'HideFileFrame':
        button_hidefile_file_explorer_command(controller, filepath)

    elif current_frame == 'SaveFrame':
        controller.save_path = filepath
        if controller.current_process == 'encode':
            encode_and_save(controller)
        else:
            save_decoded(controller)
        controller.show_frame('MenuFrame')


# MenuFrame button functions
def button_encode_command(controller):
    controller.current_process = 'encode'
    controller.show_frame('ImgPathFrame')


def button_decode_command(controller):
    controller.current_process = 'decode'
    controller.show_frame('ImgPathFrame')


def button_about_command(controller):
    controller.show_frame('AboutFrame')


# ImgPathFrame button functions
def button_imgpath_continue_command(master_frame, controller):
    entry_input = master_frame.entry.get().strip()
    master_frame.entry.delete(0, 'end')

    if not path.isfile(entry_input):
        master_frame.error_label.place(x=35, y=280)
        return

    # hide the error label
    master_frame.error_label.place_forget()

    controller.original_image_path = entry_input
    if controller.current_process == 'encode':
        img_path_frame_continue_e(controller)
    else:
        img_path_frame_continue_d(controller)


def img_path_frame_continue_e(controller):
    controller.show_frame('EncodeSelectionFrame')


def img_path_frame_continue_d(controller):
    controller.show_frame('DecodeSelectionFrame')


# DecodeSelectionFrame button functions
def button_decode_selection_command(controller):
    try:
        if controller.encoding_technique == 'appending':
               controller.decoded_data = decode_file_appending(controller.original_image_path)

        elif controller.encoding_technique == 'metadata':
            controller.decoded_data = decode_file_metadata(controller.original_image_path)

        elif controller.encoding_technique == 'lsb':
            controller.decoded_data = decode_file_lsb(controller.original_image_path)

        elif controller.encoding_technique == 'aes+lsb':
            controller.decoded_data = decode_file_aes_lsb(controller.original_image_path)

        elif controller.encoding_technique == 'rsa+aes+lsb':
            controller.decoded_data = 'TEMP'

    except:
       show_error_msg('an error occured while decoding the file')

    _button_decode_selection_continuation(controller)


def button_decode_selection_appending_command(controller):
    controller.encoding_technique = 'appending'
    button_decode_selection_command(controller)


def button_decode_selection_metadata_command(controller):
    controller.encoding_technique = 'metadata'
    button_decode_selection_command(controller)


def button_decode_selection_lsb_command(controller):
    controller.encoding_technique = 'lsb'
    button_decode_selection_command(controller)


def button_decode_selection_aes_lsb_command(controller):
    controller.encoding_technique = 'aes+lsb'
    button_decode_selection_command(controller)


def button_decode_selection_rsa_aes_lsb_command(controller):
    controller.show_frame('EnterKeyFrame')


def _button_decode_selection_continuation(controller):
    controller.frames['PrintoutFrame'].message_textbox.delete('0.0', 'end')
    controller.frames['PrintoutFrame'].message_textbox.insert('insert', str(controller.decoded_data))
    controller.show_frame('PrintoutFrame')


# EncodeSelectionFrame button functions
def button_encode_selection_appending_command(controller):
    controller.encoding_technique = 'appending'
    controller.show_frame('EncodeTextOrFileFrame')


def button_encode_selection_metadata_command(controller):
    controller.encoding_technique = 'metadata'
    controller.show_frame('EncodeTextOrFileFrame')


def button_encode_selection_lsb_command(controller):
    controller.encoding_technique = 'lsb'
    controller.show_frame('EncodeTextOrFileFrame')


def button_encode_selection_aes_lsb_command(controller):
    controller.encoding_technique = 'aes+lsb'
    controller.show_frame('EncodeTextOrFileFrame')


def button_encode_selection_rsa_aes_lsb_command(controller):
    controller.encoding_technique = 'rsa+aes+lsb'
    controller.show_frame('EncodeTextOrFileFrame')


# EncodeTextOrFileFrame button functions
def button_hide_file_command(controller):
    controller.show_frame('HideFileFrame')


def button_enter_message_command(controller):
    controller.show_frame('EnterMessageFrame')


# HideFileFrame button functions
def button_hidefile_file_explorer_command(controller, file_to_hide_path):
    try:
        with open(file_to_hide_path, 'rb') as f:
            controller.data_to_hide = f.read()      
    except:
        show_error_msg('an error occured while trying to read a file')

    controller.show_frame('SaveFrame')


def button_hidefile_continue_command(master_frame, controller):
    entry_input = master_frame.entry.get().strip()
    master_frame.entry.delete(0, 'end')

    if not path.isfile(entry_input):
        master_frame.error_label.place(x=35, y=280)
        return

    with open(entry_input, 'rb') as f:
        controller.data_to_hide = f.read()

    master_frame.error_label.place_forget()
    controller.show_frame('SaveFrame')


def button_entermessageframe_save_command(master_frame, controller):
    controller.data_to_hide = bytes(master_frame.message_textbox.get('0.0', 'end'), 'utf-8')
    master_frame.message_textbox.delete('0.0', 'end')
    controller.show_frame('SaveFrame')


# PrintoutFrame
def button_save_printoutframe_command(controller):
    controller.show_frame('SaveFrame')


# SaveFrame
def button_saveframe_save_command(master_frame, controller):
    entry_input = master_frame.entry.get().strip()
    master_frame.entry.delete(0, 'end')

    try:
        with open(entry_input, 'a+') as f:
            pass
    except:
        master_frame.error_label.place(x=35, y=280)
        return

    controller.save_path = entry_input
    master_frame.error_label.place_forget()
    
    if controller.current_process == 'encode':
        encode_and_save(controller)
    elif controller.current_process == 'decode':
        save_decoded(controller)

    controller.show_frame('MenuFrame')
    

def encode_and_save(controller):
    original_image_path = controller.original_image_path
    save_path = controller.save_path
    data = controller.data_to_hide

    try:
        if controller.encoding_technique == 'appending':
            encode_file_by_appending(file_path=original_image_path, data=data, save_path=save_path)
   
        elif controller.encoding_technique == 'metadata':
            encode_file_by_hiding_in_metadata(file_path=original_image_path, data=data, save_path=save_path)

        elif controller.encoding_technique == 'lsb':
            encode_file_by_lsb(file_path=original_image_path, data=data, save_path=save_path)

        elif controller.encoding_technique == 'aes+lsb':
            encode_file_by_aes_lsb(file_path=original_image_path, data=data, save_path=save_path)

    except:
       show_error_msg('an error occured while encoding or saving the file')


def save_decoded(controller):
    data = controller.decoded_data
    save_path = controller.save_path

    try:
        with open(save_path, 'w') as f:
            f.write(data)

    except:
        show_error_msg('an error occured while saving the file')


# EnterKeyFrame

def _decode_rsa_aes_lsb(key_path):
    # parse the json file
    # assemble the key
    # decrypt
    return ''


def button_enterkeyframe_continue_command(master_frame, controller):

    controller.encoding_technique = 'rsa+aes+lsb'
    button_decode_selection_command(controller)

    '''
    entry_input = master_frame.entry.get().strip()
    master_frame.entry.delete(0, 'end')

    try:
        with open(entry_input, 'r') as f:
            pass
    except:
        master_frame.error_label.place(x=35, y=280)
        return

    # if entry_input[-5:] != '.json':
    #     master_frame.error_label.place(x=35, y=280)
    #     return

    controller.decoded_data = _decode_rsa_aes_lsb(entry_input)
    master_frame.error_label.place_forget()
    
    controller.show_frame('PrintoutFrame')
    '''
