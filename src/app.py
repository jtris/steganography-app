import tkinter
import customtkinter as ctk
from PIL import Image

from button_command_functions import *


W_WIDTH = 800
W_HEIGHT = 500
MEDIUM_FONT = ('Fixedsys', 50)
ENTRY_FONT = ('Fixedsys', 40)
ERROR_FONT = ('Fixedsys', 30)
SMALL_FONT = ('Fixedsys', 20)

ABOUT_TEXT = 'Supports JPG and PNG file types.'
ABOUT_TEXT_2 = 'Source code can be found on github.'
ABOUT_TEXT_3 = '(see github.com/jtris)'


class Root(ctk.CTk):
    def __init__(self, *args, **kwargs): # init App class
        super().__init__(*args, **kwargs) # init Tk class
        
        # variables
        self.current_process = None # either 'encode' or 'decode'
        self.encoding_technique = None # 'appending' or 'lsb' or 'lsb and grain'
        self.original_image_path = None
        self.decoded_data = None
        self.data_to_hide = None
        self.save_path = None

        # window parameters
        self.geometry(f'{W_WIDTH}x{W_HEIGHT}')
        self.resizable(False, False)
        self.title("Steganography")
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

        frames_ = [MenuFrame, AboutFrame, ImgPathFrame, EncodeTextOrFileFrame,
                    HideFileFrame, EnterMessageFrame, SaveFrame, PrintoutFrame,
                    EncodeSelectionFrame, DecodeSelectionFrame]
        
        self.frames = {}
        for frame_class in frames_:
            frame = frame_class(container_frame, self)
            self.frames[frame.__class__.__name__] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('MenuFrame')

    def show_frame(self, frame_cls_name):
        frame = self.frames[frame_cls_name]
        frame.tkraise()



# FRAMES

class MenuFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        self.title_label = ctk.CTkLabel(self, text='steganography', font=('Fixedsys', 60))
        self.title_label.place(x=W_WIDTH/2, y=90, anchor=tkinter.CENTER)

        self.button_encode = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_encode_command(controller), text='encode', font=MEDIUM_FONT,
            width=400, height=100)
        self.button_encode.place(x=W_WIDTH/2, y=W_HEIGHT/2-15, anchor=tkinter.CENTER)

        self.button_decode = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_decode_command(controller), text='decode', font=MEDIUM_FONT,
            width=400, height=100)
        self.button_decode.place(x=W_WIDTH/2, y=W_HEIGHT/2+90, anchor=tkinter.CENTER)

        self.button_about = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_about_command(controller), text='about', font=('Fixedsys', 35),
            width=200, height=50)
        self.button_about.place(x=W_WIDTH/2, y=W_HEIGHT/2+190, anchor=tkinter.CENTER)


class AboutFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        self.title1 = ctk.CTkLabel(self, text='about steganography', font=MEDIUM_FONT)
        self.title1.place(x=40, y=25)

        self.title2 = ctk.CTkLabel(self, text='and this app', font=MEDIUM_FONT)
        self.title2.place(x=40, y=85)

        self.body_text = ctk.CTkLabel(self, text=ABOUT_TEXT, font=ERROR_FONT)
        self.body_text.place(x=40, y=190)

        self.body_text_2 = ctk.CTkLabel(self, text=ABOUT_TEXT_2, font=ERROR_FONT)
        self.body_text_2.place(x=40, y=230)

        self.body_text_3 = ctk.CTkLabel(self, text=ABOUT_TEXT_3, font=ERROR_FONT)
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
            text='continue', font=MEDIUM_FONT, width=450, height=80)
        self.button_continue.place(x=30, y=390)


class EncodeSelectionFrame(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)

        self.title1 = ctk.CTkLabel(self, text='choose how you would', font=MEDIUM_FONT)
        self.title1.place(x=20, y=25)

        self.title2 = ctk.CTkLabel(self, text='like to hide the data', font=MEDIUM_FONT)
        self.title2.place(x=20, y=85)

        self.button_appending = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_encode_selection_appending_command(controller),
            text='append', font=ERROR_FONT, width=350, height=80)
        self.button_appending.place(x=30, y=190)

        self.button_metadata = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_encode_selection_metadata_command(controller),
            text='hide in metadata', font=ERROR_FONT, width=350, height=80)
        self.button_metadata.place(x=30, y=275)

        self.button_3 = ctk.CTkButton(master=self, corner_radius=15,
            command=None,
            text='', font=ERROR_FONT, width=350, height=80)
        self.button_3.place(x=30, y=360)

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
            text='appended', font=ERROR_FONT, width=350, height=80)
        self.button_appending.place(x=30, y=190)

        self.button_metadata = ctk.CTkButton(master=self, corner_radius=15,
            command=lambda:button_decode_selection_metadata_command(controller),
            text='hidden in metadata', font=ERROR_FONT, width=350, height=80)
        self.button_metadata.place(x=30, y=275)

        self.button_3 = ctk.CTkButton(master=self, corner_radius=15,
            command=None,
            text='', font=ERROR_FONT, width=350, height=80)
        self.button_3.place(x=30, y=360)

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
            text='continue', font=MEDIUM_FONT, width=450, height=80)
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
            command=lambda:button_saveframe_save_command(self, controller), text='save', font=MEDIUM_FONT, width=450, height=80)
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


# OTHER FNs
def place_home_button(master, controller):
    home_button = ctk.CTkButton(master=master, corner_radius=15, text=None,
        command=lambda:home_button_command(master, controller), image=controller.menu_icon, width=80, height=80)

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
