import tkinter as tk
import customtkinter as ctk
import Database.database as db
from Database.presets_values import user, databases, tables
import ctypes
import time
import threading
import pygame
from PIL import Image
from tktooltip import ToolTip
import datetime
import os
from utils import get_resource_path
import webbrowser

# Connect to the database.
database = db.Database(**db.root_access)

# Get the windows resolution regardless of rescaling
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

# Get the parent folder path and the image folder path.
main_path = get_resource_path("Interface")

# First letter is changed to upper.
main_path_edited = main_path.replace(main_path[0], main_path[0].upper(), 1)

image_path = os.path.join(main_path_edited, "Images")
sounds_path = os.path.join(main_path_edited, "Sounds")

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

# Set all valid audio extension.
audio_accepted_files = (("Audio Files", "*.mp3"),("Audio Files", "*.ogg"), ("Audio Files", "*.wav"),
                        ("Audio Files", "*.m4a"), ("Audio Files", "*.wma"), ("Audio Files", "*.flac"))

#######################################################
### Class that contains general settings of the App ###
#######################################################

class RelaxApp_Structure:
    """This class defines the general structure of the app.
       Defines the dimensions, title and creates a frame."""

    def __init__(self, root):
        
        self.root = root

        # Set the width, height, configuration and location of the windows.
        width = 350
        height = 500
        width_resolution = self.root.winfo_screenwidth() // 2 - width // 2 - width // 3
        height_resolution = self.root.winfo_screenheight() // 2 - height
        self.dimentions = self.root.geometry(f"{width}x{height}+{width_resolution}+{height_resolution}")
        self.maximize = self.root.resizable(False,False)

        # The main frame is created.
        self.general_frame = ctk.CTkFrame(self.root, height=485, width=336, fg_color=colors["soft_grey"],
                                          corner_radius=10)
        self.general_frame.place(rely=0.015, relx=0.02)

        # Set the title and the logo of the app.
        self.title = self.root.title("RelaxApp")
        self.root.after(200, lambda: self.root.iconbitmap(os.path.join(image_path, "logo.ico")))
        
        # The main menu is run.
        RelaxApp_Initial_Frame(self.root, self.general_frame)

    # Method that creates a new root everytime the main root is destroyed. Widget are removed from the screen.
    def close_create(self, new_window, root, clean_frame, *args):
        self.root = root
        # All widget are remove from the frame.
        for wid in clean_frame.winfo_children():
            wid.destroy()
        # New class is run.
        app = new_window(self.root, clean_frame)

    # Method that, besides to create a new root everytime the main root is destroyed, creates the main frame again.
    def close_create2(self, new_window, root, clean_frame, *args):
        self.root = root
        for wid in clean_frame.winfo_children():
            wid.destroy()

        self.general_frame = ctk.CTkFrame(clean_frame, height=485, width=336, fg_color=colors["soft_grey"],
                                          corner_radius=10)
        self.general_frame.place(rely=0.0, relx=0.0)

        app = new_window(self.root, self.general_frame, *args)

    # Method that remove widget from the main menu profile.
    def clean_MMP_widgets(self, clean_MMP_frame):
        for element in clean_MMP_frame:
            for wid in element.winfo_children():
                wid.destroy()
        return clean_MMP_frame
    
    # Method that hide the root to keep it once turning back from the app run.
    def hide_unhide_window(self, root):
        self.root = root
        self.root.withdraw()


###########################################################
### Class that contains general settings of the Pop-ups ###
###########################################################

class RelaxApp_MessageBox_Structure:
    """This class defines the general structure of the pop-ups.
       Defines the dimensions, title and creates a frame."""

    def __init__(self):

        # New pop-ups is created.
        self.window_MS = ctk.CTkToplevel()
        self.window_MS.grab_set()

        # Set the width, height, configuration and location of the windows.
        width = 550
        height = 150
        width_resolution = self.window_MS.winfo_screenwidth() // 2 - width // 2 - width // 3
        height_resolution = self.window_MS.winfo_screenheight() // 2 - height
        self.dimensions = self.window_MS.geometry(f"{width}x{height}+{width_resolution}+{height_resolution}")
        self.maximize = self.window_MS.resizable(False,False)

        # Set a frame at the background.
        self.frame_MS = ctk.CTkFrame(self.window_MS, height=200, width=550, fg_color=colors["soft_grey"])
        self.frame_MS.pack(pady=10, padx=10, fill="both")
        
        # Set the title and the logo of the app.
        self.title = self.window_MS.title("RelaxApp")
        self.window_MS.after(200, lambda: self.window_MS.iconbitmap(os.path.join(image_path, "logo.ico")))

    # Method that remove widget from the main menu profile.
    def clean_MB_widgets(self, clean_MB_frame):
        counter = 1
        for wid in clean_MB_frame.winfo_children():
            if counter != 1:
                wid.destroy()
            counter += 1


####################################################################
### Class that contains general settings of the user's main menu ###
####################################################################

class RelaxApp_User_Settings_Structure:
    """This class defines the general structure of the user's main 
       menu settings. Defines the appearance, dimensions and title."""

    def __init__(self):

        # New pop-ups is created.
        self.window_User_SS = ctk.CTkToplevel()
        self.window_User_SS.grab_set()

        # Set the width, height, configuration and location of the windows.
        width = 260
        height = 300
        width_resolution = self.window_User_SS.winfo_screenwidth() // 2 - width // 2 - width // 3
        height_resolution = self.window_User_SS.winfo_screenheight() // 2 - height
        self.dimensions = self.window_User_SS.geometry(f"{width}x{height}+{width_resolution}+{height_resolution}")
        self.maximize = self.window_User_SS.resizable(False,False)

        # Set a frame at the background.
        self.frame_User_SS = ctk.CTkFrame(self.window_User_SS, height=300, width=260, fg_color=colors["soft_grey"])
        self.frame_User_SS.pack(pady=10, padx=10, fill="both")

        # Set the title and the logo of the app.
        self.title = self.window_User_SS.title("RelaxApp")
        self.window_User_SS.after(200, lambda: self.window_User_SS.iconbitmap(os.path.join(image_path, "logo.ico")))

    # Method that creates a new root everytime the main root is destroyed.
    def close_create_profiles(self, new_window, root, clean_frame, *args):
        self.root = root
        for wid in clean_frame.winfo_children():
            wid.destroy()
        app = new_window(self.root, clean_frame)

######################################################################
### Class that contains general settings while RelaxApp is running ###
######################################################################

class RelaxApp_Running_Structure:
    """This class defines the general structure while app is running. 
       Defines the appearance, dimensions and title."""

    def __init__(self):

        # New pop-ups is created.
        self.window_RS = ctk.CTkToplevel()
        self.window_RS.grab_set()

        # Set the width, height, configuration and location of the windows.
        width = 280
        height = 400
        width_resolution = self.window_RS.winfo_screenwidth() // 2 - width // 2 - width // 3
        height_resolution = self.window_RS.winfo_screenheight() // 2 - height
        self.dimensions = self.window_RS.geometry(f"{width}x{height}+{width_resolution}+{height_resolution}")
        self.maximize = self.window_RS.resizable(False,False)

        # Set a frame at the background.
        self.frame_RS = ctk.CTkFrame(self.window_RS, height=400, width=280, fg_color=colors["soft_grey"])
        self.frame_RS.pack(pady=10, padx=10, fill="both") 

        # Set the title and the logo of the app.
        self.title = self.window_RS.title("RelaxApp")
        self.window_RS.after(200, lambda: self.window_RS.iconbitmap(os.path.join(image_path, "logo.ico")))


############################################################################
### Class that contains general settings while Profile's menu is running ###
############################################################################

class RelaxApp_Profile_Name_Structure:
    """This class defines the general structure while profile name is 
       requested. Defines the appearance, dimensions and title."""

    def __init__(self, root):
        self.root = root

        # New pop-ups is created.
        self.window_PFS = ctk.CTkToplevel()
        self.window_PFS.grab_set()

        # Set the width, height, configuration and location of the windows.
        width = 310
        height = 50
        width_resolution = self.window_PFS.winfo_screenwidth() // 2 - width // 2 - width // 3
        height_resolution = self.window_PFS.winfo_screenheight() // 2 - height - 45
        self.dimensions = self.window_PFS.geometry(f"{width}x{height}+{width_resolution}+{height_resolution}")
        self.maximize = self.window_PFS.resizable(False,False)

        # Set a frame at the background.
        self.frame_PFS = ctk.CTkFrame(self.window_PFS, height=100, width=310, fg_color=colors["soft_grey"])
        self.frame_PFS.pack(pady=10, padx=10, fill="both")

        # Set the title and the logo of the app.
        self.title = self.window_PFS.title("RelaxApp")
        self.window_PFS.after(200, lambda: self.window_PFS.iconbitmap(os.path.join(image_path, "logo.ico")))


#############################################################
### Class that contains general functions to set RelaxApp ###
#############################################################

class Check_Values_Configuration():
    """This class contains only functions which are used to
       verify profiles imported and settings made by the user."""
    
    # This method checks if the lenght of the profile name is shorter than 1 or larger than 20 characters.
    def check_profile_lenght(self, value):
        if len(value) > 20 or len(value) == 0:
            return False
   
    # This method checks if the profile name is duplicated.
    def check_profile_duplicated(self, profile):
        database.query(f"SELECT Profile_Name FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}' and Profile_Name = '{profile}'")
        profile_name = database.value
        if profile_name != []:
            return True

    # This method checks if all values set by the user are correct.
    def check_settings(self, value):

        if value == "":
            return None, None
        
        if value != "":
            try:
                lenght_HH = value[:2]
                lenght_MM = value[2:4]
                lapse = value[4:6]
                break_time_MM = value[6:8]
                break_time_SS = value[8:10]
                sound = value[10:]
            except:
                # print("Archivo corrupto texto")
                return False, False
            
            valid_numbers = [str(x).zfill(2) for x in range(61)]

            if lenght_HH not in valid_numbers or lenght_MM not in valid_numbers or \
            lapse not in valid_numbers or break_time_MM not in valid_numbers or \
            break_time_SS not in valid_numbers:
                # print("Archivo corrupto invalid numbers")
                return False, "Invalid Time"
            
            elif int(lenght_HH) * 60 + int(lenght_MM) > 960:
                # print("Archivo corrupto extra hours")
                return False, "Extra Hours"
            
            elif int(lenght_HH) * 60 + int(lenght_MM) < 1:
                # print("Archivo corrupto minimum time")
                return False, "Minimum Time"
            
            elif int(lapse) > int(lenght_HH) * 60 + int(lenght_MM):
                # print("Archivo corrupto over duration")
                return False, "Over Duration"
            
            elif int(break_time_MM) * 60 + int(break_time_SS) > \
            int(lapse) * 60:
                # print("Archivo corrupto over lapse")
                return False, "Over Lapse"
            
            elif int(lapse) == 0:
                # print("Archivo corrupto no lapse")
                return False, "No Lapse"
            
            elif int(break_time_MM) == 0 and int(break_time_SS) < 30:
                # print("Archivo corrupto no break")
                return False, "No Break"
            
            elif sound != "True" and sound != "False":
                # print("Archivo corrupto sound")
                return False, False
            else:
                return True, "Valid Profile"

    # This method checks if all sound values set by the user are correct.
    def check_sounds_settings(self, value):
        if value == "":
            return None
        sound_path = os.path.isfile(value)
        extension_sound_path = os.path.splitext(value)

        if sound_path == False:
            # print(f"comprobar ruta: {sound_path}")
            # print("ruta: ", value)
            return False

        extension = False
        for values in audio_accepted_files:
            if extension_sound_path[1] in values[1]:
                extension = True
                break

        if extension == False:
            # print("Ruta correcta. Error extension: ", extension)
            return False

        return True


###############################################################################
### Class that is used to validate entries in the user's main menu settings ###
###############################################################################

class Validate_CMD:
    """This class is used to validate the user's personal settings entries
       in the main menu."""
    
    # Funtions to validate lenght of the hours entries.
    def validate_hours(text):
        if len(text) == 0:
            return True
        elif text == "HH":
            return True           
        elif len(text) < 3 and text.isdigit():
            return True
        else:
            return False
    
    # Funtions to validate lenght of the minutes and seconds entries.
    def validate_min_sec(text):
        if len(text) == 0:
            return True
        elif text == "MM" or text == "SS":
            return True
        elif len(text) < 3 and text.isdigit():
            return True
        else:
            return False
    
    # Funtions to validate lenght of the profile name not to be larger than 20 characters.
    def validate_lenght_name(text):
        if len(text) == 0:
            return True
        elif text == "Nombre del Perfil":
            return True
        elif len(text) < 21:
            return True
        else:
            return False
        

######################################################
### Class that contains the first frame of the App ###
######################################################

class RelaxApp_Initial_Frame():
    """This class defines all buttons and options availables into
       the first frame."""

    def __init__(self, root, frame):
        self.root = root
        self.frame = frame

        # User label.
        self.user = ctk.CTkLabel(self.frame, text="Usuario", font=(font,19))
        self.user.place(rely=0.40, relx=0.5, anchor="center")

        # User entry.
        self.entry_user = ctk.CTkEntry(self.frame,font=(font,15), corner_radius=10)
        self.entry_user.place(rely=0.47, relx=0.5, anchor="center")
        self.entry_user.insert(0, "Ej: Usuario")
        self.entry_user.bind("<Button-1>", lambda remove: self.entry_user.delete(0, tk.END))

        # Password label.
        self.password = ctk.CTkLabel(self.frame, text="Contraseña", font=(font,19))
        self.password.place(rely=0.54, relx=0.5, anchor="center")

        # Password entry.
        self.entry_password = ctk.CTkEntry(self.frame,font=(font,15), corner_radius=10, show="*")
        self.entry_password.place(rely=0.61, relx=0.5, anchor="center",)
        self.entry_password.insert(0, "**********")
        self.entry_password.bind("<Button-1>", lambda remove: self.entry_password.delete(0, tk.END))

        # Login button.
        self.button_start = ctk.CTkButton(self.frame, text="Entrar", font=(font,20), command= self.sign_in,
                                          corner_radius=90, width=100, height=20, hover=True, fg_color=colors["soft_green"], 
                                          hover_color=colors["dark_green"])
        self.button_start.place(rely=0.72, relx=0.5, anchor="center")

        # "Register User" button.
        self.button_new_user = ctk.CTkButton(self.frame, width=10, height=10, text="Registrar Usuario", font=(font,12), 
                                             command=self.sign_up, corner_radius=10, hover=True, fg_color=colors["soft_grey"], 
                                             hover_color=colors["dark_green"])
        self.button_new_user.place(rely=0.9, relx=0.04)

        # "Forget password" button.
        self.button_forget_pw = ctk.CTkButton(self.frame, width=10, height=10, text="Olvidé contraseña", font=(font,12), 
                                              command=self.change_password, corner_radius=10, hover=True, fg_color=colors["soft_grey"], 
                                              hover_color=colors["dark_green"])
        self.button_forget_pw.place(rely=0.9, relx=0.6)

    # Method to log in.
    def sign_in(self):
        get_login = self.entry_user.get()
        get_password = self.entry_password.get()
        user["login"] = get_login
        user["password"] = get_password
        database.verify_login(databases["database1"], tables["users_table"], user)
        
        if database.valid_login:
            waiting_logging = ctk.CTkLabel(self.frame, text="Iniciando Sesión...", font=(font,12))
            waiting_logging.place(rely=0.81, relx=0.5, anchor="center")
            self.frame.update_idletasks()
            database.user_configuration(databases["database1"], tables["settings_table"], user["login"], 
                                        "Restore")
            RelaxApp_Structure.close_create(self, RelaxApp_User_Main_Menu, self.root, self.frame)

        else:
            self.error_login = ctk.CTkLabel(self.frame, text="Usuario o contraseña incorrecta. Vuelva a intentarlo.", 
                                            font=(font,11))
            self.error_login.place(rely=0.81, relx=0.5, anchor="center")
   
    # Method that register users.
    def sign_up(self):
        RelaxApp_Structure.close_create(self, RelaxApp_User_Registration, self.root, self.frame)

    # Method to change password.
    def change_password(self):
        RelaxApp_Structure.close_create(self, RelaxApp_User_Change_Password, self.root, self.frame)
   

