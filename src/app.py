import tkinter
import customtkinter as ctk
from PIL import Image

from button_command_functions import *


W_WIDTH = 800
W_HEIGHT = 500
LARGE_TITLE_FONT = ('Fixedsys', 60)
MEDIUM_FONT = ('Fixedsys', 50)
ENTRY_FONT = ('Fixedsys', 40)
ERROR_FONT = ('Fixedsys', 30)
SMALL_TITLE_FONT = ('Fixedsys', 30)
SMALL_FONT = ('Fixedsys', 20)

DEFAULT_WINDOW_TITLE = 'Steganography'

ABOUT_TEXT = 'Supports JPG and PNG file types.'
ABOUT_TEXT_2 = 'Source code can be found on github.'
ABOUT_TEXT_3 = '(see github.com/jtris)'


class Root(ctk.CTk):
    def __init__(self, *args, **kwargs): # init App class
        super().__init__(*args, **kwargs) # init Tk class
        ctk.set_appearance_mode('light')
        
        # variables
        self.current_process = None # either 'encode' or 'decode'
        self.encoding_technique = None 
        self.original_image_path = None
        self.decoded_data = None
        self.data_to_hide = None
        self.save_path = None
        self.key_path = None

        # window parameters
        self.geometry(f'{W_WIDTH}x{W_HEIGHT}')
        self.resizable(False, False)
        self.title(DEFAULT_WINDOW_TITLE)
        ctk.set_default_color_theme("green")

        # container frame
        container_frame = tkinter.Frame(self)
        container_frame.pack(side='top', fill='both', expand=True)
        container_frame.grid_rowconfigure(0, weight=1)
        container_frame.grid_columnconfigure(0, weight=1)

        # icons
        self.menu_icon = ctk.CTkImage(light_image=Image.open('assets/menu_icon.png'), size=(50, 50))
        self.file_explorer_icon = ctk.CTkImage(light_image=Image.open('assets/file_explorer_icon.png'), size=(60, 50))
        self.save_icon = ctk.CTkImage(light_image=Image.open('assets/save_icon.png'), size=(40, 40))

        _frames = [MenuFrame, OtherOptionsFrame, AboutFrame, ImgPathFrame, EncodeTextOrFileFrame,
                    HideFileFrame, EnterMessageFrame, SaveFrame, PrintoutFrame,
                    EncodeSelectionFrame, DecodeSelectionFrame, EnterKeyFrame,
                    AutoDecodingPrintoutFrame, GenerateRSAKeysFrame]
        
        self.frames = {}
        for frame_class in _frames:
            frame = frame_class(container_frame, self)
            self.frames[frame.__class__.__name__] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('MenuFrame')

    def clear_data(self):
        self.current_process = None 
        self.encoding_technique = None 
        self.original_image_path = None
        self.decoded_data = None
        self.data_to_hide = None
        self.save_path = None
        self.key_path = None

    def show_frame(self, frame_cls_name):
        frame = self.frames[frame_cls_name]
        frame.tkraise()

    def append_to_title(self, text: str):
        self.title(self.title() + ' / '+ text)

    def reset_title(self):
        self.title(DEFAULT_WINDOW_TITLE)



# FRAMES

class MenuFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        self.title_label = ctk.CTkLabel(self, text='steganography', font=LARGE_TITLE_FONT)
        self.title_label.place(x=W_WIDTH/2, y=90, anchor=tkinter.CENTER)

        self.button_encode = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_encode_command(controller), text='encode', font=MEDIUM_FONT,
            width=400, height=100)
        self.button_encode.place(x=W_WIDTH/2, y=W_HEIGHT/2-15, anchor=tkinter.CENTER)

        self.button_decode = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_decode_command(controller), text='decode', font=MEDIUM_FONT,
            width=400, height=100)
        self.button_decode.place(x=W_WIDTH/2, y=W_HEIGHT/2+90, anchor=tkinter.CENTER)

        self.button_other = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_other_command(controller), text='other', font=('Fixedsys', 35),
            width=200, height=50)
        self.button_other.place(x=W_WIDTH/2, y=W_HEIGHT/2+190, anchor=tkinter.CENTER)


class OtherOptionsFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        self.title = ctk.CTkLabel(self, text='other options:', font=MEDIUM_FONT)
        self.title.place(x=30, y=35)

        self.button_about = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_about_command(controller),
            text='about this app', font=MEDIUM_FONT, width=580, height=125)
        self.button_about.place(x=W_WIDTH/2, y=210, anchor=tkinter.CENTER)

        self.button_generate_rsa_keys = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_generate_rsa_keys_command(controller),
            text='generate RSA keys', font=MEDIUM_FONT, width=580, height=125)
        self.button_generate_rsa_keys.place(x=W_WIDTH/2, y=340, anchor=tkinter.CENTER)

        place_home_button(master=self, controller=controller)


class AboutFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        self.title1 = ctk.CTkLabel(self, text='about steganography', font=MEDIUM_FONT)
        self.title1.place(x=40, y=25)

        self.title2 = ctk.CTkLabel(self, text='and this app', font=MEDIUM_FONT)
        self.title2.place(x=40, y=85)

        self.body_text = ctk.CTkLabel(self, text=ABOUT_TEXT, font=SMALL_TITLE_FONT)
        self.body_text.place(x=40, y=190)

        self.body_text_2 = ctk.CTkLabel(self, text=ABOUT_TEXT_2, font=SMALL_TITLE_FONT)
        self.body_text_2.place(x=40, y=230)

        self.body_text_3 = ctk.CTkLabel(self, text=ABOUT_TEXT_3, font=SMALL_TITLE_FONT)
        self.body_text_3.place(x=40, y=270)

        place_home_button(master=self, controller=controller)


class ImgPathFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        self.title1 = ctk.CTkLabel(self, text='choose an image file', font=MEDIUM_FONT)
        self.title1.place(x=20, y=25)

        self.title2 = ctk.CTkLabel(self, text='or enter the path', font=MEDIUM_FONT)
        self.title2.place(x=20, y=85)

        self.error_label = ctk.CTkLabel(self, text='enter a valid path', # only defined
            text_color='red', font=ERROR_FONT, fg_color='transparent')

        place_home_button(self, controller)

        self.entry = ctk.CTkEntry(self, font=ENTRY_FONT,
            width=600, height=100, corner_radius=15)
        self.entry.place(x=30, y=170)

        place_file_explorer_button(master=self, controller=controller, current_frame='ImgPathFrame')

        self.button_continue = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_imgpath_continue_command(self, controller),
            text='continue', font=MEDIUM_FONT, width=350, height=80)
        self.button_continue.place(x=30, y=390)


class EncodeSelectionFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        self.title1 = ctk.CTkLabel(self, text='choose how you would', font=MEDIUM_FONT)
        self.title1.place(x=20, y=25)

        self.title2 = ctk.CTkLabel(self, text='like to hide the data', font=MEDIUM_FONT)
        self.title2.place(x=20, y=85)

        self.button_appending = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_encode_selection_command(controller, 'appending'),
            text='append', font=SMALL_TITLE_FONT, width=350, height=80)
        self.button_appending.place(x=40, y=175)

        self.button_metadata = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_encode_selection_command(controller, 'metadata'),
            text='hide in metadata', font=SMALL_TITLE_FONT, width=350, height=80)
        self.button_metadata.place(x=40, y=265)

        self.button_lsb = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_encode_selection_command(controller, 'lsb'),
            text='LSB', font=SMALL_TITLE_FONT, width=350, height=80)
        self.button_lsb.place(x=40, y=355)

        self.button_aes_lsb = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_encode_selection_command(controller, 'aes+lsb'),
            text='AES + LSB', font=SMALL_TITLE_FONT, width=350, height=80)
        self.button_aes_lsb.place(x=400, y=175)

        self.button_rsa_aes_lsb = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_encode_selection_rsa_aes_lsb_command(controller),
            text='RSA + AES + LSB', font=SMALL_TITLE_FONT, width=350, height=80)
        self.button_rsa_aes_lsb.place(x=400, y=265)

        self.button_generate_rsa_keys = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_generate_rsa_keys_command(controller),
            text='generate RSA keys', font=SMALL_TITLE_FONT, width=350, height=80)
        self.button_generate_rsa_keys.place(x=400, y=355)

        place_home_button(self, controller)


class DecodeSelectionFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        self.title1 = ctk.CTkLabel(self, text='choose how the data', font=MEDIUM_FONT)
        self.title1.place(x=20, y=25)

        self.title2 = ctk.CTkLabel(self, text='was hidden', font=MEDIUM_FONT)
        self.title2.place(x=20, y=85)

        self.button_appending = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_decode_selection_appending_command(controller),
            text='appended', font=SMALL_TITLE_FONT, width=350, height=80)
        self.button_appending.place(x=40, y=175)

        self.button_metadata = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_decode_selection_metadata_command(controller),
            text='hidden in metadata', font=SMALL_TITLE_FONT, width=350, height=80)
        self.button_metadata.place(x=40, y=265)

        self.button_lsb = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_decode_selection_lsb_command(controller),
            text='LSB', font=SMALL_TITLE_FONT, width=350, height=80)
        self.button_lsb.place(x=40, y=355)

        self.button_aes_lsb = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_decode_selection_aes_lsb_command(controller),
            text='AES + LSB', font=SMALL_TITLE_FONT, width=350, height=80)
        self.button_aes_lsb.place(x=400, y=175)

        self.button_rsa_aes_lsb = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_decode_selection_rsa_aes_lsb_command(controller),
            text='RSA + AES + LSB', font=SMALL_TITLE_FONT, width=350, height=80)
        self.button_rsa_aes_lsb.place(x=400, y=265)

        self.button_auto = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_auto_decode(controller),
            text='*auto', font=SMALL_TITLE_FONT, width=350, height=80)
        self.button_auto.place(x=400, y=355)

        place_home_button(self, controller)


class EncodeTextOrFileFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        place_home_button(self, controller)

        self.button_hide_file = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_hide_file_command(controller), text='hide contents\nof a file',
            font=MEDIUM_FONT, width=520, height=150)
        self.button_hide_file.place(x=W_WIDTH/2, y=190, anchor=tkinter.CENTER)

        self.button_enter_message = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_enter_message_command(controller), text='enter a message',
            font=MEDIUM_FONT, width=520, height=100)
        self.button_enter_message.place(x=W_WIDTH/2, y=322, anchor=tkinter.CENTER)


class HideFileFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        place_home_button(self, controller)

        self.title1 = ctk.CTkLabel(self, text='choose a file', font=MEDIUM_FONT)
        self.title1.place(x=20, y=25)

        self.title2 = ctk.CTkLabel(self, text='or enter the path', font=MEDIUM_FONT)
        self.title2.place(x=20, y=85)

        self.error_label = ctk.CTkLabel(self, text='enter a valid path',
            text_color='red', font=ERROR_FONT, fg_color='transparent')

        self.entry = ctk.CTkEntry(self, font=ENTRY_FONT,
            width=600, height=100, corner_radius=15)
        self.entry.place(x=30, y=170)

        place_file_explorer_button(master=self, controller=controller, current_frame='HideFileFrame')

        self.button_continue = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_hidefile_continue_command(self, controller),
            text='continue', font=MEDIUM_FONT, width=350, height=80)
        self.button_continue.place(x=30, y=390)


class EnterMessageFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        place_home_button(self, controller)

        self.title = ctk.CTkLabel(self, text='enter a message:', font=MEDIUM_FONT)
        self.title.place(x=30, y=35)

        self.message_textbox = ctk.CTkTextbox(self, width=600, height=240, corner_radius=15,
            fg_color='transparent', font=ENTRY_FONT, border_color='dark grey', border_width=2)
        self.message_textbox.place(x=30, y=120)

        self.save_button = ctk.CTkButton(self, corner_radius=15,
            command=lambda:button_entermessageframe_save_command(self, controller), text='save',
            font=MEDIUM_FONT, width=200, height=80)
        self.save_button.place(x=30, y=390)


class SaveFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        place_home_button(self, controller)

        self.title1 = ctk.CTkLabel(self, text='choose or enter', font=MEDIUM_FONT)
        self.title1.place(x=20, y=25)

        self.title2 = ctk.CTkLabel(self, text='the save path', font=MEDIUM_FONT)
        self.title2.place(x=20, y=85)

        self.error_label = ctk.CTkLabel(self, text='enter a valid path',
            text_color='red', font=ERROR_FONT, fg_color='transparent')

        self.entry = ctk.CTkEntry(self, font=ENTRY_FONT,
            width=600, height=100, corner_radius=15)
        self.entry.place(x=30, y=170)

        place_file_explorer_button(master=self, controller=controller, current_frame='SaveFrame')

        self.button_save = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_saveframe_save_command(self, controller),
            text='save', font=MEDIUM_FONT, width=350, height=80)
        self.button_save.place(x=30, y=390)


class PrintoutFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        place_home_button(self, controller)

        self.save_button = ctk.CTkButton(master=self, corner_radius=15, text=None,
            command=lambda:button_save_printoutframe_command(controller), image=controller.save_icon, width=85, height=80)
        self.save_button.place(x=690, y=125)

        self.message_textbox = ctk.CTkTextbox(self, width=630, height=440, corner_radius=15,
            fg_color='transparent', font=SMALL_FONT, border_color='dark grey', border_width=2)
        self.message_textbox.place(x=30, y=30)


class AutoDecodingPrintoutFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        place_home_button(self, controller)

        self.title_text = 'data hidden with: '
        self.title = ctk.CTkLabel(self, text=self.title_text, font=SMALL_TITLE_FONT)
        self.title.place(x=30, y=25)

        self.save_button = ctk.CTkButton(master=self, corner_radius=15, text=None,
            command=lambda:button_save_printoutframe_command(controller), image=controller.save_icon, width=85, height=80)
        self.save_button.place(x=690, y=125)

        self.message_textbox = ctk.CTkTextbox(self, width=630, height=380, corner_radius=15,
            fg_color='transparent', font=SMALL_FONT, border_color='dark grey', border_width=2)
        self.message_textbox.place(x=30, y=80)


class EnterKeyFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        place_home_button(self, controller)

        self.title1 = ctk.CTkLabel(self, text='choose or enter', font=MEDIUM_FONT)
        self.title1.place(x=20, y=25)

        self.title2 = ctk.CTkLabel(self, text='the key path (.pem)', font=MEDIUM_FONT)
        self.title2.place(x=20, y=85)

        self.error_label = ctk.CTkLabel(self, text='enter a valid path',
            text_color='red', font=ERROR_FONT, fg_color='transparent')

        self.entry = ctk.CTkEntry(self, font=ENTRY_FONT,
            width=600, height=100, corner_radius=15)
        self.entry.place(x=30, y=170)

        place_file_explorer_button(master=self, controller=controller, current_frame='EnterKeyFrame')

        self.button_save = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_enterkeyframe_continue_command(self, controller),
            text='continue', font=MEDIUM_FONT, width=350, height=80)
        self.button_save.place(x=30, y=390)


class GenerateRSAKeysFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        place_home_button(self, controller)

        self.title1 = ctk.CTkLabel(self, text='choose/enter where', font=MEDIUM_FONT)
        self.title1.place(x=20, y=25)

        self.title2 = ctk.CTkLabel(self, text='to save the keys', font=MEDIUM_FONT)
        self.title2.place(x=20, y=85)

        self.error_label = ctk.CTkLabel(self, text='enter a valid path',
            text_color='red', font=ERROR_FONT, fg_color='transparent')

        self.entry = ctk.CTkEntry(self, font=ENTRY_FONT,
            width=600, height=100, corner_radius=15)
        self.entry.place(x=30, y=170)

        place_file_explorer_button(master=self, controller=controller, current_frame='GenerateRSAKeysFrame')

        self.button_save = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_generate_rsa_keys_continue_command(self, controller),
            text='continue', font=MEDIUM_FONT, width=350, height=80)
        self.button_save.place(x=30, y=390)


# OTHER FNs
def place_home_button(master, controller):
    home_button = ctk.CTkButton(master=master, corner_radius=15, text=None,
        command=lambda:home_button_command(controller, master), image=controller.menu_icon, width=80, height=80)

    home_button.place(x=690, y=25)


def place_file_explorer_button(master, controller, current_frame):
    fe_button = ctk.CTkButton(master=master, corner_radius=15, text=None,
        command=lambda:button_file_explorer_command(master, controller, current_frame),
        image=controller.file_explorer_icon, width=100, height=100,
        hover_color='white', fg_color='white', border_width=2, border_color='dark grey')

    fe_button.place(x=640, y=170)


if __name__ == '__main__':
    root = Root()
    root.mainloop()
