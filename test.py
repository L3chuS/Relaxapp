import tkinter as tk
import customtkinter as ctk
import Database.database as bd
from Database.presets_values import user, databases, tables
from os import path
import ctypes
import time
import threading
import pygame
from PIL import Image
from tktooltip import ToolTip
import datetime

# Connect to the database.
database = bd.Database(**bd.root_access)

# Get the windows resolution regardless of rescaling
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

# Get the parent folder path and the image folder path.
main_path = path.dirname(__file__)
main_path_edited = ""

# Bucle that changes "\" for "/" because mysql don't accept first value.
for letters in main_path:
    if letters != "\\":
        main_path_edited += letters
    else:
        main_path_edited += "/"

# First letter is changed to upper.
main_path_edited = main_path_edited.replace(main_path_edited[0], main_path_edited[0].upper(), 1)

# Main used path are linked.
image_path = main_path_edited + "/Images/"
sounds_path = main_path_edited + "/Sounds/"

# Set appearance.
appearance = ctk.set_appearance_mode("dark")
color_theme = ctk.set_default_color_theme("green")

# Dictionary to set colors of the app.
colors = {"black":"#242424",
          "white":"white",
          "soft_grey":"#2b2b2b",
          "dark_green":"#0a4e50",       
          "soft_green":"#118589"}

# Set App font.
font = "Segoe Print"

#######################################################
### Class that contains general settings of the App ###
#######################################################

class RelaxApp_Structure:

    def __init__(self, root):
        
        self.root = root

        # Set the width, height, configuration and location of the windows.
        width = 350
        height = 500
        width_resolution = self.root.winfo_screenwidth() // 2 - width // 2 - width // 3
        height_resolution = self.root.winfo_screenheight() // 2 - height
        self.dimentions = self.root.geometry(f"{width}x{height}+{width_resolution}+{height_resolution}")
        self.maximize = self.root.resizable(False,False)

        # Set a frame at the background.
        self.frame = ctk.CTkFrame(self.root, height=500, width=350, fg_color=colors["soft_grey"])
        self.frame.pack(pady=10, padx=10, fill="both")

      
        RelaxApp_Initial_Frame(self.frame)

    # Method that creates a new root everytime the main root is destroyed.
    def close_create(self, new_window, *args):
        for wid in self.frame.winfo_children():
            wid.destroy()

        app = new_window(self.frame)



class RelaxApp_Initial_Frame():

    def __init__(self, frame):

        self.frame = frame

    # Login button.
        self.button_start = ctk.CTkButton(self.frame, text="Entrar", font=(font,20), command= self.sign_in,
                                          corner_radius=90, width=100, height=20, hover=True, fg_color=colors["soft_green"], 
                                          hover_color=colors["dark_green"])
        self.button_start.place(rely=0.32, relx=0.5, anchor="center")

    # Method to log in.
    def sign_in(self):
        RelaxApp_Structure.close_create(self, RelaxApp_User_Main_Menu)
        


class RelaxApp_User_Main_Menu():

    def __init__(self, frame):

        self.frame = frame

        self.button_start = ctk.CTkButton(self.frame, text="Volver", font=(font,20), command= self.back,
                                          hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.button_start.place(rely=0.32, relx=0.5, anchor="center")

    # Method to log in.
    def back(self):
        RelaxApp_Structure.close_create(self, RelaxApp_Initial_Frame)


############################################

root = ctk.CTk()
app = RelaxApp_Structure(root)
root.mainloop()