###############################################################
###  Class that contains the window for users registrations ###
###############################################################

class RelaxApp_User_Registration():
    """This class opens a new window for users registrations."""

    def __init__(self, root, frame):
        self.root = root
        self.frame = frame
        
        # Top bar of the register menu.
        self.top_bar = ctk.CTkLabel(self.frame, text=None, fg_color=colors["dark_green"], width=310, height=0, 
                                    corner_radius=10)
        self.top_bar.place(rely=0.02, relx=0.03)

        # Bottom bar of the register menu.
        self.bottom_bar = ctk.CTkLabel(self.frame, text=None, fg_color=colors["dark_green"], width=310, height=0, 
                                       corner_radius=10)
        self.bottom_bar.place(rely=0.95, relx=0.03)

        # Label of the register menu.
        self.top_text = ctk.CTkLabel(self.frame, text="Complete todos los campos indicados:", font=(font,14))
        self.top_text.place(rely=0.08, relx=0.03)

        # Label to register the name.
        self.name = ctk.CTkLabel(self.frame, text="Nombre:", font=(font,14))
        self.name.place(rely=0.2, relx=0.03)
       
        # Name entry.
        self.name_entry = ctk.CTkEntry(self.frame, font=(font,14), width=180, height=10, corner_radius=10)
        self.name_entry.place(rely=0.2, relx=0.42)
        self.name_entry.bind("<Button-1>", lambda remove: self.name_entry.delete(0, tk.END))

        # Label to register the last name.
        self.last_name = ctk.CTkLabel(self.frame, text="Apellido:", font=(font,14))
        self.last_name.place(rely=0.3, relx=0.03)
        
        # Last name entry.
        self.last_name_entry = ctk.CTkEntry(self.frame, font=(font,14), width=180, height=10, corner_radius=10)
        self.last_name_entry.place(rely=0.3, relx=0.42)
        self.last_name_entry.bind("<Button-1>", lambda remove: self.last_name_entry.delete(0, tk.END))

        # Label to register the username.
        self.username = ctk.CTkLabel(self.frame, text="Nombre Usuario:", font=(font,14))
        self.username.place(rely=0.4, relx=0.03)
        
        # Username entry.
        self.username_entry = ctk.CTkEntry(self.frame, font=(font,14), width=180, height=10, corner_radius=10)
        self.username_entry.place(rely=0.4, relx=0.42)
        self.username_entry.bind("<Button-1>", lambda remove: self.username_entry.delete(0, tk.END))

        # Label to register the password.
        self.password = ctk.CTkLabel(self.frame, text="Contraseña:", font=(font,14))
        self.password.place(rely=0.5, relx=0.03)
        
        # Password entry.
        self.password_entry = ctk.CTkEntry(self.frame, font=(font,14), width=180, height=10, corner_radius=10, 
                                           show="*")
        self.password_entry.place(rely=0.5, relx=0.42)
        self.password_entry.bind("<Button-1>", lambda remove: self.password_entry.delete(0, tk.END))

        # Button to accept the user registration.
        self.create_button = ctk.CTkButton(self.frame, text="Dar de Alta", font=(font,14), command= self.accept_sign_up,
                                           corner_radius=90, width=100, height=20, hover=True, fg_color=colors["soft_green"], 
                                           hover_color="#0a4e50")
        self.create_button.place(rely=0.7, relx=0.5, anchor="center")

        # Button to cancel the user registration.
        self.cancel_button = ctk.CTkButton(self.frame, text="Cancelar", font=(font,14), command= self.cancel_sign_up,
                                           corner_radius=90, width=100, height=20, hover=True, fg_color=colors["soft_green"], 
                                           hover_color=colors["dark_green"])
        self.cancel_button.place(rely=0.8, relx=0.5, anchor="center")

    # This method gets the values registered and call the class to check them          
    def accept_sign_up(self):
        get_name = self.name_entry.get()
        get_last_name = self.last_name_entry.get()
        get_username = self.username_entry.get()
        get_password = self.password_entry.get()

        user["action"] = "sign_up"
        user["name"] = get_name
        user["lastname"] = get_last_name
        user["login"] = get_username
        user["password"] = get_password

        RelaxApp_MessageBox_Options(self.root, self.frame, "Sign up", user)

    # This method cancel the user registration and turns back to the main menu.
    def cancel_sign_up (self):
        RelaxApp_MessageBox_Options(self.root, self.frame, "Cancel", user)


##############################################################
###  Class that contains the window to change the password ###
##############################################################

class RelaxApp_User_Change_Password():
    """This class opens a new window to change the pasword."""

    def __init__(self, root, frame):
        self.root = root
        self.frame = frame
        
        # Top bar of the change password menu.
        self.top_bar = ctk.CTkLabel(self.frame, text=None, fg_color=colors["dark_green"], width=310, height=0, 
                                    corner_radius=10)
        self.top_bar.place(rely=0.02, relx=0.03)

        # Bottom bar of the change password menu.
        self.bottom_bar = ctk.CTkLabel(self.frame, text=None, fg_color=colors["dark_green"], width=310, height=0, 
                                       corner_radius=10)
        self.bottom_bar.place(rely=0.95, relx=0.03)

        # Label of the change password menu.
        self.top_text = ctk.CTkLabel(self.frame, text="Complete todos los campos indicados:", font=(font,14))
        self.top_text.place(rely=0.08, relx=0.03)

        # Label to set the username.
        self.name = ctk.CTkLabel(self.frame, text="Nombre Usuario:", font=(font,14))
        self.name.place(rely=0.2, relx=0.03)
       
        # Username entry.
        self.name_entry = ctk.CTkEntry(self.frame, font=(font,14), width=165, height=10, corner_radius=10)
        self.name_entry.place(rely=0.2, relx=0.47)
        self.name_entry.bind("<Button-1>", lambda remove: self.name_entry.delete(0, tk.END))
       
        # Label to set the new password.
        self.pw1 = ctk.CTkLabel(self.frame, text="Nueva Contraseña:", font=(font,14))
        self.pw1.place(rely=0.3, relx=0.03)
        
        # Password entry 1.
        self.pw1_entry = ctk.CTkEntry(self.frame, font=(font,14), width=165, height=10, corner_radius=10, 
                                      show="*")
        self.pw1_entry.place(rely=0.3, relx=0.47)
        self.pw1_entry.bind("<Button-1>", lambda remove: self.pw1_entry.delete(0, tk.END))

        # Label to confirm the new password.
        self.pw2 = ctk.CTkLabel(self.frame, text="Repetir Contraseña:", font=(font,14))
        self.pw2.place(rely=0.4, relx=0.03)
        
        # Password entry 2.
        self.pw2_entry = ctk.CTkEntry(self.frame, font=(font,14), width=165, height=10, corner_radius=10, 
                                      show="*")
        self.pw2_entry.place(rely=0.4, relx=0.47)
        self.pw2_entry.bind("<Button-1>", lambda remove: self.pw2_entry.delete(0, tk.END))
        
        # Button to confirm to change the password.
        self.change_pw_button = ctk.CTkButton(self.frame, text="Cambiar Contraseña", font=(font,14), command= self.accept_change_pw,
                                              corner_radius=90, width=100, height=20, hover=True, fg_color=colors["soft_green"], 
                                              hover_color=colors["dark_green"])
        self.change_pw_button.place(rely=0.55, relx=0.5, anchor="center")

        # Button to cancel to change the password.
        self.cancel_change_pw_button = ctk.CTkButton(self.frame, text="Cancelar", font=(font,14), command= self.cancel_change_pw,
                                                     corner_radius=90, width=100, height=20, hover=True, fg_color=colors["soft_green"], 
                                                     hover_color=colors["dark_green"])
        self.cancel_change_pw_button.place(rely=0.65, relx=0.5, anchor="center")

    # This method gets the values registered and call the class to check them.
    def accept_change_pw(self):

        # Variable to compare password 1 with password 2.
        self.confirm_pw = False

        get_username_pw_menu = self.name_entry.get()
        get_password1_pw_menu = self.pw1_entry.get()
        get_password2_pw_menu = self.pw2_entry.get()

        user["action"] = "modify"
        user["login"] = get_username_pw_menu
        user["password"] = get_password1_pw_menu

        if user["password"] == get_password2_pw_menu:
            self.confirm_pw = True
            RelaxApp_MessageBox_Options(self.root, self.frame, "Password Correct", user)
        else:
            RelaxApp_MessageBox_Options(self.root, self.frame, "Password Incorrect", user)

    # This method cancel the user registration and turns back to the main menu.
    def cancel_change_pw (self):
        RelaxApp_MessageBox_Options(self.root, self.frame, "Cancel Change PW", user)


#########################################################
###  Class that contains the user's main menu window  ###
#########################################################

