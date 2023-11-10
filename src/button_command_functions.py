from os import path, remove
import tkinter
from tkinter import messagebox

from encoding import encode_file
from decoding import decode_file


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
	filepath = tkinter.filedialog.askopenfilename(initialdir = "/", title = "Select a file to use: ")

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
	controller.show_frame('EncodeTextOrFileFrame')


def img_path_frame_continue_d(controller):
	try:
		controller.decoded_data = decode_file(controller.original_image_path)
	except:
		show_error_msg('an error occured while decoding the file')

	controller.frames['PrintoutFrame'].message_textbox.insert('insert', controller.decoded_data)
	controller.show_frame('PrintoutFrame')



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


def encode_and_save(controller):
	original_image_path = controller.original_image_path
	save_path = controller.save_path
	data = controller.data_to_hide

	try:
		encode_file(file_path=original_image_path, data=data, save_path=save_path)
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