class RelaxApp_User_Main_Menu():
    """This class contains the user's main menu. It allows to start
       the app, set, save and load settings and knows about RelaxApp."""

    def __init__(self, root, frame, visual_set=False, stretch_set=False, value=False):
        
        self.root = root
        self.frame = frame

        self.visual_set = visual_set
        self.stretch_set = stretch_set
        self.value_test = value

        # Frame at the back.
        self.frame.configure(fg_color=colors["black"])

        # Frame at the top that contains menu options.
        self.frame_top_menu = ctk.CTkFrame(self.frame, height=30, width=340, fg_color=colors["soft_grey"], 
                                           corner_radius=3)
        self.frame_top_menu.place(rely=0.0)

        # Main frame that contains all user options.
        self.frame_main = ctk.CTkFrame(self.frame, height=450, width=336, fg_color=colors["soft_grey"],
                                       corner_radius=10)
        self.frame_main.place(rely=0.07)

        # Archieve button menu.
        self.archieve_menu_button = tk.Menubutton(self.frame_top_menu, text="Archivo", font=(font,9), width=5, 
                                                  height=2, background=colors["soft_grey"], foreground=colors["white"], 
                                                  activebackground=colors["dark_green"], activeforeground=colors["white"])
        self.archieve_menu_button.place(rely=0.5, relx=0, anchor="w")

        # Help button menu.
        self.help_button = tk.Menubutton(self.frame_top_menu, text="Ayuda", font=(font,9), width=4, 
                                         height=2, background=colors["soft_grey"], foreground=colors["white"], 
                                         activebackground=colors["dark_green"], activeforeground=colors["white"])
        self.help_button.place(rely=0.5, relx=0.18, anchor="w")

        # Profile button menu.
        self.profile_button = tk.Menubutton(self.frame_top_menu, text="Cuenta", font=(font,9), width=4, 
                                            height=2, background=colors["soft_grey"], foreground=colors["white"], 
                                            activebackground=colors["dark_green"], activeforeground=colors["white"])
        self.profile_button.place(rely=0.5, relx=0.34, anchor="w")
        
        # Sign out button menu.
        self.sign_out_button = ctk.CTkButton(self.frame_top_menu, width=10, height=50, text="Cerrar Sesión", 
                                             font=(font,12), command=self.sign_out, hover=True, fg_color=colors["soft_grey"], 
                                             hover_color=colors["dark_green"])
        self.sign_out_button.place(rely=0.5, relx=1, anchor="e")

        # Archieve menu cascade.
        self.menu_archieve = tk.Menu(self.archieve_menu_button, tearoff=0)
        self.archieve_menu_button.config(menu=self.menu_archieve)

        # Help menu cascade.
        self.menu_help = tk.Menu(self.help_button, tearoff=0)
        self.help_button.config(menu=self.menu_help)

        # Profile menu cascade.
        self.menu_profile = tk.Menu(self.profile_button, tearoff=0)
        self.profile_button.config(menu=self.menu_profile)

        # Labels of archieve menu cascade.
        self.menu_archieve.add_command(label=" Importar Perfil  ", font=(font,9), command=self.import_profile, 
                                       background=colors["soft_grey"], foreground=colors["white"], activebackground=colors["dark_green"], 
                                       hidemargin=True)
        self.menu_archieve.add_command(label=" Exportar Perfil  ", font=(font,9), command=self.export_profile, 
                                       background=colors["soft_grey"], foreground=colors["white"], activebackground=colors["dark_green"], 
                                       hidemargin=True)
        
        # Label of help menu cascade.
        self.menu_help.add_command(label=" Conozca RelaxApp  ", font=(font,9), command=self.about_us, background=colors["soft_grey"], 
                                   foreground=colors["white"], activebackground=colors["dark_green"], hidemargin=True) 

        # Label of profile menu cascade.
        self.menu_profile.add_command(label=" Eliminar Cuenta  ", font=(font,9), command=self.remove_account, background=colors["soft_grey"], 
                                      foreground=colors["white"], activebackground=colors["dark_green"], hidemargin=True) 

        # Options label.
        self.options = ctk.CTkLabel(self.frame_main, text="Configurar", font=(font, 16), corner_radius=10, height=35)
        self.options.place(rely=0.2, relx=0.5, anchor="center")

        database.query(f"SELECT Profile_Name FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}'")
        len_profiles = database.value

        # Profile button is set as active or deactive when a profile exists.
        if len(len_profiles) > 1 or self.value_test == True:
            self.profile_state = "normal"
        else:
            self.profile_state = ctk.DISABLED   
            
        # Button to create profiles.
        self.profile_options = ctk.CTkButton(self.frame_main, text="Perfiles", font=(font, 14), 
                                             command=self.create_profile, corner_radius=10, height=35, 
                                             hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"],
                                             state=self.profile_state)
        self.profile_options.place(rely=0.3, relx=0.25, anchor="w")

        # Variable to save the information of "profile_options_CB" when is marked or unmarked.
        self.profile_options_choice = ctk.IntVar()

        # Checkbox to activate or deactivate "profile_options".
        self.profile_options_CB = ctk.CTkCheckBox(self.frame_main, text=None, variable=self.profile_options_choice , width=20, height=20, hover=True, 
                                                  command=self.checkbox_option1, state=self.profile_state,
                                                  fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.profile_options_CB.place(rely=0.3, relx=0.8, anchor="e")

        # Button to set visual options.
        self.visual_options = ctk.CTkButton(self.frame_main, text="Descanso Visual", font=(font, 14), 
                                            command=self.set_visual_options, corner_radius=10, height=35, 
                                            hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.visual_options.place(rely=0.4, relx=0.25, anchor="w")

        # Variable to save the information of "visual_options_CB" when is marked or unmarked.
        self.visual_options_choice = ctk.IntVar()

        # Checkbox to activate or deactivate "visual_options".
        self.visual_options_CB = ctk.CTkCheckBox(self.frame_main, text=None, variable=self.visual_options_choice , width=20, height=20, hover=True, 
                                                 command=self.checkbox_option2, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.visual_options_CB.place(rely=0.4, relx=0.8, anchor="e")

        # Image of a restart simbol.
        self.restart_button = ctk.CTkImage(Image.open(os.path.join(image_path, "Restart.png")))
        

        # Button to restart VO values set.
        self.restart_button1 = ctk.CTkButton(self.frame_main, text=None, image=self.restart_button, width=20, height=20, hover=True,
                                             command=lambda: self.restart_values("VO"), fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.restart_button1.place(rely=0.4, relx=0.9, anchor="e")

        # Button to set stretch options.
        self.stretch_options = ctk.CTkButton(self.frame_main, text="Estirar", font=(font, 14), 
                                             command=self.set_stretch_options, corner_radius=10, height=35, 
                                             hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.stretch_options.place(rely=0.5, relx=0.25, anchor="w")

        # Variable to save the information of "stretch_options_CB" when is marked or unmarked.
        self.stretch_options_choice = ctk.IntVar()

        # Checkbox to activate or deactivate "stretch_options".
        self.stretch_options_CB = ctk.CTkCheckBox(self.frame_main, text=None, variable=self.stretch_options_choice, width=20, height=20, hover=True, 
                                                  command=self.checkbox_option3,
                                                  fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.stretch_options_CB.place(rely=0.5, relx=0.8, anchor="e")

        # Button to restart SO values set.
        self.restart_button2 = ctk.CTkButton(self.frame_main, text=None, image=self.restart_button, width=20, height=20, hover=True,
                                             command=lambda: self.restart_values("SO"), fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.restart_button2.place(rely=0.5, relx=0.9, anchor="e")

        # Button to set sounds options.
        self.sounds_options = ctk.CTkButton(self.frame_main, text="Sonidos", font=(font, 14), 
                                            command=self.set_sounds_options, corner_radius=10, height=35, 
                                            hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.sounds_options.place(rely=0.6, relx=0.25, anchor="w")

        # Button to set start RelaxApp.
        self.start_relaxapp_button = ctk.CTkButton(self.frame_main, text="Iniciar", font=(font, 20), 
                                                   command=self.start_relaxapp, height=70, corner_radius=50, 
                                                   hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.start_relaxapp_button.place(rely=0.8, relx=0.5, anchor="center")

    # Next 3 functions unmark values when user choose between use a profile or not. 
    def checkbox_option1(self):
        self.visual_options_choice.set(0)
        self.stretch_options_choice.set(0)
        
    def checkbox_option2(self):
        self.profile_options_choice.set(0)
        
    def checkbox_option3(self):
        self.profile_options_choice.set(0)

    # This method creates profiles.
    def create_profile(self):
        RelaxApp_User_Main_Menu_Profiles(user["login"])
    
    # This method import profiles.
    def import_profile(self):
        try:
            import_file = ctk.filedialog.askopenfilename(title="Importar Perfil")

            with open(import_file, mode="r", encoding="utf-8") as file:
                read_file = file.readlines()
                self.corrupt_file = False
                file_values = []

                # Bucle that add values in a list to check them easily.
                for value in read_file:
                    file_values.append(value[:-1])
                
                while self.corrupt_file == False:
                    # Lenght of the profile name is checked.
                    check_profile = Check_Values_Configuration.check_profile_lenght(self, file_values[0])
                    if check_profile == False:
                        self.corrupt_file = True

                    # Name of the profile is checked to avoid duplicated name.
                    check_profile_duplicated = Check_Values_Configuration.check_profile_duplicated(self, file_values[0])
                    if check_profile_duplicated == True:
                        self.corrupt_file = True

                    # Settings of the profile values are checked.
                    check_settings_1 = Check_Values_Configuration.check_settings(self, file_values[1])
                    check_settings_2 = Check_Values_Configuration.check_settings(self, file_values[2])

                    if check_settings_1[0] == False or check_settings_2[0] == False:
                        self.corrupt_file = True

                    if file_values[1] == "" and file_values[2] == "":
                        self.corrupt_file = True

                    check_sounds_settings_1 = Check_Values_Configuration.check_sounds_settings(self, file_values[3])
                    check_sounds_settings_2 = Check_Values_Configuration.check_sounds_settings(self, file_values[4])

                    if check_sounds_settings_1 == False or check_sounds_settings_2 == False:
                        self.corrupt_file = True

                    if check_sounds_settings_1 != check_sounds_settings_2:
                        self.corrupt_file = True
                    break

                if self.corrupt_file == True:
                    return RelaxApp_MessageBox_Options(self.root, self.frame, "File_Corrupt")
                else:
                    RelaxApp_MessageBox_Options(self.root, self.frame, "Valid Profile", None, file_values)

        except FileNotFoundError:
            pass
        except UnicodeDecodeError:
            RelaxApp_MessageBox_Options(self.root, self.frame, "Invalid_Format")
        except:
            RelaxApp_MessageBox_Options(self.root, self.frame, "File_Corrupt")

    # This method saves profiles set.
    def export_profile(self):

        # Query method is called to check or get profiles information.
        database.query(f"SELECT Profile_Name, Default_Profile, Visual_Configuration, Stretch_Configuration, Final_Sounds_Configuration, \
                       Lapse_Sounds_Configuration FROM {databases['database1']}.{tables['settings_table']} WHERE \
                       login = '{user['login']}' and Default_Profile = 'True'")
        
        # Message box is called if there no profile to export.
        if database.value == []:
            RelaxApp_MessageBox_Options(self.root, self.frame, "No Profile")
        else:
            try:
                save_file = ctk.filedialog.asksaveasfilename(title="Exportar Perfil")

                # Bucle to go through each value saved in the profile.
                with open(save_file, mode="w", encoding="utf-8") as file:
                    for line in database.value[0]:
                        if line == "True" or line == "False":
                            pass
                        elif line == "":
                            file.write("\n")
                        else:
                            file.write(line + "\n")
            except:
                pass            

    def about_us(self):
        webbrowser.open("https://github.com/L3chuS/Relaxapp.git")

    # This method removes profiles set.
    def remove_account(self):
        RelaxApp_MessageBox_Options(self.root, self.frame, "Remove Account", user["login"])

    # This method signs out of the App.
    def sign_out(self):
        RelaxApp_MessageBox_Options(self.root, self.frame, "Sign Out", user["login"])

    # This method sets visual options of the App.
    def set_visual_options(self):
        self.visual_options_values = True
        RelaxApp_User_Main_Menu_Settings(self.root, self.frame, self.visual_options_values)

    # This method sets stretch options of the App.
    def set_stretch_options(self):
        self.stretch_options_values = True
        RelaxApp_User_Main_Menu_Settings(self.root, self.frame, None, self.stretch_options_values)

    # This method restarts values set.
    def restart_values(self, value):
        if value == "VO":
            database.user_configuration(databases["database1"], tables["settings_table"], user["login"], "Restart", "Visual_Configuration")
        elif value == "SO":
            database.user_configuration(databases["database1"], tables["settings_table"], user["login"], "Restart", "Stretch_Configuration")      

    # This method sets sound options of the App.
    def set_sounds_options(self):
        RelaxApp_User_Main_Menu_Sounds(self.frame)

    # This method starts the App.
    def start_relaxapp(self):
        self.visual_set = False
        self.stretch_set = False
        self.value_VO = ""
        self.value_SO = ""

        # Get if "self.visual_options_CB" is checked.
        if self.profile_options_choice.get() == 1:
            try:
                database.query(f"SELECT Visual_Configuration FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}' and Default_Profile = 'True'")
                self.value_VO = database.value[0][0]

                database.query(f"SELECT Stretch_Configuration FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}' and Default_Profile = 'True'")
                self.value_SO = database.value[0][0]
                if self.value_VO != "":
                    self.visual_set = True
                if self.value_SO != "":
                    self.stretch_set = True
                if self.value_VO == "" and self.value_SO == "":
                    RelaxApp_MessageBox_Options(self.root, self.frame, "No Values Set")
                    return
                database.query(f"SELECT Final_Sounds_Configuration, Lapse_Sounds_Configuration FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}' and Default_Profile = 'True'")
                self.final_sound = database.value[0][0]
                self.lapse_sound = database.value[0][1]

            except:
                RelaxApp_MessageBox_Options(self.root, self.frame, "No Values Set")
                return

        # Get if "self.visual_options_CB" is checked.
        if self.visual_options_choice.get() == 1:
            self.visual_set = True
            database.query(f"SELECT Visual_Configuration FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}' and Default_Profile is NULL")
            self.value_VO = database.value[0][0]
            
            if self.value_VO == "":
                RelaxApp_MessageBox_Options(self.root, self.frame, "No Values Set")
                return
        
        # Get if "self.stretch_options_CB" is checked.
        if self.stretch_options_choice.get() == 1:
            self.stretch_set = True
            database.query(f"SELECT Stretch_Configuration FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}' and Default_Profile is NULL")
            self.value_SO = database.value[0][0]

            if self.value_SO == "":
                RelaxApp_MessageBox_Options(self.root, self.frame, "No Values Set")
                return

        if self.visual_set == False and self.stretch_set == False:
            RelaxApp_MessageBox_Options(self.root, self.frame, "No Settings")
            return
        
        if self.visual_options_choice.get() == 1 or self.stretch_options_choice.get() == 1:
            database.query(f"SELECT Final_Sounds_Configuration, Lapse_Sounds_Configuration FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}' and Default_Profile is NULL")
            self.final_sound = database.value[0][0]
            self.lapse_sound = database.value[0][1]

        RelaxApp_Structure.hide_unhide_window(self, self.root)
        RelaxApp_Running(self.root, self.frame, self.visual_set, self.stretch_set, self.value_VO, self.value_SO, self.final_sound, self.lapse_sound)


##########################################################
###  Class that contains the user's personal settings  ###
##########################################################

class RelaxApp_User_Main_Menu_Profiles(RelaxApp_User_Settings_Structure):
    """This class opens a new window to set the user's personal profiles 
       of the App. Inherit all structure from parent."""
    
    def __init__(self, user):

        super().__init__()

        # User logged in is gotten.
        self.user = user

        # Frame at the back.
        self.frame_User_SS.configure(fg_color=colors["black"])
        self.frame_User_SS.pack(pady=0, padx=0, fill="both")

        # Frame that contains the tittle of the class.
        self.frame1 = ctk.CTkFrame(self.frame_User_SS, height=50, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame1.pack(pady=10, padx=10)

        # Frame that contains the create and remove buttons.
        self.frame2 = ctk.CTkFrame(self.frame_User_SS, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame2.pack(pady=1, padx=10)

        # Frame that contains the first profile.
        self.frame3 = ctk.CTkFrame(self.frame_User_SS, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame3.pack(pady=1, padx=10)

        # Frame that contains the second profile.
        self.frame4 = ctk.CTkFrame(self.frame_User_SS, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame4.pack(pady=1, padx=10)

        # Frame that contains the third profile.
        self.frame5 = ctk.CTkFrame(self.frame_User_SS, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame5.pack(pady=1, padx=10)

        # Frame that contains the save and cancel buttons.
        self.frame6 = ctk.CTkFrame(self.frame_User_SS, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame6.pack(pady=10, padx=10)

        # Tittle label of the class.
        self.setting_title = ctk.CTkLabel(self.frame1, text="Perfil Predeterminado", font=(font, 15), 
                                        corner_radius=5, fg_color=colors["soft_green"])
        self.setting_title.place(rely=0.5, relx=0.5, anchor="center")

        # Image of a create simbol.
        self.create_button = ctk.CTkImage(Image.open(os.path.join(image_path, "Create.png")))
        # Image of a remove simbol.
        self.remove_button = ctk.CTkImage(Image.open(os.path.join(image_path, "Remove.png")))

        # Button to create new profile.
        self.create_profile_button = ctk.CTkButton(self.frame2, text=None, image=self.create_button, width=0, command=self.create_profile,
                                                hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.create_profile_button.place(rely=0.5, relx=0.3, anchor="center")

        # Button to remove profile selected.
        self.remove_profile_button = ctk.CTkButton(self.frame2, text=None, image=self.remove_button, width=0, command=self.remove_profile,
                                                hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.remove_profile_button.place(rely=0.5, relx=0.7, anchor="center")

        # Save button.
        self.save_button = ctk.CTkButton(self.frame6, width=10, height=10, text="Guardar", font=(font,14), 
                                        command=self.save_settings, corner_radius=10, hover=True, 
                                        fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.save_button.place(rely=0.5, relx=0.1, anchor="w")

        # Cancel button.
        self.cancel_button = ctk.CTkButton(self.frame6, width=10, height=10, text="Cancelar", font=(font,14),
                                        command=self.cancel_settings, corner_radius=10, hover=True, 
                                        fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.cancel_button.place(rely=0.5, relx=0.9, anchor="e")

        # Frames which will be cleaned when creating and removing profiles.
        self.dinamics_frames = (self.frame3, self.frame4, self.frame5)

        # Profile list is gotten to run or not the profile function.
        profile_list = self.get_profile_list()
        # Variable to save the option chosen with the radiobuttons.
        self.get_profile_saved = [self.get_profile_chosen_default()]

        # Profiles are run if there's any.
        if len(profile_list) > 1:
            self.run_profiles(profile_list)

    # This method gets all profiles names of the current user from the database.
    def get_profile_list(self):

        # Search method is called to get all the profile set for current user.
        database.query(f"SELECT Profile_Name FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}'")
        profile_list = database.value
        return profile_list

    # This method gets all default profiles of the current user from the database.
    def get_default_profile(self):

        # Search method is called to get if there's a profile set as default.
        database.query(f"SELECT Default_Profile FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}'")
        default_profile = database.value
        return default_profile

    # This method checks if there's any profile set as default.
    def check_profile_true(self):

        default_profile = RelaxApp_User_Main_Menu_Profiles.get_default_profile(self)
        for profile in default_profile:
            if profile[0] == "True":
                return True

    # This method gets the option chosen by the radio buttons.
    def get_choice(self):

        try:
            # Try to get the option.
            profile_chosen = self.profile_choice.get()
        except:
            # Set an option by default when none is chosen (after a profile is created).
            profile_chosen = 0

        # The value is saved in a list and the last one is removed.
        self.get_profile_saved.append(profile_chosen)
        self.get_profile_saved.remove(self.get_profile_saved[0])
        return self.get_profile_saved

    # This method gets the profile set as default to set the correct option for the radio buttons.
    def get_profile_chosen_default(self):

        default = RelaxApp_User_Main_Menu_Profiles.get_default_profile(self)
        choice_counter = -1
        profile_choice = 0
        # This for function iterates from the profiles to get the one set as "True" and set the correct 
        # option for the radio buttons.
        for value in default:
            if value[0] == "True":
                profile_choice = choice_counter
                break
            choice_counter += 1
        return profile_choice

    # This method set the first profile and set it as default. Is used when none profiles is set as default.
    def set_profile_true(self, profile_list):

        self.profile_choice = ctk.IntVar(value=0)
        # When there's no profile set as "True" database is modified to set the first one as default. 
        database.user_configuration(databases["database1"], tables["settings_table"], user["login"], "Update",
                                            ("Profile_Name", "Default_Profile"), (profile_list[1][0], "True"))

    # This method creates the radio buttons based on the amount of profiles.
    def create_RB_profile(self, profile_list, dinamics_frames, profile_choice=0, *args):

        # Var to work with the radio buttons.
        self.profile_choice = ctk.IntVar(value=profile_choice)

        # Radio button 1 that contains the first profile set.
        profile_set1 = ctk.CTkRadioButton(dinamics_frames[0], text=None, value=0, variable=self.profile_choice, command=lambda:RelaxApp_User_Main_Menu_Profiles.get_choice(self),
                                          hover=True, border_width_unchecked=2, border_width_checked=5, fg_color=colors["soft_green"], 
                                          hover_color=colors["dark_green"])
        profile_set1.place(rely=0.5, relx=0.87, anchor="w")

        # Radio button 2 that contains the second profile set. 
        if len(profile_list) > 2:
            profile_set2 = ctk.CTkRadioButton(dinamics_frames[1], text=None, value=1, variable=self.profile_choice, command=lambda:RelaxApp_User_Main_Menu_Profiles.get_choice(self),
                                              hover=True, border_width_unchecked=2, border_width_checked=5, fg_color=colors["soft_green"], 
                                              hover_color=colors["dark_green"])
            profile_set2.place(rely=0.5, relx=0.87, anchor="w")

        # Radio button 3 that contains the third profile set.
        if len(profile_list) > 3:
            profile_set3 = ctk.CTkRadioButton(dinamics_frames[2], text=None, value=2, variable=self.profile_choice, command=lambda:RelaxApp_User_Main_Menu_Profiles.get_choice(self),
                                              hover=True, border_width_unchecked=2, border_width_checked=5, fg_color=colors["soft_green"], 
                                              hover_color=colors["dark_green"])
            profile_set3.place(rely=0.5, relx=0.87, anchor="w")

    # This method writes all profiles set if there's any.
    def run_profiles(self, profile_list, *args):

        check_profile = RelaxApp_User_Main_Menu_Profiles.check_profile_true(self)
        if check_profile == None:
            profile_choice = RelaxApp_User_Main_Menu_Profiles.set_profile_true(self, profile_list)

        # Variable to be used to write the profile selected in the frame 3, 4 or 5.
        frame_counter = 3
        # Bucle to write each profile on each frame.
        for profile in range(1, len(profile_list)):
            if frame_counter == 3:
                frame = self.dinamics_frames[0]
            elif frame_counter == 4:
                frame = self.dinamics_frames[1]
            elif frame_counter == 5:
                frame = self.dinamics_frames[2]

            profile_set = ctk.CTkLabel(frame, text=profile_list[profile][0], font=(font, 15))
            profile_set.place(rely=0.5, relx=0.02, anchor="w")
            frame_counter += 1

        profile_choice = RelaxApp_User_Main_Menu_Profiles.get_profile_chosen_default(self)

        RelaxApp_User_Main_Menu_Profiles.create_RB_profile(self, profile_list, self.dinamics_frames, profile_choice, self.get_profile_saved)

    # This method creates the profiles.
    def create_profile(self):
        RelaxApp_Profile_Name(self.frame_User_SS, self.window_User_SS, self.dinamics_frames, self.get_profile_saved)

    # This method removes the profile selected.
    def remove_profile(self):

        profile_list = self.get_profile_list()
        if len(profile_list) > 1:
            # The profile selected is chosen. 
            profile_choosen = profile_list[self.get_profile_saved[0]+1][0]
            # Profile is removed from database.
            database.user_configuration(databases["database1"], tables["settings_table"], user["login"], "Remove", ("Login", "Profile_Name"), profile_choosen)

            # Frames 3,5,6 are cleaned where the profiles are located.
            RelaxApp_Structure.clean_MMP_widgets(self, self.dinamics_frames)

            # Profiles are run again after one was removed.
            profile_list = self.get_profile_list()
            if len(profile_list) > 1:
                self.get_profile_saved = [0]
                RelaxApp_User_Main_Menu_Profiles.run_profiles(self, profile_list, self.dinamics_frames, self.get_profile_saved)

    # This method saves the profile/s created and selected as default.
    def save_settings(self):

        profile_list = self.get_profile_list()

        if len(profile_list) > 1:
            profile_selected = self.get_profile_saved
            # This bucle set the profile select as "True" and the rest (if there's any) as "False".
            for profile in range(1, len(profile_list)):
                if profile == profile_selected[0] + 1:
                    database.user_configuration(databases["database1"], tables["settings_table"], user["login"], 
                                                "Update", ("Profile_Name", "Default_Profile"), (profile_list[profile][0], "True"))
                else:
                    database.user_configuration(databases["database1"], tables["settings_table"], user["login"], 
                                                "Update", ("Profile_Name", "Default_Profile"), (profile_list[profile][0], "False"))
        self.window_User_SS.destroy()

    # This method cancel the profile menu and close the window.
    def cancel_settings(self):
        self.window_User_SS.destroy()


##################################################################
###  Class that contains the window to write the profile name  ###
##################################################################

class RelaxApp_Profile_Name(RelaxApp_Profile_Name_Structure):
    """This class opens a new window to set the user's personal profiles
       of the App. Inherit all structure from parent."""
    
    def __init__(self, frame, window, dinamics_frames, variable_saved):
        super().__init__(frame)
        self.frame = frame
        self.window = window
        self.dinamics_frames = dinamics_frames
        self.get_profile_saved = variable_saved

        # Image of an accept simbol.
        self.accept_image = ctk.CTkImage(Image.open(os.path.join(image_path, "Accept.png")))
        # Image of a remove simbol.
        self.close_image = ctk.CTkImage(Image.open(os.path.join(image_path, "Remove.png")))

        # Validate character limit. 
        self.lenght_name = self.root.register(Validate_CMD.validate_lenght_name)

        # Profile name entry.
        self.profile_name_entry = ctk.CTkEntry(self.frame_PFS, font=(font,14), width=200, validate="key",
                                               validatecommand=(self.lenght_name, "%P"))
        self.profile_name_entry.place(rely=0.5, relx=0.01, anchor="w")
        self.profile_name_entry.insert(0, "Nombre del Perfil")
        self.profile_name_entry.bind("<Button-1>", lambda remove: self.profile_name_entry.delete(0, tk.END))

        # Accept button to create a profile.
        self.accept_button = ctk.CTkButton(self.frame_PFS, text=None, image=self.accept_image, width=0, command=self.accept,
                                           hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.accept_button.place(rely=0.5, relx=0.85, anchor="e")

        # Cancel button to not create a profile.
        self.close_button = ctk.CTkButton(self.frame_PFS, text=None, image=self.close_image, width=0, command=self.close,
                                          hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.close_button.place(rely=0.5, relx=0.99, anchor="e")

    # This method check the name given and create or not the new profile.
    def accept(self):
        profile_name = self.profile_name_entry.get()

        profile_list = RelaxApp_User_Main_Menu_Profiles.get_profile_list(self)

        check_profile_duplicated = Check_Values_Configuration.check_profile_duplicated(self, profile_name)

        if len(profile_name) == 0:
            RelaxApp_MessageBox_Options(self.root, self.window, "No Name")
        elif len(profile_list) == 4:
            RelaxApp_MessageBox_Options(self.root, self.window, "Full Profile")
        elif check_profile_duplicated == True:
            RelaxApp_MessageBox_Options(self.root, self.window, "Duplicated")
        else:
            date_time = datetime.datetime.now().strftime("%d-%m-%Y - %H.%M.%Shs")

            # Search method is called to get all the profile set for current user.
            database.query(f"SELECT Visual_Configuration, Stretch_Configuration, Final_Sounds_Configuration, Lapse_Sounds_Configuration FROM \
                           {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}' and Profile_Name is NULL")
            profile_values = database.value
            visual_config = profile_values[0][0]
            stretch_config = profile_values[0][1]
            final_sound_config = profile_values[0][2]
            lapse_sound_config = profile_values[0][3]

            database.user_configuration(databases["database1"], tables["settings_table"], user["login"], 
                                        "Add", "Login, Profile_Name, Date_Time, Default_Profile, Visual_Configuration, \
                                        Stretch_Configuration, Final_Sounds_Configuration, Lapse_Sounds_Configuration", 
                                        (profile_name, date_time, False, visual_config, stretch_config, final_sound_config, lapse_sound_config))
            
            profile_list = RelaxApp_User_Main_Menu_Profiles.get_profile_list(self)

            self.window_PFS.destroy()

            dinamics_frames = RelaxApp_Structure.clean_MMP_widgets(self, self.dinamics_frames)
            RelaxApp_User_Main_Menu_Profiles.run_profiles(self, profile_list, dinamics_frames, self.get_profile_saved)

    # This method cancel the profile name menu and returns to the profile menu.
    def close(self):
        self.window_PFS.destroy()


##########################################################
###  Class that contains the user's personal settings  ###
##########################################################

class RelaxApp_User_Main_Menu_Settings(RelaxApp_User_Settings_Structure):
    """This class opens a new window to set the user's personal settings 
       of the App. Inherit all structure from parent."""
    
    def __init__(self, root, frame, visual_values=None, stretch_values=None):
        super().__init__()
        
        self.root = root
        self.frame = frame

        self.visual_options_values = visual_values
        self.stretch_options_values = stretch_values

        # An empty string which is going to save all values when user save a configuration.
        self.values = ""

        # Frame at the back.
        self.frame_User_SS.configure(fg_color=colors["black"])
        self.frame_User_SS.pack(pady=0, padx=0, fill="both")  

        # Frame that contains the alert configuration label.
        self.frame1 = ctk.CTkFrame(self.frame_User_SS, height=50, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame1.pack(pady=10, padx=10)

        # Frame that contains the lenght configuration label.
        self.frame2 = ctk.CTkFrame(self.frame_User_SS, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame2.pack(pady=1, padx=10)

        # Frame that contains the lapse configuration label.
        self.frame3 = ctk.CTkFrame(self.frame_User_SS, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame3.pack(pady=1, padx=10)

        # Frame that contains the break time configuration label.
        self.frame4 = ctk.CTkFrame(self.frame_User_SS, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame4.pack(pady=1, padx=10)

        # Frame that contains the sound configuration checkbox.
        self.frame5 = ctk.CTkFrame(self.frame_User_SS, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame5.pack(pady=1, padx=10)

        # Frame that contains the save and cancel buttons.
        self.frame6 = ctk.CTkFrame(self.frame_User_SS, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame6.pack(pady=10, padx=10)

        # Alert configuration label.
        self.setting_title = ctk.CTkLabel(self.frame1, text="Configurar Alertas", font=(font, 15), 
                                          corner_radius=5, fg_color=colors["soft_green"])
        self.setting_title.place(rely=0.5, relx=0.5, anchor="center")

        # Lenght label.
        self.lenght = ctk.CTkLabel(self.frame2, text="Duración", font=(font, 14))
        self.lenght.place(rely=0.5, relx=0.03, anchor="w")

        # Validate hours. 
        self.hours_entry = self.root.register(Validate_CMD.validate_hours)

        # Validate minutes or seconds. 
        self.min_sec_entry = self.root.register(Validate_CMD.validate_min_sec)

        # Lenght entry hours.
        self.lenght_entryHH = ctk.CTkEntry(self.frame2, font=(font,14), width=40, justify="center",
                                           validate="key", validatecommand=(self.hours_entry, "%P"))
        self.lenght_entryHH.place(rely=0.5, relx=0.76, anchor="e")
        self.lenght_entryHH.insert(0, "HH")
        self.lenght_entryHH.bind("<Button-1>", lambda remove: self.lenght_entryHH.delete(0, tk.END))

        # Two points separator.
        self.colon_lenght_entry = ctk.CTkLabel(self.frame2, text=":", font=(font, 14))
        self.colon_lenght_entry.place(rely=0.5, relx=0.79, anchor="e")

        # Lenght entry minutes.
        self.lenght_entryMM = ctk.CTkEntry(self.frame2, font=(font,14), width=40, justify="center",
                                           validate="key", validatecommand=(self.min_sec_entry, "%P"))
        self.lenght_entryMM.place(rely=0.5, relx=0.97, anchor="e")
        self.lenght_entryMM.insert(0, "MM")
        self.lenght_entryMM.bind("<Button-1>", lambda remove: self.lenght_entryMM.delete(0, tk.END))

        # Lapse label.
        self.lapse = ctk.CTkLabel(self.frame3, text="Intervalo Alertas", font=(font, 14))
        self.lapse.place(rely=0.5, relx=0.03, anchor="w")

        # Lapse entry.
        self.lapse_entry = ctk.CTkEntry(self.frame3, font=(font,14), width=40, justify="center",
                                        validate="key", validatecommand=(self.min_sec_entry, "%P"))
        self.lapse_entry.place(rely=0.5, relx=0.97, anchor="e")
        self.lapse_entry.insert(0, "MM")
        self.lapse_entry.bind("<Button-1>", lambda remove: self.lapse_entry.delete(0, tk.END))

        # Break time label.
        self.break_time = ctk.CTkLabel(self.frame4, text="Tiempo Descanso", font=(font, 14))
        self.break_time.place(rely=0.5, relx=0.03, anchor="w")

        # Break time entry minutes.
        self.break_time_entryMM = ctk.CTkEntry(self.frame4, font=(font,14), width=40, justify="center",
                                               validate="key", validatecommand=(self.min_sec_entry, "%P"))

        self.break_time_entryMM.place(rely=0.5, relx=0.76, anchor="e")
        self.break_time_entryMM.insert(0, "MM")
        self.break_time_entryMM.bind("<Button-1>", lambda remove: self.break_time_entryMM.delete(0, tk.END))

        # Two points separator.
        self.colon_break_time_entry = ctk.CTkLabel(self.frame4, text=":", font=(font, 14))
        self.colon_break_time_entry.place(rely=0.5, relx=0.79, anchor="e")

        # Break time entry seconds.
        self.break_time_entrySS = ctk.CTkEntry(self.frame4, font=(font,14), width=40, justify="center",
                                               validate="key", validatecommand=(self.min_sec_entry, "%P"))

        self.break_time_entrySS.place(rely=0.5, relx=0.97, anchor="e")
        self.break_time_entrySS.insert(0, "SS")
        self.break_time_entrySS.bind("<Button-1>", lambda remove: self.break_time_entrySS.delete(0, tk.END))

        # Sound alert label.
        self.sound_alert = ctk.CTkLabel(self.frame5, text="Activar Sonido", font=(font, 14))
        self.sound_alert.place(rely=0.5, relx=0.03, anchor="w")

        # Sound alert checkbox.
        self.sound_alert_choice = ctk.IntVar()
        self.sound_alert_CB = ctk.CTkCheckBox(self.frame5, text=None, variable=self.sound_alert_choice, width=20, height=20, hover=True, 
                                              fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.sound_alert_CB.place(rely=0.5, relx=1, anchor="e")

        # Save button.
        self.save_button = ctk.CTkButton(self.frame6, width=10, height=10, text="Guardar", font=(font,14), 
                                              command=self.save_settings, corner_radius=10, hover=True, 
                                              fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.save_button.place(rely=0.5, relx=0.1, anchor="w")

        # Cancel button.
        self.cancel_button = ctk.CTkButton(self.frame6, width=10, height=10, text="Cancelar", font=(font,14),
                                           command=self.cancel_settings, corner_radius=10, hover=True, 
                                           fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.cancel_button.place(rely=0.5, relx=0.9, anchor="e")

    # This method saves settings in the user's main menu.
    def save_settings(self):
        # Get when the sound checkbox is activated or not.
        if self.sound_alert_choice.get() == 1:
            self.sound = True
        else:
            self.sound = False

        lenght_HH = self.lenght_entryHH.get()
        lenght_MM = self.lenght_entryMM.get()
        lapse = self.lapse_entry.get()
        break_time_MM = self.break_time_entryMM.get()
        break_time_SS = self.break_time_entrySS.get()

        to_validate = lenght_HH + lenght_MM + lapse + break_time_MM + break_time_SS + str(self.sound)
        check_values = Check_Values_Configuration.check_settings(self, to_validate)

        # Verify if all entries are filled.
        if check_values[0] != True:
            # Pop-ups a message box if any entry is unfilled.
            if check_values[1] == "Invalid Time":
                RelaxApp_MessageBox_Options(self.root, self.window_User_SS, "Invalid Time")
            # Verify if lenght entry is not higher than 16hs.
            elif check_values[1] == "Extra Hours":
                RelaxApp_MessageBox_Options(self.root, self.window_User_SS, "Extra Hours")
            # Verify if lenght entry is not lower than 1 minute.
            elif check_values[1] == "Minimum Time":
                RelaxApp_MessageBox_Options(self.root, self.window_User_SS, "Minimum Time")
            # Verify if lapse is not higher than lenght.
            elif check_values[1] == "Over Duration":
                RelaxApp_MessageBox_Options(self.root, self.window_User_SS, "Over Duration")
            # Verify if break is not higher than lapse.
            elif check_values[1] == "Over Lapse":
                RelaxApp_MessageBox_Options(self.root, self.window_User_SS, "Over Lapse")
            # Verify if lapse is at least 1 minute.
            elif check_values[1] == "No Lapse":
                RelaxApp_MessageBox_Options(self.root, self.window_User_SS, "No Lapse")
            # Verify if break is at least 30 seconds.
            elif check_values[1] == "No Break":
                RelaxApp_MessageBox_Options(self.root, self.window_User_SS, "No Break")
        
        else:
            # Convert 60 minutes in 1 hour.
            if lenght_MM == "60":
                lenght_MM = "00"
                lenght_HH = str(int(lenght_HH) + 1)
                if len(lenght_HH) == 1:
                    lenght_HH = "0" + str(lenght_HH)
            # Convert 60 seconds in 1 minute.
            if break_time_SS == "60":
                break_time_SS = "00"
                break_time_MM = str(int(break_time_MM) + 1)
                if len(break_time_MM) == 1:
                    break_time_MM = "0" + str(break_time_MM)

            # All entries are concatenated in one string.
            self.values += lenght_HH
            self.values += lenght_MM
            self.values += lapse
            self.values += break_time_MM
            self.values += break_time_SS
            self.values += str(self.sound)

            # Varible "self.values" is saved in the database inside the "Visual_Configuration" column.
            if self.visual_options_values == True:
                database.user_configuration(databases["database1"], tables["settings_table"], user["login"], 
                                            "UpdateNULL", ("Profile_Name", "Visual_Configuration"), self.values)

            # Varible "self.values" is saved in the database inside the "Stretch_Configuration" column.    
            elif self.stretch_options_values == True:
                database.user_configuration(databases["database1"], tables["settings_table"], user["login"], 
                                            "UpdateNULL", ("Profile_Name", "Stretch_Configuration"), self.values)

            self.window_User_SS.destroy()
            RelaxApp_Structure.close_create2(self, RelaxApp_User_Main_Menu, self.root, self.frame, None, None, True)

    # This method cancel the configuration and close the windows in the front.
    def cancel_settings(self):
        self.window_User_SS.destroy()


##########################################################
###  Class that contains the user's personal settings  ###
##########################################################

class RelaxApp_User_Main_Menu_Sounds(RelaxApp_User_Settings_Structure):
    """This class opens a new window to set the user's personal sounds 
       of the App. Inherit all structure from parent."""
    
    def __init__(self, root):
        super().__init__()
        self.root = root

        # An empty string which is going to save all values when user save a configuration.
        self.final_sound = ""
        self.lapse_sound = ""

        # Frame at the back.
        self.frame_User_SS.configure(fg_color=colors["black"])
        self.frame_User_SS.pack(pady=0, padx=0, fill="both")  

        # Frame that contains the tittle of the window.
        self.frame1 = ctk.CTkFrame(self.frame_User_SS, height=50, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame1.pack(pady=10, padx=10)

        # Frame that contains the first sound to set.
        self.frame2 = ctk.CTkFrame(self.frame_User_SS, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame2.pack(pady=1, padx=10)

        # Frame that contains the second sound to set.
        self.frame3 = ctk.CTkFrame(self.frame_User_SS, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame3.pack(pady=1, padx=10)

        # Frame that contains the third sound to set.
        self.frame4 = ctk.CTkFrame(self.frame_User_SS, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame4.pack(pady=1, padx=10)

        # Frame that contains the fourth sound to set.
        self.frame5 = ctk.CTkFrame(self.frame_User_SS, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame5.pack(pady=1, padx=10)

        # Frame that contains the save and cancel buttons.
        self.frame6 = ctk.CTkFrame(self.frame_User_SS, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame6.pack(pady=10, padx=10)

        # Tittle label.
        self.setting_title = ctk.CTkLabel(self.frame1, text="Configurar Sonidos", font=(font, 15), 
                                          corner_radius=5, fg_color=colors["soft_green"])
        self.setting_title.place(rely=0.5, relx=0.5, anchor="center")

        # Image of a play simbol.
        self.play_button_image = ctk.CTkImage(Image.open(os.path.join(image_path, "Play.png")).resize((40,40)))

        # Image of a play simbol.
        self.pause_button_image = ctk.CTkImage(Image.open(os.path.join(image_path, "Pause.png")).resize((40,40)))

        # Sound by default 1 label.
        self.sound_alert_D1 = ctk.CTkLabel(self.frame2, text="Default 1", font=(font, 14))
        self.sound_alert_D1.place(rely=0.5, relx=0.03, anchor="w")

        # Button to play sound example.
        self.play_button_D1 = ctk.CTkButton(self.frame2, text=None, image=self.play_button_image, width=0, command=lambda: self.sound_default("Play", "Final"),
                                            hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.play_button_D1.place(rely=0.5, relx=0.35, anchor="w")

        # Button to pause sound example.
        self.pause_button_D1 = ctk.CTkButton(self.frame2, text=None, image=self.pause_button_image, width=0, command=lambda: self.sound_default("Pause", "Final"),
                                             hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.pause_button_D1.place(rely=0.5, relx=0.5, anchor="w")

        # Both variables get the selected choice by the user.
        self.sound_alert_choice1 = ctk.IntVar()
        self.sound_alert_choice2 = ctk.IntVar()

        # Checkbox to activate or deactivate sound by default 1 and set it as "final".
        self.sound_alert_D1_CB1 = ctk.CTkRadioButton(self.frame2, text=None, value=0, variable=self.sound_alert_choice1, hover=True, 
                                                     border_width_unchecked=2, border_width_checked=5, fg_color=colors["soft_green"], 
                                                     hover_color=colors["dark_green"])
        self.sound_alert_D1_CB1.place(rely=0.5, relx=0.72, anchor="w")

        # Checkbox to activate or deactivate sound by default 1 and set it as "lapse".
        self.sound_alert_D1_CB2 = ctk.CTkRadioButton(self.frame2, text=None, value=0, variable=self.sound_alert_choice2, hover=True, 
                                                     border_width_unchecked=2, border_width_checked=5, fg_color=colors["soft_green"], 
                                                     hover_color=colors["dark_green"])
        self.sound_alert_D1_CB2.place(rely=0.5, relx=0.87, anchor="w")

        # Sound by default 2 label.
        self.sound_alert_D2 = ctk.CTkLabel(self.frame3, text="Default 2", font=(font, 14))
        self.sound_alert_D2.place(rely=0.5, relx=0.03, anchor="w")

        # Button to play sound example.
        self.play_button_D2 = ctk.CTkButton(self.frame3, text=None, image=self.play_button_image, width=0, command=lambda: self.sound_default("Play", "Lapse"),
                                            hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.play_button_D2.place(rely=0.5, relx=0.35, anchor="w")

        # Button to pause sound example.
        self.pause_button_D2 = ctk.CTkButton(self.frame3, text=None, image=self.pause_button_image, width=0, command=lambda: self.sound_default("Pause", "Lapse"),
                                             hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.pause_button_D2.place(rely=0.5, relx=0.5, anchor="w")

        # Checkbox to activate or deactivate sound by default 2 and set it as "final".
        self.sound_alert_D2_CB1 = ctk.CTkRadioButton(self.frame3, text=None, value=1, variable=self.sound_alert_choice1, hover=True, 
                                                     border_width_unchecked=2, border_width_checked=5, fg_color=colors["soft_green"], 
                                                     hover_color=colors["dark_green"])
        self.sound_alert_D2_CB1.place(rely=0.5, relx=0.72, anchor="w")

        # Checkbox to activate or deactivate sound by default 2 and set it as "lapse".
        self.sound_alert_D2_CB2 = ctk.CTkRadioButton(self.frame3, text=None, value=1, variable=self.sound_alert_choice2, hover=True, 
                                                     border_width_unchecked=2, border_width_checked=5, fg_color=colors["soft_green"], 
                                                     hover_color=colors["dark_green"])
        self.sound_alert_D2_CB2.place(rely=0.5, relx=0.87, anchor="w")

        # Sound load 1 label.
        self.sound_alert_load1 = ctk.CTkButton(self.frame4, width=10, height=10, text="Cargar 1", font=(font, 14), command=lambda: self.sound_load("1"),
                                               corner_radius=10, hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.sound_alert_load1.place(rely=0.5, anchor="w")

        # Button to play sound example.
        self.play_button_load1 = ctk.CTkButton(self.frame4, text=None, image=self.play_button_image, width=0, command=lambda: self.sound_loaded("Play", "1"),
                                               hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.play_button_load1.place(rely=0.5, relx=0.35, anchor="w")

        # Button to pause sound example.
        self.pause_button_load1 = ctk.CTkButton(self.frame4, text=None, image=self.pause_button_image, width=0, command=lambda: self.sound_loaded("Pause", "1"),
                                                hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.pause_button_load1.place(rely=0.5, relx=0.5, anchor="w")

        # Checkbox to activate or deactivate sound loaded 2 and set it as "final".
        self.sound_alert_load1_CB1 = ctk.CTkRadioButton(self.frame4, text=None, value=2, variable=self.sound_alert_choice1, hover=True, 
                                                        border_width_unchecked=2, border_width_checked=5, fg_color=colors["soft_green"], 
                                                        hover_color=colors["dark_green"])
        self.sound_alert_load1_CB1.place(rely=0.5, relx=0.72, anchor="w")

        # Checkbox to activate or deactivate sound loaded 2 and set it as "lapse".
        self.sound_alert_load1_CB2 = ctk.CTkRadioButton(self.frame4, text=None, value=2, variable=self.sound_alert_choice2, hover=True, 
                                                        border_width_unchecked=2, border_width_checked=5, fg_color=colors["soft_green"], 
                                                        hover_color=colors["dark_green"])
        self.sound_alert_load1_CB2.place(rely=0.5, relx=0.87, anchor="w")

        # Sound load 2 label.
        self.sound_alert_load2 = ctk.CTkButton(self.frame5, width=10, height=10, text="Cargar 2", font=(font, 14), command=lambda: self.sound_load("2"),
                                               corner_radius=10, hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.sound_alert_load2.place(rely=0.5, anchor="w")

        # Button to play sound example.
        self.play_button_load2 = ctk.CTkButton(self.frame5, text=None, image=self.play_button_image, width=0, command=lambda: self.sound_loaded("Play", "2"),
                                               hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.play_button_load2.place(rely=0.5, relx=0.35, anchor="w")

        # Button to pause sound example.
        self.pause_button_load2 = ctk.CTkButton(self.frame5, text=None, image=self.pause_button_image, width=0, command=lambda: self.sound_loaded("Pause", "2"),
                                                hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.pause_button_load2.place(rely=0.5, relx=0.5, anchor="w")

        # Checkbox to activate or deactivate sound loaded 2 and set it as "final".
        self.sound_alert_load2_CB1 = ctk.CTkRadioButton(self.frame5, text=None, value=3, variable=self.sound_alert_choice1, hover=True, 
                                                        border_width_unchecked=2, border_width_checked=5, fg_color=colors["soft_green"], 
                                                        hover_color=colors["dark_green"])
        self.sound_alert_load2_CB1.place(rely=0.5, relx=0.72, anchor="w")

        # Checkbox to activate or deactivate sound loaded 2 and set it as "lapse".
        self.sound_alert_load2_CB2 = ctk.CTkRadioButton(self.frame5, text=None, value=3, variable=self.sound_alert_choice2, hover=True, 
                                                        border_width_unchecked=2, border_width_checked=5, fg_color=colors["soft_green"], 
                                                        hover_color=colors["dark_green"])
        self.sound_alert_load2_CB2.place(rely=0.5, relx=0.87, anchor="w")

        # Save button.
        self.save_button = ctk.CTkButton(self.frame6, width=10, height=10, text="Guardar", font=(font,14), 
                                         command=self.save_settings, corner_radius=10, hover=True, 
                                         fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.save_button.place(rely=0.5, relx=0.1, anchor="w")

        # Cancel button.
        self.cancel_button = ctk.CTkButton(self.frame6, width=10, height=10, text="Cancelar", font=(font,14),
                                           command=self.cancel_settings, corner_radius=10, hover=True, 
                                           fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.cancel_button.place(rely=0.5, relx=0.9, anchor="e")

        # An information is showed when mouse is over "Configurar Sonidos".
        ToolTip(self.setting_title, msg="Debes elegir un sonido de alarma en la columna 1 que \nsonará al finalizar el contador y otro en la columna 2 \npara que se ejecute \
entre cada alerta.", parent_kwargs = { "bg": colors["black"]}, delay=0.5, font=(font,11), fg=colors["white"], bg=colors["soft_grey"], padx=10, pady=10)

    # This method runs and stop defaults sounds.
    def sound_default(self, action, sound):
        pygame.mixer.init()
        if action == "Play":
            if sound == "Final":
                pygame.mixer.music.load(os.path.join(sounds_path, "Final.mp3"))
            elif sound == "Lapse":
                pygame.mixer.music.load(os.path.join(sounds_path, "Lapse.mp3"))

            pygame.mixer.music.play(loops=0)
        elif action == "Pause":
            pygame.mixer.quit()

    # This method loads sounds.
    def sound_load(self, value):
        if value == "1":
            self.sound_loaded1_path = ctk.filedialog.askopenfilename(title="Cargar Sonido Final", filetypes=audio_accepted_files)
        elif value == "2":
            self.sound_loaded2_path = ctk.filedialog.askopenfilename(title="Cargar Sonido Alerta", filetypes=audio_accepted_files)

    # This method runs and stops loaded sounds.
    def sound_loaded(self, action, value):
        try:
            pygame.mixer.init()
            if action == "Play" and value == "1":
                pygame.mixer.music.load(self.sound_loaded1_path)  
                pygame.mixer.music.play(loops=0)
            elif action == "Play" and value == "2":
                pygame.mixer.music.load(self.sound_loaded2_path)  
                pygame.mixer.music.play(loops=0)
            elif action == "Pause":
                pygame.mixer.quit()
        except:
            pass

    # This method saves the configuration.
    def save_settings(self):
        try:
            # Final sound is choosen.
            if self.sound_alert_choice1.get() == 0:
                self.final_sound = os.path.join(sounds_path, "Final.mp3")
            elif self.sound_alert_choice1.get() == 1:
                self.final_sound = os.path.join(sounds_path, "Lapse.mp3")
            elif self.sound_alert_choice1.get() == 2:
                self.final_sound = self.sound_loaded1_path
            elif self.sound_alert_choice1.get() == 3:
                self.final_sound = self.sound_loaded2_path
        except:
            self.final_sound = ""

        try:
            # Lapse sound is choosen.
            if self.sound_alert_choice2.get() == 0:
                self.lapse_sound = os.path.join(sounds_path, "Final.mp3")
            elif self.sound_alert_choice2.get() == 1:
                self.lapse_sound = os.path.join(sounds_path, "Lapse.mp3")
            elif self.sound_alert_choice2.get() == 2:
                self.lapse_sound = self.sound_loaded1_path
            elif self.sound_alert_choice2.get() == 3:
                self.lapse_sound = self.sound_loaded2_path
        except:
            self.lapse_sound = ""

        # MessageBox is called when user try to save a configuration with a loaded sound before loading.
        if self.final_sound == "" or self.lapse_sound == "":
            RelaxApp_MessageBox_Options(self.root, self.window_User_SS, "No Sound")
        else:
            # Varible "self.final_sound" is saved in the database inside the "Final_Sounds_Configuration" column.
            database.user_configuration(databases["database1"], tables["settings_table"], user["login"], 
                                        "UpdateNULL", ("Profile_Name", "Final_Sounds_Configuration"), self.final_sound)
            
            # Varible "self.lapse_sound" is saved in the database inside the "Lapse_Sounds_Configuration" column.
            database.user_configuration(databases["database1"], tables["settings_table"], user["login"], 
                                        "UpdateNULL", ("Profile_Name", "Lapse_Sounds_Configuration"), self.lapse_sound)
            
            self.window_User_SS.destroy()

    # This method cancel the configuration to returns to the main menu.
    def cancel_settings(self):
        self.window_User_SS.destroy()

    # Function that show information about how to use the sound settings.
    def show_info(self ,text):
        self.text = text
        ctk.CTkLabel(self.root, text=f' "{self.text}" ', font=("Segoe Print", 22),
        fg_color=colors["soft_grey"]).pack()


#######################################################
###  Class that is showed when RelaxApp is running  ###
#######################################################

class RelaxApp_Running(RelaxApp_Running_Structure):
    """This class start RelaxApp. All countdown are executed depending on previus
       values choosen. Inherit all structure from parent."""
    
    def __init__(self, root, frame, visual_set, stretch_set, value_VO, value_SO, final_sound, lapse_sound):

        super().__init__()

        self.root = root
        self.frame = frame
        pygame.mixer.init()
        self.start_time = time.perf_counter()
        
        # Variables to set which threading is started.
        self.visual_set = visual_set
        self.stretch_set = stretch_set
        self.value_VO = value_VO
        self.value_SO = value_SO
        self.final_sound = final_sound
        self.lapse_sound = lapse_sound
        
        # Variable to stop bucles when return button is used after countdown is finished.
        self.app_running = True
        # Variables to stop bucles when function TR_VO_countdown or TR_SO_countdown are finished.
        self.stop_countdown_VO = False
        self.stop_countdown_SO = False

        # Dictionary that contains each value of user's visual options settings.
        self.values_VO = {"time_left_HH" : self.value_VO[0:2],
                          "time_left_MM" : self.value_VO[2:4],
                          "next_alert_MM" : self.value_VO[4:6],
                          "breaktime_MM" : self.value_VO[6:8],
                          "breaktime_SS" : self.value_VO[8:10],
                          "sound_active" : self.value_VO[10::]}
               
        # Dictionary that contains each value of user's stretch options settings.
        self.values_SO = {"time_left_HH" : self.value_SO[0:2],
                          "time_left_MM" : self.value_SO[2:4],
                          "next_alert_MM" : self.value_SO[4:6],
                          "breaktime_MM" : self.value_SO[6:8],
                          "breaktime_SS" : self.value_SO[8:10],
                          "sound_active" : self.value_SO[10::]}

        # Initial values of all visual options settings.
        self.time_left_HH_VO = ctk.StringVar(value=self.values_VO["time_left_HH"])
        self.time_left_MM_VO = ctk.StringVar(value=self.values_VO["time_left_MM"])
        self.next_alert_MM_VO = ctk.StringVar(value=self.values_VO["next_alert_MM"])
        self.next_alert_SS_VO = ctk.StringVar(value="00")
        self.breaktime_MM_VO = ctk.StringVar(value=self.values_VO["breaktime_MM"])
        self.breaktime_SS_VO = ctk.StringVar(value=self.values_VO["breaktime_SS"])
        self.sound_active_VO = ctk.StringVar(value=self.values_VO["sound_active"])

        # Initial values of all stretch options settings.
        self.time_left_HH_SO = ctk.StringVar(value=self.values_SO["time_left_HH"])
        self.time_left_MM_SO = ctk.StringVar(value=self.values_SO["time_left_MM"])
        self.next_alert_MM_SO = ctk.StringVar(value=self.values_SO["next_alert_MM"])
        self.next_alert_SS_SO = ctk.StringVar(value="00")
        self.breaktime_MM_SO = ctk.StringVar(value=self.values_SO["breaktime_MM"])
        self.breaktime_SS_SO = ctk.StringVar(value=self.values_SO["breaktime_SS"])
        self.sound_active_SO = ctk.StringVar(value=self.values_SO["sound_active"])

        # Varibales that get the sound value set to active or deactive sound alert.
        self.sound_VO = self.sound_active_VO.get()
        self.sound_SO = self.sound_active_SO.get()

        # Variables that set the position in "Y" when both visual options and stretch options are active.
        self.frame_visual_rely = 0.25
        self.frame_stretch_rely = 0.62
        self.stretch_title_rely = 0.44

        # Variables that set the position in "Y" when visual options is deactive and stretch options is active.
        if self.visual_set == False and self.stretch_set == True:
            self.frame_stretch_rely = 0.25
            self.stretch_title_rely = 0.07

        if self.visual_set == True:
            # Frame that contains visual options.
            self.frame_visual = ctk.CTkFrame(self.frame_RS, height=100, width=250, fg_color=colors["black"], 
                                                corner_radius=10)
            self.frame_visual.place(rely=self.frame_visual_rely, relx=0.5, anchor="center")

            # Main title of the frame.
            self.visual_title = ctk.CTkLabel(self.frame_RS, text="Descanso Visual", font=(font, 16))
            self.visual_title.place(rely=0.07, relx=0.5, anchor="center")

            # Vertical bar between time left and alert.
            self.bar_VO = ctk.CTkLabel(self.frame_visual, text=None, width=4, height=100, fg_color=colors["soft_grey"])
            self.bar_VO.place(relx=0.61)

            # Time left title.
            self.time_left_title_VO = ctk.CTkLabel(self.frame_visual, text="Tiempo Restante", font=(font, 14))
            self.time_left_title_VO.place(rely=0.15, relx=0.04, anchor="w")

            # Labels that contains "HH", ":" and "MM" of the time left.
            self.time_left_HH_VO_label = ctk.CTkLabel(self.frame_visual, textvariable=self.time_left_HH_VO, font=(font, 24))
            self.time_left_HH_VO_label.place(rely=0.5, relx=0.11, anchor="w")

            self.colon_VO_1 = ctk.CTkLabel(self.frame_visual, text=":", font=(font, 28))
            self.colon_VO_1.place(rely=0.5, relx=0.27, anchor="w")

            self.time_left_MM_VO_label = ctk.CTkLabel(self.frame_visual, textvariable=self.time_left_MM_VO, font=(font, 24))
            self.time_left_MM_VO_label.place(rely=0.5, relx=0.32, anchor="w")

            # Next alert title.
            self.next_alert_title_VO = ctk.CTkLabel(self.frame_visual, text="Alerta", font=(font, 14), justify="center")
            self.next_alert_title_VO.place(rely=0.15, relx=0.96, anchor="e")

            # Labels that contains "MM", ":" and "SS" of the next alert.
            self.next_alert_MM_VO_label = ctk.CTkLabel(self.frame_visual, textvariable=self.next_alert_MM_VO, font=(font, 16))
            self.next_alert_MM_VO_label.place(rely=0.4, relx=0.81, anchor="e")

            self.colon_VO_2 = ctk.CTkLabel(self.frame_visual, text=":", font=(font, 16))
            self.colon_VO_2.place(rely=0.4, relx=0.85, anchor="e")

            self.next_alert_SS_VO_label = ctk.CTkLabel(self.frame_visual, textvariable=self.next_alert_SS_VO, font=(font, 16))
            self.next_alert_SS_VO_label.place(rely=0.4, relx=0.96, anchor="e")

            # Break time title.
            self.breaktime_title_VO = ctk.CTkLabel(self.frame_visual, text="Descanso", font=(font, 14), justify="center")
            self.breaktime_title_VO.place(rely=0.6, relx=0.96, anchor="e")

            # Labels that contains "MM", ":" and "SS" of the break time.
            self.breaktime_MM_VO_label = ctk.CTkLabel(self.frame_visual, textvariable=self.breaktime_MM_VO, font=(font, 16))
            self.breaktime_MM_VO_label.place(rely=0.8, relx=0.81, anchor="e")

            self.colon_VO_3 = ctk.CTkLabel(self.frame_visual, text=":", font=(font, 16))
            self.colon_VO_3.place(rely=0.8, relx=0.85, anchor="e")

            self.breaktime_SS_VO_label = ctk.CTkLabel(self.frame_visual, textvariable=self.breaktime_SS_VO, font=(font, 16))
            self.breaktime_SS_VO_label.place(rely=0.8, relx=0.96, anchor="e")

        if self.stretch_set == True:
            # Frame that contains stretch options.
            self.frame_stretch = ctk.CTkFrame(self.frame_RS, height=100, width=250, fg_color=colors["black"], 
                                                corner_radius=10)
            self.frame_stretch.place(rely=self.frame_stretch_rely, relx=0.5, anchor="center")

            # Main title of the frame.
            self.stretch_title = ctk.CTkLabel(self.frame_RS, text="Estirar", font=(font, 16))
            self.stretch_title.place(rely=self.stretch_title_rely, relx=0.5, anchor="center")

            # Vertical bar between time left and alert.
            self.bar_SO = ctk.CTkLabel(self.frame_stretch, text=None, width=4, height=100, fg_color=colors["soft_grey"])
            self.bar_SO.place(relx=0.61)

            # Time left title.
            self.time_left_title_SO = ctk.CTkLabel(self.frame_stretch, text="Tiempo Restante", font=(font, 14))
            self.time_left_title_SO.place(rely=0.15, relx=0.04, anchor="w")

            # Labels that contains "HH", ":" and "MM" of the time left.
            self.time_left_HH_SO_label = ctk.CTkLabel(self.frame_stretch, textvariable=self.time_left_HH_SO, font=(font, 24))
            self.time_left_HH_SO_label.place(rely=0.5, relx=0.11, anchor="w")

            self.colon_SO_1 = ctk.CTkLabel(self.frame_stretch, text=":", font=(font, 28))
            self.colon_SO_1.place(rely=0.5, relx=0.27, anchor="w")

            self.time_left_MM_SO_label = ctk.CTkLabel(self.frame_stretch, textvariable=self.time_left_MM_SO, font=(font, 24))
            self.time_left_MM_SO_label.place(rely=0.5, relx=0.32, anchor="w")

            # Next alert title.
            self.next_alert_title_SO = ctk.CTkLabel(self.frame_stretch, text="Alerta", font=(font, 14), justify="center")
            self.next_alert_title_SO.place(rely=0.15, relx=0.96, anchor="e")

            # Labels that contains "MM", ":" and "SS" of the next alert.
            self.next_alert_MM_SO_label = ctk.CTkLabel(self.frame_stretch, textvariable=self.next_alert_MM_SO, font=(font, 16))
            self.next_alert_MM_SO_label.place(rely=0.4, relx=0.81, anchor="e")

            self.colon_SO_2 = ctk.CTkLabel(self.frame_stretch, text=":", font=(font, 16))
            self.colon_SO_2.place(rely=0.4, relx=0.85, anchor="e")

            self.next_alert_SS_SO_label = ctk.CTkLabel(self.frame_stretch, textvariable=self.next_alert_SS_SO, font=(font, 16))
            self.next_alert_SS_SO_label.place(rely=0.4, relx=0.96, anchor="e")

            # Break time title.
            self.breaktime_title_SO = ctk.CTkLabel(self.frame_stretch, text="Descanso", font=(font, 14), justify="center")
            self.breaktime_title_SO.place(rely=0.6, relx=0.96, anchor="e")

            # Labels that contains "MM", ":" and "SS" of the break time.
            self.breaktime_MM_SO_label = ctk.CTkLabel(self.frame_stretch, textvariable=self.breaktime_MM_SO, font=(font, 16))
            self.breaktime_MM_SO_label.place(rely=0.8, relx=0.81, anchor="e")

            self.colon_SO_3 = ctk.CTkLabel(self.frame_stretch, text=":", font=(font, 16))
            self.colon_SO_3.place(rely=0.8, relx=0.85, anchor="e")

            self.breaktime_SS_SO_label = ctk.CTkLabel(self.frame_stretch, textvariable=self.breaktime_SS_SO, font=(font, 16))
            self.breaktime_SS_SO_label.place(rely=0.8, relx=0.96, anchor="e")
        
        # Hidden button that init the countdown when this class is called.
        self.start = ctk.CTkButton(self.window_RS, text=None, command=self.threading(), hover=False, fg_color=colors["soft_grey"],
                                   bg_color=colors["soft_grey"])                        
        self.start.place(rely=0.9, relx=0.5, anchor="center")

        # Button that returns to the user's main menu.
        self.stop = ctk.CTkButton(self.window_RS, text="Volver", font=(font, 14), command=self.stop_app, width=80, height=20, 
                                  corner_radius=10, hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"],
                                  bg_color=colors["soft_grey"])
        self.stop.place(rely=0.85, relx=0.1, anchor="w")

        # Button that stop music when is playing.
        self.pause_alarm = ctk.CTkButton(self.window_RS, text="Silenciar", font=(font, 14), command=self.stop_sound, width=60, height=20, 
                                  corner_radius=10, hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"],
                                  bg_color=colors["soft_grey"])
        self.pause_alarm.place(rely=0.85, relx=0.9, anchor="e")

        # This variables are counting how many round have been lunched.
        self.init_TR_VO_multiplier = 0
        self.init_TR_SO_multiplier = 0
        self.init_VO_countdown_multiplier = 0
        self.init_SO_countdown_multiplier = 0

    # This method calls 4 of the 6 countdown.
    def threading(self):

        # Call all countdown funtions.
        if self.visual_set == True:
            t1=threading.Thread(target=self.TR_VO_countdown) 
            t1.start()
            t2= threading.Thread(target=self.NA_VO_countdown)
            t2.start()

        if self.stretch_set == True:
            t3=threading.Thread(target=self.TR_SO_countdown) 
            t3.start()
            t4=threading.Thread(target=self.NA_SO_countdown) 
            t4.start()     

    # This method starts the main countdown "Time Remaining" of the visual options.
    def TR_VO_countdown(self):

        # Hours and minutes of time remaining are gotten.
        TR_HH_value = int(self.time_left_HH_VO.get())
        TR_MM_value = int(self.time_left_MM_VO.get())

        while True:
            # This variable change when return button is pressed to stop or not the app.
            if self.app_running == False:
                self.stop_countdown_VO = True
                break              
            else:
                # Verify if values have one or two digits in order to add a "0" in front.
                if TR_MM_value > 9:
                    self.time_left_MM_VO.set(TR_MM_value)
                else:
                    self.time_left_MM_VO.set("0" + str(TR_MM_value))
                if TR_HH_value > 9:
                    self.time_left_HH_VO.set(TR_HH_value)
                else:
                    self.time_left_HH_VO.set("0" + str(TR_HH_value))

                self.init_timer(60, "TR_VO")
                if TR_MM_value > 0:
                    TR_MM_value -= 1
                # When minute is cero one is subtracted from the hours.
                elif TR_HH_value > 0:
                    TR_HH_value -= 1
                    TR_MM_value = 59
                # When the main countdown is 0 all label change.    
                if TR_HH_value == 0 and TR_MM_value == 0:
                    # Sound alert is called.
                    if self.sound_VO == "True":
                        self.play_sounds(1)
                    # Hours,minutes and colon of time remaining are hidden. 
                    self.time_left_HH_VO.set("")
                    self.time_left_MM_VO.set("")
                    self.colon_VO_1.place_forget()
                    # New label is set to show that the countdown is finished.
                    finished_label_VO = ctk.CTkLabel(self.frame_visual, text="Finalizado", font=(font, 20), corner_radius=5,
                                                    fg_color=colors["soft_green"])
                    finished_label_VO.place(rely=0.55, relx=0.06, anchor="w")
                    # All label are set as "00"
                    self.next_alert_MM_VO.set("00")
                    self.next_alert_SS_VO.set("00")
                    self.breaktime_MM_VO.set("00")
                    self.breaktime_SS_VO.set("00")
                    # Varible change to stop next alert and break time countdowns.
                    self.stop_countdown_VO = True
                    break

    # This method starts the countdown "Next Alert" of the visual options.
    def NA_VO_countdown(self):
        
        # Minutes and seconds of next alert are gotten.
        initial_value_MM = self.next_alert_MM_VO.get()
        initial_value_SS = self.next_alert_SS_VO.get()

        NA_MM_value = int(initial_value_MM)
        NA_SS_value = int(initial_value_SS)
 
        while NA_MM_value > -1:
            
            # Conditional that stop bucle when return button is pressed or time remaining is finished.
            if self.app_running == False or self.stop_countdown_VO == True:
                break
            # Verify if values have one or two digits in order to add a "0" in front.
            elif NA_SS_value > 9:
                self.next_alert_SS_VO.set(NA_SS_value)
            else:
                self.next_alert_SS_VO.set("0" + str(NA_SS_value))
            if NA_MM_value > 9:
                self.next_alert_MM_VO.set(NA_MM_value)
            else:
                self.next_alert_MM_VO.set("0" + str(NA_MM_value))

            # After 1 second one is subtracted from the seconds.
            if NA_SS_value > 0:
                self.init_timer(1, "VO_countdown")
                NA_SS_value -= 1
            # When second is cero one is subtracted from the minutes.
            elif NA_MM_value > 0:
                self.init_timer(1, "VO_countdown")
                NA_MM_value -= 1
                NA_SS_value = 59
            else:
                # Sound alert is called.
                if self.sound_VO == "True":
                    self.play_sounds(2)
                # Minutes and second are set as there was at the beggining.
                self.next_alert_SS_VO.set(initial_value_SS)
                self.next_alert_MM_VO.set(initial_value_MM)
                # New threading is run to start BT_VO_countdown function.
                threading.Thread(target=self.BT_VO_countdown).start()
                break
            
    # This method starts the countdown "Break Time" of the visual options.
    def BT_VO_countdown(self):
        
        # Minutes and seconds of next alert are gotten.
        initial_value_MM = self.breaktime_MM_VO.get()
        initial_value_SS = self.breaktime_SS_VO.get()

        BT_MM_value = int(initial_value_MM)
        BT_SS_value = int(initial_value_SS)

        while BT_MM_value > -1:
            # Conditional that stop bucle when return button is pressed or time remaining is finished.
            if self.app_running == False or self.stop_countdown_VO == True:
                break 

            # Verify if values have one or two digits in order to add a "0" in front.
            if BT_MM_value > 9:
                self.breaktime_MM_VO.set(BT_MM_value)
            else:
                self.breaktime_MM_VO.set("0" + str(BT_MM_value))
            if BT_SS_value > 9:
                self.breaktime_SS_VO.set(BT_SS_value)
            else:
                self.breaktime_SS_VO.set("0" + str(BT_SS_value))

            # After 1 second one is subtracted from the seconds.
            if BT_SS_value > 0:
                self.init_timer(1, "VO_countdown")
                BT_SS_value -= 1
            # When second is cero one is subtracted from the minutes.
            elif BT_MM_value > 0:
                self.init_timer(1, "VO_countdown")
                BT_MM_value -= 1
                BT_SS_value = 59
            else:
                # Sound alert is called.
                if self.sound_VO == "True":
                    self.play_sounds(2)
                # Minutos and second are set as there was at the beggining.
                self.breaktime_SS_VO.set(initial_value_SS)
                self.breaktime_MM_VO.set(initial_value_MM)
                # New threading is run to start BT_VO_countdown function.
                threading.Thread(target=self.NA_VO_countdown).start()
                break

    # This method starts the main countdown "Time Remaining" of the stretch options.
    def TR_SO_countdown(self):

        TR_HH_value = int(self.time_left_HH_SO.get())
        TR_MM_value = int(self.time_left_MM_SO.get())

        while True:
            if self.app_running == False:
                self.stop_countdown_SO = True
                break
            else:
                if TR_MM_value > 9:
                    self.time_left_MM_SO.set(TR_MM_value)
                else:
                    self.time_left_MM_SO.set("0" + str(TR_MM_value))
                if TR_HH_value > 9:
                    self.time_left_HH_SO.set(TR_HH_value)
                else:
                    self.time_left_HH_SO.set("0" + str(TR_HH_value))

                self.init_timer(60, "TR_SO")
                if TR_MM_value > 0:
                    TR_MM_value -=1
                elif TR_HH_value > 0:     
                    TR_HH_value -=1
                    TR_MM_value = 59  
                if TR_HH_value == 0 and TR_MM_value == 0:
                    if self.sound_SO == "True":
                        self.play_sounds(1)
                    self.time_left_HH_SO.set("")
                    self.time_left_MM_SO.set("")
                    self.colon_SO_1.place_forget()
                    finished_label_SO = ctk.CTkLabel(self.frame_stretch, text="Finalizado", font=(font, 20), corner_radius=5,
                                                     fg_color=colors["soft_green"])
                    finished_label_SO.place(rely=0.55, relx=0.06, anchor="w")
                    self.next_alert_MM_SO.set("00")
                    self.next_alert_SS_SO.set("00")
                    self.breaktime_MM_SO.set("00")
                    self.breaktime_SS_SO.set("00")
                    self.stop_countdown_SO = True
                    break
            
    # This method starts the countdown "Next Alert" of the stretch options.
    def NA_SO_countdown(self):

        initial_value_MM = self.next_alert_MM_SO.get()
        initial_value_SS = self.next_alert_SS_SO.get()
        
        NA_MM_value = int(initial_value_MM)
        NA_SS_value = int(initial_value_SS)

        while NA_MM_value > -1:
            # Conditional that stop bucle when return button is pressed or time remaining is finished.
            if self.app_running == False or self.stop_countdown_SO == True:
                break
            elif NA_SS_value > 9:
                self.next_alert_SS_SO.set(NA_SS_value)
            else:
                self.next_alert_SS_SO.set("0" + str(NA_SS_value))         
            if NA_MM_value > 9:
                self.next_alert_MM_SO.set(NA_MM_value)
            else:
                self.next_alert_MM_SO.set("0" + str(NA_MM_value))

            if NA_SS_value > 0:
                self.init_timer(1, "SO_countdown")
                NA_SS_value -=1
            elif NA_MM_value > 0:
                self.init_timer(1, "SO_countdown")
                NA_MM_value -= 1
                NA_SS_value = 59
            else:
                if self.sound_SO == "True":
                    self.play_sounds(2)
                self.next_alert_SS_SO.set(initial_value_SS)
                self.next_alert_MM_SO.set(initial_value_MM)
                threading.Thread(target=self.BT_SO_countdown).start()
                break

    # This method starts the countdown "Break Time" of the stretch options.
    def BT_SO_countdown(self):

        initial_value_MM = self.breaktime_MM_SO.get()
        initial_value_SS = self.breaktime_SS_SO.get()

        BT_MM_value = int(initial_value_MM)
        BT_SS_value = int(initial_value_SS)

        while BT_MM_value > -1:
            # Conditional that stop bucle when return button is pressed or time remaining is finished.
            if self.app_running == False or self.stop_countdown_SO == True:
                break 

            if BT_SS_value > 9:
                self.breaktime_SS_SO.set(BT_SS_value)
            else:
                self.breaktime_SS_SO.set("0" + str(BT_SS_value))
            if BT_MM_value > 9:
                self.breaktime_MM_SO.set(BT_MM_value)
            else:
                self.breaktime_MM_SO.set("0" + str(BT_MM_value))
            
            if BT_SS_value > 0:
                self.init_timer(1, "SO_countdown")
                BT_SS_value -=1
            elif BT_MM_value > 0:
                self.init_timer(1, "SO_countdown")
                BT_MM_value -=1
                BT_SS_value = 59
            else:
                if self.sound_SO == "True":
                    self.play_sounds(2)
                self.breaktime_SS_SO.set(initial_value_SS)
                self.breaktime_MM_SO.set(initial_value_MM)
                threading.Thread(target=self.NA_SO_countdown).start()
                break

    # This method runs sounds alerts.
    def play_sounds(self, value):
        if self.app_running == True:
            # When value is "1" the sound related to "Time Remaining" is set.
            if value == 1:
                try:
                    if self.final_sound == "":
                        pygame.mixer.music.load(os.path.join(sounds_path, "Final.mp3"))  
                        pygame.mixer.music.play(loops=0)
                    else:
                        pygame.mixer.music.load(self.final_sound)  
                        pygame.mixer.music.play(loops=0)
                except:
                    pygame.mixer.music.load(os.path.join(sounds_path, "Final.mp3"))  
                    pygame.mixer.music.play(loops=0)

            # When value is "2" the sound related to "Lapse" is set.
            elif value == 2:
                try:    
                    if self.lapse_sound == "":
                        pygame.mixer.music.load(os.path.join(sounds_path, "Lapse.mp3"))  
                        pygame.mixer.music.play(loops=0)
                    else:
                        pygame.mixer.music.load(self.lapse_sound)  
                        pygame.mixer.music.play(loops=0)
                except:
                    pygame.mixer.music.load(os.path.join(sounds_path, "Final.mp3"))  
                    pygame.mixer.music.play(loops=0)

    # This method stops the app when return button is pressed.
    def stop_app(self):
        # Variable to stop all bucles running.
        self.app_running = False
        # Method is called to stop the sound alert.
        pygame.mixer.quit()
        self.window_RS.destroy()
        self.root.deiconify()

    def stop_sound(self):
        pygame.mixer.quit()
        pygame.mixer.init()
      
    # This method start timer and compare the time elapsed with "time.perf_counter".
    def init_timer(self, num_seconds, thread):

        # This conditional compense the delay between when the class is "init" with the moment that the timer is run. Only happend once
        if self.init_TR_VO_multiplier == 0 and self.init_TR_SO_multiplier == 0 and self.init_VO_countdown_multiplier == 0 and self.init_SO_countdown_multiplier == 0:
            init_elapsed_seconds = time.perf_counter() - self.start_time
            time.sleep(num_seconds - 0.1 - init_elapsed_seconds)
        else:
            # Time sleep is run with minus 0.1 to be compensated after and avoid irregulars rounds, have precision and the timer sinchronized.
            time.sleep(num_seconds - 0.1)

        current_time = time.perf_counter()

        elapsed_seconds = current_time - self.start_time

        # These conditionals get the final value to compensate and avoid the desynchronization in large timers
        if thread == "TR_VO":          
            remaining_to_compensate = num_seconds - (elapsed_seconds - (num_seconds * self.init_TR_VO_multiplier))
            self.init_TR_VO_multiplier += 1
        if thread == "TR_SO":          
            remaining_to_compensate = num_seconds - (elapsed_seconds - (num_seconds * self.init_TR_SO_multiplier))
            self.init_TR_SO_multiplier += 1
        elif thread == "VO_countdown":
            remaining_to_compensate = num_seconds - (elapsed_seconds - (num_seconds * self.init_VO_countdown_multiplier))
            self.init_VO_countdown_multiplier += 1
        elif thread == "SO_countdown":
            remaining_to_compensate = num_seconds - (elapsed_seconds - (num_seconds * self.init_SO_countdown_multiplier))
            self.init_SO_countdown_multiplier += 1
        from datetime import datetime
        if remaining_to_compensate < 0:
            remaining_to_compensate = 0

        time.sleep(remaining_to_compensate)


####################################################
###  Class that contains all pop-ups of the App  ###
####################################################

class RelaxApp_MessageBox_Options(RelaxApp_MessageBox_Structure):
    """This class defines all pop-ups of the App.
       Inherit all structure from parent."""

    def __init__(self, root, frame, message, user=None, values=None):

        super().__init__()
        
        self.root = root
        self.frame = frame
        self.message = message
        self.user = user
        self.values = values

        # Variable to set when the button "Accept", "Cancel" is activated
        self.select_button1 = False
        # Variable to set when the button "Return" is activated
        self.select_button2 = False

        if message == "Sign up":
            # Label ask/cancel user registration.
            self.ask_cancel_label = ctk.CTkLabel(self.window_MS, text="¿Está seguro que desea dar de alta el usuario indicado?", 
                                                 font=(font,14), bg_color=colors["soft_grey"])
            self.ask_cancel_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Cancel":
            # Label ask/cancel to cancel user registration.
            self.ask_cancel_label = ctk.CTkLabel(self.window_MS, text="¿Está seguro que desea cancelar el alta del usuario indicado?", 
                                                 font=(font,14), bg_color=colors["soft_grey"])
            self.ask_cancel_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Password Correct":
            # Label to confirm or not to change the password.
            self.pw_match = ctk.CTkLabel(self.window_MS, text="¿Está seguro que desea actualizar su contraseña?", 
                                         font=(font,14), bg_color=colors["soft_grey"])
            self.pw_match.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Password Incorrect":
            # Label to inform that the password 1 does not match with password 2.
            self.pw_unmatch = ctk.CTkLabel(self.window_MS, text="Las contraseñas introducidas no coinciden entre sí. \nVuelva a introducirlas.", 
                                           font=(font,14), bg_color=colors["soft_grey"])
            self.pw_unmatch.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Cancel Change PW":
            # Label ask/cancel to cancel to change password.
            self.pw_ask_cancel_label = ctk.CTkLabel(self.window_MS, text="¿Está seguro que desea cancelar el cambio de contraseña?", 
                                                    font=(font,14), bg_color=colors["soft_grey"])
            self.pw_ask_cancel_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button1 = True
        
        elif message == "No Profile":
            # Label to alert there's no profile set.
            self.no_profile_label = ctk.CTkLabel(self.window_MS, text="No tienes ningún perfil creado actualmente. Configura al menos un \nvalue para poder habilitar la opción de perfiles.", 
                                                 font=(font,14), bg_color=colors["soft_grey"])
            self.no_profile_label.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button2 = True
        
        elif message == "File_Corrupt":
            # Label to alert that the file was modified or is broken.
            self.file_corrupt_label = ctk.CTkLabel(self.window_MS, text="El archivo que intenta abrir está dañado, ha sido modificado o \nya existe y no puede abrirse. Compruebe con otro archivo.", 
                                                   font=(font,14), bg_color=colors["soft_grey"])
            self.file_corrupt_label.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button2 = True

        elif message == "Invalid_Format":
            # Label to alert that the file was modified or is broken.
            self.file_corrupt_label = ctk.CTkLabel(self.window_MS, text="El archivo que intenta abrir no tiene un formato soportado y \nno puede abrirse. Compruebe con otro archivo.", 
                                                   font=(font,14), bg_color=colors["soft_grey"])
            self.file_corrupt_label.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button2 = True
        
        elif message == "Remove Account":
            # Label ask/cancel to sign out.
            self.pw_ask_cancel_label = ctk.CTkLabel(self.window_MS, text=f"Esta opción permite eliminar completamente la cuenta \nde '{self.user}'. ¿Está seguro que desea continuar?", 
                                                    font=(font,14), bg_color=colors["soft_grey"])
            self.pw_ask_cancel_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Sign Out":
            # Label ask/cancel to sign out.
            self.pw_ask_cancel_label = ctk.CTkLabel(self.window_MS, text=f"¿Está seguro que desea cerrar la sesión de '{self.user}'?", 
                                                    font=(font,14), bg_color=colors["soft_grey"])
            self.pw_ask_cancel_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Invalid Time":
            # Label to alert not to leave entries unfilled.
            self.empty_entry_label = ctk.CTkLabel(self.window_MS, text="Los campos tienen que tener 2 números entre el 0 y el 60 \npara guardarlos.", 
                                                  font=(font,14), bg_color=colors["soft_grey"])
            self.empty_entry_label.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button2 = True

        elif message == "Extra Hours":
            # Label to alert not to work extra hours.
            self.extra_hours_label = ctk.CTkLabel(self.window_MS, text="No puedes configurar mas de 16hs de duración. Recuerda que \nmínimo debes dormir 8hs.", 
                                                  font=(font,14), bg_color=colors["soft_grey"])
            self.extra_hours_label.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button2 = True

        elif message == "Minimum Time":
            # Label to alert not to work extra hours.
            self.minimum_time_label = ctk.CTkLabel(self.window_MS, text="Debes configurar al menos 1 minuto de duración.", 
                                                   font=(font,14), bg_color=colors["soft_grey"])
            self.minimum_time_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button2 = True
        
        elif message == "Over Duration":
            # Label to alert not to set breaktime over lapse time.
            self.over_lapse_label = ctk.CTkLabel(self.window_MS, text="El tiempo de intervalo no puede ser superior a la duración configurada.", 
                                                 font=(font,14), bg_color=colors["soft_grey"])
            self.over_lapse_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button2 = True
        
        elif message == "Over Lapse":
            # Label to alert not to set breaktime over lapse time.
            self.over_lapse_label = ctk.CTkLabel(self.window_MS, text="El tiempo de descanso no puede ser superior al intervalo \nde alertas configurado.", 
                                                 font=(font,14), bg_color=colors["soft_grey"])
            self.over_lapse_label.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button2 = True
        
        elif message == "No Lapse":
            # Label to alert to set at least 1 minute between alerts.
            self.no_lapse_label = ctk.CTkLabel(self.window_MS, text="El tiempo de intervalo entre alertas debe tener al menos 1 minuto.", 
                                               font=(font,14), bg_color=colors["soft_grey"])
            self.no_lapse_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button2 = True
        
        elif message == "No Break":
            # Label to alert to set at least 1 minute between alerts.
            self.no_break_label = ctk.CTkLabel(self.window_MS, text="El tiempo de descanso debe tener al menos 30 segundos.", 
                                               font=(font,14), bg_color=colors["soft_grey"])
            self.no_break_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button2 = True

        elif message == "Valid Profile":
            # Label to alert to set at least 1 minute between alerts.
            self.valid_profile = ctk.CTkLabel(self.window_MS, text="Está seguro que desea importar el perfil seleccionado? Esto \neliminará el último de la lista  de perfiles si estuviera llena.", 
                                              font=(font,14), bg_color=colors["soft_grey"])
            self.valid_profile.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "No Settings":
            # Label to alert to choose at least one option to start the App.
            self.no_settings_label = ctk.CTkLabel(self.window_MS, text="Debes seleccionar al menos una opción antes de iniciar la aplicación.", 
                                                  font=(font,14), bg_color=colors["soft_grey"])
            self.no_settings_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button2 = True

        elif message == "No Values Set":
            # Label to alert to set the values of the option chosen to start the App.
            self.no_values_set_label = ctk.CTkLabel(self.window_MS, text="Cada opción elegida debe tener valores configurados antes \nde iniciar la aplicación.", 
                                                    font=(font,14), bg_color=colors["soft_grey"])
            self.no_values_set_label.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button2 = True

        elif message == "No Sound":
            # Label to alert that a load sounds is trying to save but no file is loaded.
            self.no_sound_label = ctk.CTkLabel(self.window_MS, text="No puedes guardar una configuración con un sonido propio \nsin cargarlo previamente.", 
                                               font=(font,14), bg_color=colors["soft_grey"])
            self.no_sound_label.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button2 = True
        
        elif message == "No Name":
            # Label to alert that a load sounds is trying to save but no file is loaded.
            self.no_name_label = ctk.CTkLabel(self.window_MS, text="El nombre del perfil deber tener al menos un caracter y un \nmáximo de 20.", 
                                              font=(font,14), bg_color=colors["soft_grey"])
            self.no_name_label.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button2 = True
         
        elif message == "Full Profile":
            # Label to alert that a load sounds is trying to save but no file is loaded.
            self.full_profile_label = ctk.CTkLabel(self.window_MS, text="No se pueden agregar mas de 3 perfiles. Elimine alguno de los \nque tiene configurados.", 
                                                   font=(font,14), bg_color=colors["soft_grey"])
            self.full_profile_label.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button2 = True
        
        elif message == "Duplicated":
            # Label to alert that a load sounds is trying to save but no file is loaded.
            self.duplicated_profile_label = ctk.CTkLabel(self.window_MS, text="El nombre del perfil que intenta agregar ya existe. Elija \nuno distinto.", 
                                            font=(font,14), bg_color=colors["soft_grey"])
            self.duplicated_profile_label.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button2 = True 

        if self.select_button1 == True:
            # Button to accept user registration.
            self.accept_ask_cancel_button = ctk.CTkButton(self.window_MS, width=80, height=17, text="Aceptar", font=(font,14), 
                                                          command=lambda: self.accept_button(message), corner_radius=10,
                                                          hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"], 
                                                          bg_color=colors["soft_grey"])
            self.accept_ask_cancel_button.place(rely=0.65, relx=0.25, anchor="w")

            # Button to cancel user registration.
            self.cancel_ask_cancel_button = ctk.CTkButton(self.window_MS, width=80, height=17, text="Cancelar", font=(font,14), 
                                                          command=self.cancel_button, corner_radius=10, hover=True, 
                                                          fg_color=colors["soft_green"], hover_color=colors["dark_green"],
                                                          bg_color=colors["soft_grey"])
            self.cancel_ask_cancel_button.place(rely=0.65, relx=0.75, anchor="e")

        if self.select_button2 == True:
            # Button to continue to the main menu.
            self.continue_registration_button = ctk.CTkButton(self.window_MS, width=80, height=17, text="Volver", font=(font,14), 
                                                              command=self.return_button, corner_radius=10, hover=True,
                                                              fg_color=colors["soft_green"], hover_color=colors["dark_green"],
                                                              bg_color=colors["soft_grey"])
            self.continue_registration_button.place(rely=0.65, relx=0.5, anchor="center")

    # This method accepts registration or accepts cancelation
    def accept_button(self, message):

        if message == "Sign up":
            # App connects with the database to check if the information is valid or not.
            database.edit_table(databases["database1"], tables["users_table"], self.user)
        elif message == "Password Correct":
             # App connects with the database to check if the information is valid or not. 
            database.edit_table(databases["database1"], tables["users_table"], self.user)
        elif message == "Valid Profile":
            database.query(f"SELECT ID FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}'")
            id = []

            for index in range(len(database.value)):
                id.append(database.value[index][0])

            self.values.append(id)

            database.user_configuration(databases["database1"], tables["settings_table"], user["login"], 
                                        "Import Profile", "Login, Profile_Name, Date_Time, Default_Profile, Visual_Configuration, \
                                        Stretch_Configuration, Final_Sounds_Configuration, Lapse_Sounds_Configuration", self.values)

            RelaxApp_MessageBox_Structure.clean_MB_widgets(self, self.window_MS)
            self.new_message_box("Continue2")

            RelaxApp_Structure.close_create(self, RelaxApp_User_Main_Menu, self.root, self.frame, None, None, True)
            
            return
        
        # User registration is canceled and turn back to main menu.
        elif message == "Cancel" or message == "Cancel Change PW" or message == "Sign Out":
            self.window_MS.destroy()
            RelaxApp_Structure.close_create2(self, RelaxApp_Initial_Frame, self.root, self.frame)
            return
        
        elif message == "Remove Account":
            database.user_configuration(databases["database1"], tables["users_table"], user["login"], "Remove Account")
            database.user_configuration(databases["database1"], tables["settings_table"], user["login"], "Remove Account")
            self.window_MS.destroy()
            RelaxApp_Structure.close_create2(self, RelaxApp_Initial_Frame, self.root, self.frame)
            return
        
        # User is registered.
        if database.validate_editing == True:

            RelaxApp_MessageBox_Structure.clean_MB_widgets(self, self.window_MS)
            self.new_message_box("Continue")

        # User is not registered.
        else:
            # # Registration pop-up window is closed.
            RelaxApp_MessageBox_Structure.clean_MB_widgets(self, self.window_MS)
            self.new_message_box("Error")
 
    # This method accepts cancelation or cancels cancelation.    
    def cancel_button(self):
        self.window_MS.destroy()

    # This method is run after a message box is asking to "continue" or not.
    def continue_button(self, message):
        if message == "Continue":
            self.window_MS.destroy()
            RelaxApp_Structure.close_create(self, RelaxApp_Initial_Frame, self.root, self.frame)
        elif message == "Continue2":
            self.window_MS.destroy()

    # This method turns back to the last menu opened.
    def return_button(self):
        self.window_MS.destroy()

    # This method runs a new message box after a message box when is needed a second confirmation.
    def new_message_box(self, message):
        
        if message == "Error":
            # Label confirm user registration.
            self.continue_registration = ctk.CTkLabel(self.window_MS, text=database.message, font=(font,14), 
                                                      bg_color=colors["soft_grey"])
            self.continue_registration.place(rely=0.35, relx=0.5, anchor="center")

            # Button to continue to the main menu.
            self.continue_registration_button = ctk.CTkButton(self.window_MS, width=80, height=17, text="Volver", font=(font,14), 
                                                              command=self.return_button, corner_radius=10, hover=True,
                                                              fg_color=colors["soft_green"], hover_color=colors["dark_green"],
                                                              bg_color=colors["soft_grey"])
            self.continue_registration_button.place(rely=0.65, relx=0.5, anchor="center")

            return
        
        elif message == "Continue":

            # Label confirm user registration.
            self.continue_registration = ctk.CTkLabel(self.window_MS, text=database.message, font=(font,14), 
                                                      bg_color=colors["soft_grey"])
            self.continue_registration.place(rely=0.35, relx=0.5, anchor="center")
        
        elif message == "Continue2":
            # Label confirm user registration.
            self.continue_registration = ctk.CTkLabel(self.window_MS, text="El perfil ha sido importado exitósamente y se ha establecido \ncomo predeterminado.", font=(font,14), 
                                                      bg_color=colors["soft_grey"])
            self.continue_registration.place(rely=0.35, relx=0.5, anchor="center")

        # Button to continue to the main menu.
        self.continue_registration_button = ctk.CTkButton(self.window_MS, width=80, height=17, text="Continuar", font=(font,14), 
                                                            command=lambda: self.continue_button(message), corner_radius=10, hover=True, 
                                                            fg_color=colors["soft_green"], hover_color=colors["dark_green"],
                                                            bg_color=colors["soft_grey"])
        self.continue_registration_button.place(rely=0.65, relx=0.5, anchor="center")
