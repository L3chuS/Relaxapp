import tkinter as tk
import customtkinter as ctk
import Base_Datos.base_datos as bd
from Base_Datos.valores_presets import user, databases, tables
from os import path
import ctypes
import time
import threading
import pygame
from PIL import Image
from tktooltip import ToolTip
import hashlib

# Connect to the database.
base_datos = bd.BaseDatos(**bd.acceso_root)

# Get the windows resolution regardless of rescaling
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

# Get the parent folder path and the image folder path.
main_path = path.dirname(__file__)
main_path_edited = ""

# Bucle that changes "\" for "/" because mysql don't accept first value.
for letra in main_path:
    if letra != "\\":
        main_path_edited += letra
    else:
        main_path_edited += "/"

# First letter is changed to upper.
main_path_edited = main_path_edited.replace(main_path_edited[0], main_path_edited[0].upper(), 1)

# Main used path are linked.
image_path = main_path_edited + "/Imagenes/"
sounds_path = main_path_edited + "/Sonidos/"

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
audio_accepted_files = (("Audio Files", "*.mp3"),("Audio Files", "*.ogg"), ("Audio Files", "*.WAV"))

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

        # Set a frame at the background.
        self.frame = ctk.CTkFrame(self.root, height=500, width=350, fg_color=colors["soft_grey"])
        self.frame.pack(pady=10, padx=10, fill="both") 
        
        # Set the title and the logo of the app.
        self.title = self.root.title("RelaxApp")
        self.root.after(200, lambda: self.root.iconbitmap(image_path + "logo.ico"))
        
    # Method that creates a new root everytime the main root is destroyed.
    def close_create(self, new_window, *args):
        self.root.withdraw()
        self.root = ctk.CTkToplevel()
        app = new_window(self.root, *args)
        self.root.mainloop()


###########################################################
### Class that contains general settings of the Pop-ups ###
###########################################################

class RelaxApp_MessageBox_Structure:
    """This class defines the general structure of the pop-ups.
       Defines the dimensions, title and creates a frame."""

    def __init__(self, root):
        self.root = root

        # New pop-ups is created.
        self.window = ctk.CTkToplevel()
        self.window.grab_set()

        # Set the width, height, configuration and location of the windows.
        width = 550
        height = 150
        width_resolution = self.window.winfo_screenwidth() // 2 - width // 2 - width // 3
        height_resolution = self.window.winfo_screenheight() // 2 - height
        self.dimensions = self.window.geometry(f"{width}x{height}+{width_resolution}+{height_resolution}")
        self.maximize = self.window.resizable(False,False)

        # Set a frame at the background.
        self.frame = ctk.CTkFrame(self.window, height=200, width=550, fg_color=colors["soft_grey"])
        self.frame.pack(pady=10, padx=10, fill="both") 
        
        # Set the title and the logo of the app.
        self.title = self.window.title("RelaxApp")
        self.window.after(200, lambda: self.window.iconbitmap(image_path + "logo.ico"))


####################################################################
### Class that contains general settings of the user's main menu ###
####################################################################

class RelaxApp_User_Settings_Structure:
    """This class defines the general structure of the user's main 
       menu settings. Defines the appearance, dimensions and title."""

    def __init__(self, root):
        self.root = root

        # New pop-ups is created.
        self.window = ctk.CTkToplevel()
        self.window.grab_set()

        # Set the width, height, configuration and location of the windows.
        width = 260
        height = 300
        width_resolution = self.window.winfo_screenwidth() // 2 - width // 2 - width // 3
        height_resolution = self.window.winfo_screenheight() // 2 - height
        self.dimensions = self.window.geometry(f"{width}x{height}+{width_resolution}+{height_resolution}")
        self.maximize = self.window.resizable(False,False)

        # Set a frame at the background.
        self.frame = ctk.CTkFrame(self.window, height=300, width=260, fg_color=colors["soft_grey"])
        self.frame.pack(pady=10, padx=10, fill="both")

        # Set the title and the logo of the app.
        self.title = self.window.title("RelaxApp")
        self.window.after(200, lambda: self.window.iconbitmap(image_path + "logo.ico"))


######################################################################
### Class that contains general settings while RelaxApp is running ###
######################################################################

class RelaxApp_Running_Structure:
    """This class defines the general structure while app is running. 
       Defines the appearance, dimensions and title."""

    def __init__(self, root):
        self.root = root

        # Set the width, height, configuration and location of the windows.
        width = 280
        height = 400
        width_resolution = self.root.winfo_screenwidth() // 2 - width // 2 - width // 3
        height_resolution = self.root.winfo_screenheight() // 2 - height
        self.dimensions = self.root.geometry(f"{width}x{height}+{width_resolution}+{height_resolution}")
        self.maximize = self.root.resizable(False,False)

        # Set a frame at the background.
        self.frame = ctk.CTkFrame(self.root, height=400, width=280, fg_color=colors["soft_grey"])
        self.frame.pack(pady=10, padx=10, fill="both") 

        # Set the title and the logo of the app.
        self.title = self.root.title("RelaxApp")
        self.root.after(200, lambda: self.root.iconbitmap(image_path + "logo.ico"))


###############################################################################
### Class that is used to validate entries in the user's main menu settings ###
###############################################################################

class Validate_CMD:
    """This class is used to validate the user's personal settings entries
       in the main menu."""
 
    def validate_hours(text):
        """Funtions to validate lenght of the hours entries"""
        if len(text) == 0:
            return True
        elif text == "HH":
            return True           
        elif len(text) < 3 and text.isdigit():
            return True
        else:
            return False
  
    def validate_min_sec(text):
        """Funtions to validate lenght of the minutes and seconds entries"""
        if len(text) == 0:
            return True
        elif text == "MM" or text == "SS":
            return True
        elif len(text) < 3 and text.isdigit():
            return True
        else:
            return False
        

######################################################
### Class that contains the first frame of the App ###
######################################################

class RelaxApp_Initial_Frame(RelaxApp_Structure):
    """This class defines all buttons and options availables into
       the first frame. Inherit all structure from parent."""

    def __init__(self, root):
        super().__init__(root)
        self.root = root

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

        # "Register User" button..
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
        base_datos.verificar_login(databases["database1"], tables["users_table"], user)
        
        # ###########################################
        # #VARIABLE OCASIONAL PARA ENTRAR SIN USUARIO
        # ###########################################
        # base_datos.validacion_login = True
        if base_datos.validacion_login:
            self.close_create(RelaxApp_User_Main_Menu)

        else:
            self.error_login = ctk.CTkLabel(self.frame, text="Usuario o contraseña incorrecta. Vuelva a intentarlo.", 
                                            font=(font,11))
            self.error_login.place(rely=0.81, relx=0.5, anchor="center")
   
    # Method that register users.
    def sign_up(self):
        self.close_create(RelaxApp_User_Registration)

    # Method to change password.
    def change_password(self):
        self.close_create(RelaxApp_User_Change_Password)
   

###############################################################
###  Class that contains the window for users registrations ###
###############################################################

class RelaxApp_User_Registration(RelaxApp_Structure):
    """This class opens a new window for users registrations. 
       Inherit all structure from parent."""

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        
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
                
    def accept_sign_up(self):
        get_name = self.name_entry.get()
        get_last_name = self.last_name_entry.get()
        get_username = self.username_entry.get()
        get_password = self.password_entry.get()

        user["accion"] = "registrar"
        user["nombre"] = get_name
        user["apellido"] = get_last_name
        user["login"] = get_username
        user["password"] = get_password

        RelaxApp_MessageBox_Options(self.root, "Sign up", user)

    def cancel_sign_up (self):
        RelaxApp_MessageBox_Options(self.root, "Cancel", user)


##############################################################
###  Class that contains the window to change the password ###
##############################################################

class RelaxApp_User_Change_Password(RelaxApp_Structure):
    """This class opens a new window to change the pasword. 
       Inherit all structure from parent."""

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        
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
                
    def accept_change_pw(self):
        # Variable to compare password 1 with password 2.
        self.confirm_pw = False

        get_username_pw_menu = self.name_entry.get()
        get_password1_pw_menu = self.pw1_entry.get()
        get_password2_pw_menu = self.pw2_entry.get()

        user["accion"] = "modificar"
        user["login"] = get_username_pw_menu
        user["password"] = get_password1_pw_menu

        if user["password"] == get_password2_pw_menu:
            self.confirm_pw = True
            RelaxApp_MessageBox_Options(self.root, "Password Correct", user)
        else:
            RelaxApp_MessageBox_Options(self.root, "Password Incorrect", user)

    def cancel_change_pw (self):
        RelaxApp_MessageBox_Options(self.root, "Cancel Change PW", user)


#########################################################
###  Class that contains the user's main menu window  ###
#########################################################

class RelaxApp_User_Main_Menu(RelaxApp_Structure):
    """This class contains the user's main menu. It allows to start
       the app, set, save and load settings and knows about RelaxApp."""

    def __init__(self, root, visual_set=False, stretch_set=False):
        super().__init__(root)
        self.root = root

        self.visual_set = visual_set
        self.stretch_set = stretch_set

        # Frame at the back.
        self.frame.configure(fg_color=colors["black"])
        self.frame.pack(pady=10, padx=0, fill="both")  

        # Frame at the top that contains menu options.
        self.frame_top_menu = ctk.CTkFrame(self.frame, height=30, width=350, fg_color=colors["soft_grey"], 
                                           corner_radius=3)
        self.frame_top_menu.pack(pady=2, padx=10) 

        # Main frame that contains all user options.
        self.frame_main = ctk.CTkFrame(self.frame, height=450, width=350, fg_color=colors["soft_grey"])
        self.frame_main.pack(padx=10, fill="both")

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

        # Labels of archieve menu cascade.
        self.menu_archieve.add_command(label=" Crear Perfil  ", font=(font,9), command=self.create_profile, 
                                       background=colors["soft_grey"], foreground=colors["white"], activebackground=colors["dark_green"], 
                                       hidemargin=True)
        self.menu_archieve.add_command(label=" Exportar Perfil  ", font=(font,9), command=self.export_profile, 
                                       background=colors["soft_grey"], foreground=colors["white"], activebackground=colors["dark_green"], 
                                       hidemargin=True)
        
        # Label of help menu cascade.
        self.menu_help.add_command(label=" Conozca RelaxApp  ", font=(font,9), command=self.about_us, background=colors["soft_grey"], 
                                   foreground=colors["white"], activebackground=colors["dark_green"], hidemargin=True) 

        # Options label.
        self.options = ctk.CTkLabel(self.frame_main, text="Configurar", font=(font, 16), corner_radius=10, height=35)
        self.options.place(rely=0.3, relx=0.5, anchor="center")

        # Button to set visual options.
        self.visual_options = ctk.CTkButton(self.frame_main, text="Descanso Visual", font=(font, 14), 
                                                command=self.set_visual_options, corner_radius=10, height=35, 
                                                hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.visual_options.place(rely=0.4, relx=0.25, anchor="w")
        # Variable to save the information of "visual_options_CB" when is marked or unmarked.
        self.visual_options_choice = ctk.IntVar()
        # Checkbox to activate or deactivate "visual_options".
        self.visual_options_CB = ctk.CTkCheckBox(self.frame_main, text=None, variable=self.visual_options_choice , width=20, height=20, hover=True, 
                                                fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.visual_options_CB.place(rely=0.4, relx=0.8, anchor="e")

        # Button to set stretch options.
        self.stretch_options = ctk.CTkButton(self.frame_main, text="Estirar", font=(font, 14), 
                                                command=self.set_stretch_options, corner_radius=10, height=35, 
                                                hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.stretch_options.place(rely=0.5, relx=0.25, anchor="w")
        # Variable to save the information of "stretch_options_CB" when is marked or unmarked.
        self.stretch_options_choice = ctk.IntVar()
        # Checkbox to activate or deactivate "stretch_options".
        self.stretch_options_CB = ctk.CTkCheckBox(self.frame_main, text=None, variable=self.stretch_options_choice, width=20, height=20, hover=True, 
                                                fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.stretch_options_CB.place(rely=0.5, relx=0.8, anchor="e")

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


    ###################################################################
    ###### TO SET ######
    def create_profile(self):
        RelaxApp_User_Main_Menu_Profiles(self.root, user["login"])
  
    # Function to save both visual and stretch setting of the user.
    def export_profile(self):
        try:
            save_file = ctk.filedialog.asksaveasfile(title="Exportar Perfil")

            # Query method is called to get the time when profile was saved.
            base_datos.consulta(f"SELECT Nombre_Perfil FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}'")
            
            if base_datos.valor[0][0] != None:
                file_profile_name_get = base_datos.valor[0][0]
            else:
                file_profile_name_get = ""

            # Query method is called to get the time when profile was saved.
            base_datos.consulta(f"SELECT Fecha_Hora FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}'")
            if base_datos.valor[0][0] != None:
                file_datetime_get = base_datos.valor[0][0]
            else:
                file_datetime_get = ""

            # Query method is called to get user's visual options settings.
            base_datos.consulta(f"SELECT Configuracion_Visual FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}'")
            if base_datos.valor[0][0] != None:
                file_data_get_VO = base_datos.valor[0][0]
            else:
                file_data_get_VO = ""

            # Query method is called to get user's stretch options settings.
            base_datos.consulta(f"SELECT Configuracion_Estirar FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}'")
            if base_datos.valor[0][0] != None:
                file_data_get_SO = base_datos.valor[0][0]
            else:
                file_data_get_SO = ""

            # Query method is called to get user's final sound settings.
            base_datos.consulta(f"SELECT Configuracion_Sonidos_Final FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}'")
            if base_datos.valor[0][0] != None:
                file_data_get_FS = base_datos.valor[0][0]
            else:
                file_data_get_FS = ""

            # Query method is called to get user's final sound settings.
            base_datos.consulta(f"SELECT Configuracion_Sonidos_Lapse FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}'")
            if base_datos.valor[0][0] != None:
                file_data_get_LS = base_datos.valor[0][0]
            else:
                file_data_get_LS = ""

            # Both settings are concatenated in one line.
            file_to_save = file_profile_name_get + "\n" + file_datetime_get + "\n" + file_data_get_VO + "\n" + file_data_get_SO + "\n" + file_data_get_FS + "\n" + file_data_get_LS
            # File is saved.
            save_file.write(file_to_save)
        except:
            pass

    ###### TO SET ######
    def about_us(self):
        ###### TO SET ######
        print("about_us EN DESARROLLO")
        ###### TO SET ######

    # Function to sign out of the App.
    def sign_out(self):
        RelaxApp_MessageBox_Options(self.root, "Sign Out", user["login"])

    # Function to set visual options of the App.
    def set_visual_options(self):
        self.visual_options_values = True
        RelaxApp_User_Main_Menu_Settings(self.root, self.visual_options_values)

    # Function to set stretch options of the App.
    def set_stretch_options(self):
        self.stretch_options_values = True
        RelaxApp_User_Main_Menu_Settings(self.root, None, self.stretch_options_values)

    def set_sounds_options(self):
        RelaxApp_User_Main_Menu_Sounds(self.root)

    # Function to start App.
    def start_relaxapp(self):
        # Get if "self.visual_options_CB" is checked.
        if self.visual_options_choice.get() == 1:
            self.visual_set = True
        else:
            self.visual_set = False
        
        # Get if "self.stretch_options_CB" is checked.
        if self.stretch_options_choice.get() == 1:
            self.stretch_set = True
        else:
            self.stretch_set = False

        if self.visual_set == False and self.stretch_set == False:
            RelaxApp_MessageBox_Options(self.root, "No Settings")
        else:  
            self.close_create(RelaxApp_Running, self.visual_set, self.stretch_set)  


#######################################################
###  Class that is showed when RelaxApp is running  ###
#######################################################

class RelaxApp_Running(RelaxApp_Running_Structure):
    """This class start RelaxApp. All countdown are executed depending on previus
       values choosen. Inherit all structure from parent."""
    
    def __init__(self, root, visual_set, stretch_set):
        super().__init__(root)

        self.root = root

        pygame.mixer.init()

        # Variables to set which threading is started.
        self.visual_set = visual_set
        self.stretch_set = stretch_set
        
        # Variable to stop bucles when return button is used after countdown is finished.
        self.app_running = True
        # Variables to stop bucles when function TR_VO_countdown or TR_SO_countdown are finished.
        self.stop_countdown_VO = False
        self.stop_countdown_SO = False

        # Query method is called to get user's visual options settings.
        self.get_values_VO = base_datos.consulta(f"SELECT Configuracion_Visual FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}'")
        base_datos.valor = base_datos.valor[0][0]

        # Dictionary that contains each value of user's visual options settings.
        self.values_VO = {"time_left_HH" : base_datos.valor[0:2],
                          "time_left_MM" : base_datos.valor[2:4],
                          "next_alert_MM" : base_datos.valor[4:6],
                          "breaktime_MM" : base_datos.valor[6:8],
                          "breaktime_SS" : base_datos.valor[8:10],
                          "sound_active" : base_datos.valor[10::]}
        
        # Query method is called to get user's stretch options settings.
        self.get_values_SO = base_datos.consulta(f"SELECT Configuracion_Estirar FROM {databases['database1']}.{tables['settings_table']} WHERE login = '{user['login']}'")
        base_datos.valor = base_datos.valor[0][0]
        
        # Dictionary that contains each value of user's stretch options settings.
        self.values_SO = {"time_left_HH" : base_datos.valor[0:2],
                          "time_left_MM" : base_datos.valor[2:4],
                          "next_alert_MM" : base_datos.valor[4:6],
                          "breaktime_MM" : base_datos.valor[6:8],
                          "breaktime_SS" : base_datos.valor[8:10],
                          "sound_active" : base_datos.valor[10::]}

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
            self.frame_visual = ctk.CTkFrame(self.frame, height=100, width=250, fg_color=colors["black"], 
                                                corner_radius=10)
            self.frame_visual.place(rely=self.frame_visual_rely, relx=0.5, anchor="center")

            # Main title of the frame.
            self.visual_title = ctk.CTkLabel(self.frame, text="Descanso Visual", font=(font, 16))
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
            self.frame_stretch = ctk.CTkFrame(self.frame, height=100, width=250, fg_color=colors["black"], 
                                                corner_radius=10)
            self.frame_stretch.place(rely=self.frame_stretch_rely, relx=0.5, anchor="center")

            # Main title of the frame.
            self.stretch_title = ctk.CTkLabel(self.frame, text="Estirar", font=(font, 16))
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
        self.start = ctk.CTkButton(self.root, text=None, command=self.threading(), hover=False, fg_color=colors["soft_grey"],
                                   bg_color=colors["soft_grey"])                        
        self.start.place(rely=0.9, relx=0.5, anchor="center")

        # Button that returns to the user's main menu.
        self.stop = ctk.CTkButton(self.root, text="Volver", font=(font, 20), command=self.stop_app, width=100, height=20, 
                                  corner_radius=90, hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"],
                                  bg_color=colors["soft_grey"])
        self.stop.place(rely=0.85, relx=0.5, anchor="center")

    # Function that call 4 of the 6 countdown.
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

    # Function to start the main countdown "Time Remaining" of the visual options.
    def TR_VO_countdown(self):
        # Variable to be used to sinchronize countdowns between Time Remaining and both Next Alert and Break Time.
        contador = 0
        # Hours and minutes of time remaining are gotten.
        TR_HH_valor = int(self.time_left_HH_VO.get())
        TR_MM_valor = int(self.time_left_MM_VO.get())

        while True:
            # This variable change when return button is pressed to stop or not the app.
            if self.app_running == False:
                self.stop_countdown_VO = True
                break              
            else:
                # Timer are sinchronized.
                self.root.after(30 + contador)
                # Verify if values have one or two digits in order to add a "0" in front.
                if TR_MM_valor > 9:
                    self.time_left_MM_VO.set(TR_MM_valor)
                else:
                    self.time_left_MM_VO.set("0" + str(TR_MM_valor))
                if TR_HH_valor > 9:
                    self.time_left_HH_VO.set(TR_HH_valor)
                else:
                    self.time_left_HH_VO.set("0" + str(TR_HH_valor))
 
                time.sleep(60)
                contador += 2
                # After 1 minute one is subtracted from the minutes.
                if TR_MM_valor > 0:
                    TR_MM_valor -=1
                # When minute is cero one is subtracted from the hours.
                elif TR_HH_valor > 0:     
                    TR_HH_valor -=1
                    TR_MM_valor = 59
                else:
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

    # Function to start the countdown "Next Alert" of the visual options.
    def NA_VO_countdown(self):
        
        # Minutes and seconds of next alert are gotten.
        initial_value_MM = self.next_alert_MM_VO.get()
        initial_value_SS = self.next_alert_SS_VO.get()

        NA_MM_valor = int(initial_value_MM)
        NA_SS_valor = int(initial_value_SS)
        
        while NA_MM_valor > -1:
            # Conditional that stop bucle when time remaining is finished.
            if self.stop_countdown_VO == True:
                break
            # Verify if values have one or two digits in order to add a "0" in front.
            elif NA_SS_valor > 9:
                self.next_alert_SS_VO.set(NA_SS_valor)
            else:
                self.next_alert_SS_VO.set("0" + str(NA_SS_valor))
            if NA_MM_valor > 9:
                self.next_alert_MM_VO.set(NA_MM_valor)
            else:
                self.next_alert_MM_VO.set("0" + str(NA_MM_valor))

            # After 1 second one is subtracted from the seconds.
            if NA_SS_valor > 0:
                NA_SS_valor -=1
                time.sleep(1)
            # When second is cero one is subtracted from the minutes.
            elif NA_MM_valor > 0:
                NA_MM_valor -= 1
                NA_SS_valor = 59
                time.sleep(1)
            else:
                # Sound alert is called.
                if self.sound_VO == "True":
                    self.play_sounds(2)
                # Minutos and second are set as there was at the beggining.
                self.next_alert_SS_VO.set(initial_value_SS)
                self.next_alert_MM_VO.set(initial_value_MM)
                # New threading is run to start BT_VO_countdown function.
                threading.Thread(target=self.BT_VO_countdown).start()
                break

    # Function to start the countdown "Break Time" of the visual options.
    def BT_VO_countdown(self):
        
        # Minutes and seconds of next alert are gotten.
        initial_value_MM = self.breaktime_MM_VO.get()
        initial_value_SS = self.breaktime_SS_VO.get()

        BT_MM_valor = int(initial_value_MM)
        BT_SS_valor = int(initial_value_SS)

        while BT_MM_valor > -1:
            # Conditional that stop bucle when time remaining is finished.
            if self.stop_countdown_VO == True:
                break
            # Verify if values have one or two digits in order to add a "0" in front.
            if BT_MM_valor > 9:
                self.breaktime_MM_VO.set(BT_MM_valor)
            else:
                self.breaktime_MM_VO.set("0" + str(BT_MM_valor))
            if BT_SS_valor > 9:
                self.breaktime_SS_VO.set(BT_SS_valor)
            else:
                self.breaktime_SS_VO.set("0" + str(BT_SS_valor))

            # After 1 second one is subtracted from the seconds.
            if BT_SS_valor > 0:
                BT_SS_valor -=1
                time.sleep(1)
            # When second is cero one is subtracted from the minutes.
            elif BT_MM_valor > 0:     
                BT_MM_valor -=1
                BT_SS_valor = 59
                time.sleep(1)
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

    # Function to start the main countdown "Time Remaining" of the stretch options.
    def TR_SO_countdown(self):
        contador = 0
        TR_HH_valor = int(self.time_left_HH_SO.get())
        TR_MM_valor = int(self.time_left_MM_SO.get())

        while True:
            if self.app_running == False:
                self.stop_countdown_SO = True
                break
            else:
                self.root.after(30 + contador)

                if TR_MM_valor > 9:
                    self.time_left_MM_SO.set(TR_MM_valor)
                else:
                    self.time_left_MM_SO.set("0" + str(TR_MM_valor))
                if TR_HH_valor > 9:
                    self.time_left_HH_SO.set(TR_HH_valor)
                else:
                    self.time_left_HH_SO.set("0" + str(TR_HH_valor))

                time.sleep(60)
                contador += 2
                if TR_MM_valor > 0:
                    TR_MM_valor -=1
                elif TR_HH_valor > 0:     
                    TR_HH_valor -=1
                    TR_MM_valor = 59
                else:
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
            
    # Function to start the countdown "Next Alert" of the stretch options.
    def NA_SO_countdown(self):

        initial_value_MM = self.next_alert_MM_SO.get()
        initial_value_SS = self.next_alert_SS_SO.get()
        
        NA_MM_valor = int(initial_value_MM)
        NA_SS_valor = int(initial_value_SS)

        while NA_MM_valor > -1:
            if self.stop_countdown_SO == True:
                break

            elif NA_SS_valor > 9:
                self.next_alert_SS_SO.set(NA_SS_valor)
            else:
                self.next_alert_SS_SO.set("0" + str(NA_SS_valor))         
            if NA_MM_valor > 9:
                self.next_alert_MM_SO.set(NA_MM_valor)
            else:
                self.next_alert_MM_SO.set("0" + str(NA_MM_valor))

            if NA_SS_valor > 0:
                NA_SS_valor -=1
                time.sleep(1)
            elif NA_MM_valor > 0:
                NA_MM_valor -= 1
                NA_SS_valor = 59
                time.sleep(1)
            else:
                if self.sound_SO == "True":
                    self.play_sounds(2)
                self.next_alert_SS_SO.set(initial_value_SS)
                self.next_alert_MM_SO.set(initial_value_MM)
                threading.Thread(target=self.BT_SO_countdown).start()
                break

    # Function to start the countdown "Break Time" of the stretch options.
    def BT_SO_countdown(self):

        initial_value_MM = self.breaktime_MM_SO.get()
        initial_value_SS = self.breaktime_SS_SO.get()

        BT_MM_valor = int(initial_value_MM)
        BT_SS_valor = int(initial_value_SS)

        while BT_MM_valor > -1:
            if self.stop_countdown_SO == True:
                break

            if BT_SS_valor > 9:
                self.breaktime_SS_SO.set(BT_SS_valor)
            else:
                self.breaktime_SS_SO.set("0" + str(BT_SS_valor))
            if BT_MM_valor > 9:
                self.breaktime_MM_SO.set(BT_MM_valor)
            else:
                self.breaktime_MM_SO.set("0" + str(BT_MM_valor))

            if BT_SS_valor > 0:
                BT_SS_valor -=1
                time.sleep(1)
            elif BT_MM_valor > 0:
                BT_MM_valor -=1
                BT_SS_valor = 59
                time.sleep(1)
            else:
                if self.sound_SO == "True":
                    self.play_sounds(2)
                self.breaktime_SS_SO.set(initial_value_SS)
                self.breaktime_MM_SO.set(initial_value_MM)
                threading.Thread(target=self.NA_SO_countdown).start()
                break

    # Function to stop the app when return button is pressed.
    def stop_app(self):
        # Variable to stop all bucles running.
        self.app_running = False
        # Method is called to stop the sound alert.
        pygame.mixer.quit()
        RelaxApp_Structure.close_create(self, RelaxApp_User_Main_Menu, False, False)

    # Function to run sounds alerts.
    def play_sounds(self, value):
        # When value is "1" the sound related to "Time Remaining" is set.
        if value == 1:
            pygame.mixer.music.load(sounds_path + "Final.mp3")  
            pygame.mixer.music.play(loops=0)
        # When value is "2" the sound related to "Lapse" is set.
        elif value == 2:
            pygame.mixer.music.load(sounds_path + "Lapse.mp3")  
            pygame.mixer.music.play(loops=0)
        

##########################################################
###  Class that contains the user's personal settings  ###
##########################################################

class RelaxApp_User_Main_Menu_Profiles(RelaxApp_User_Settings_Structure):
    """This class opens a new window to set the user's personal profiles 
       of the App. Inherit all structure from parent."""
    
    def __init__(self, root, user):
        super().__init__(root)
        self.root = root
        self.user = user

#         # An empty string which is going to save all values when user save a configuration.
#         # self.final_sound = ""
#         # self.lapse_sound = ""

        # Frame at the back.
        self.frame.configure(fg_color=colors["black"])
        self.frame.pack(pady=0, padx=0, fill="both")  

        # Frame that contains the alert configuration label.
        self.frame1 = ctk.CTkFrame(self.frame, height=50, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame1.pack(pady=10, padx=10)

        # Frame that contains the lenght configuration label.
        self.frame2 = ctk.CTkFrame(self.frame, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame2.pack(pady=1, padx=10)

        # Frame that contains the lapse configuration label.
        self.frame3 = ctk.CTkFrame(self.frame, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame3.pack(pady=1, padx=10)

        # Frame that contains the break time configuration label.
        self.frame4 = ctk.CTkFrame(self.frame, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame4.pack(pady=1, padx=10)

        # Frame that contains the sound configuration checkbox.
        self.frame5 = ctk.CTkFrame(self.frame, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame5.pack(pady=1, padx=10)

        # Frame that contains the save and cancel buttons.
        self.frame6 = ctk.CTkFrame(self.frame, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame6.pack(pady=10, padx=10)

        # Alert configuration label.
        self.setting_title = ctk.CTkLabel(self.frame1, text="Perfiles Configurados", font=(font, 15), 
                                          corner_radius=5, fg_color=colors["soft_green"])
        self.setting_title.place(rely=0.5, relx=0.5, anchor="center")

#         # Image of a open simbol.
        self.open_button = ctk.CTkImage(Image.open(image_path + "Abrir.png"))

        # Image of a remove simbol.
        self.remove_button = ctk.CTkImage(Image.open(image_path + "Borrar.png"))

        # # Sound by default label.
        # self.sound_alert_D1 = ctk.CTkLabel(self.frame2, text="Test", font=(font, 14))
        # self.sound_alert_D1.place(rely=0.5, relx=0.03, anchor="w")

        # Button to create new profile.
        self.create_profile_button = ctk.CTkButton(self.frame2, text=None, image=self.open_button, width=0, command=self.create_profile,
                                                hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.create_profile_button.place(rely=0.5, relx=0.25, anchor="w")

        # Button to remove profile selected.
        self.remove_profile_button = ctk.CTkButton(self.frame2, text=None, image=self.remove_button, width=0, command=self.remove_profile,
                                                hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.remove_profile_button.place(rely=0.5, relx=0.75, anchor="e")

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

    def create_profile(self):
        pass

    def load_prifile(self):
        pass

    def remove_profile(self):
        pass
    
    def profile_name(self):
        pass

    def save_settings(self):
        self.window.destroy()

    def cancel_settings(self):
        self.window.destroy()


##########################################################
###  Class that contains the user's personal settings  ###
##########################################################

class RelaxApp_User_Main_Menu_Settings(RelaxApp_User_Settings_Structure):
    """This class opens a new window to set the user's personal settings 
       of the App. Inherit all structure from parent."""
    
    def __init__(self, root, visual_values=None, stretch_values=None):
        super().__init__(root)
        self.root = root
        
        self.visual_options_values = visual_values
        self.stretch_options_values = stretch_values

        # An empty string which is going to save all values when user save a configuration.
        self.values = ""

        # Frame at the back.
        self.frame.configure(fg_color=colors["black"])
        self.frame.pack(pady=0, padx=0, fill="both")  

        # Frame that contains the alert configuration label.
        self.frame1 = ctk.CTkFrame(self.frame, height=50, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame1.pack(pady=10, padx=10)

        # Frame that contains the lenght configuration label.
        self.frame2 = ctk.CTkFrame(self.frame, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame2.pack(pady=1, padx=10)

        # Frame that contains the lapse configuration label.
        self.frame3 = ctk.CTkFrame(self.frame, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame3.pack(pady=1, padx=10)

        # Frame that contains the break time configuration label.
        self.frame4 = ctk.CTkFrame(self.frame, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame4.pack(pady=1, padx=10)

        # Frame that contains the sound configuration checkbox.
        self.frame5 = ctk.CTkFrame(self.frame, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame5.pack(pady=1, padx=10)

        # Frame that contains the save and cancel buttons.
        self.frame6 = ctk.CTkFrame(self.frame, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
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

    # Funtions to save settings in the user's main menu.
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
        
        # Verify if all entries are filled.
        if lenght_HH == "HH" or lenght_MM == "MM" or \
        lapse == "MM" or break_time_MM == "MM" or \
        break_time_SS == "SS":
            # Pop-ups a message box if any entry is unfilled.
            RelaxApp_MessageBox_Options(self.root, "Empty")

        # Verify if lenght entry is not higher than 16hs.
        elif int(lenght_HH) * 60 + int(lenght_MM) > 960:
            RelaxApp_MessageBox_Options(self.root, "Extra Hours")
        # Verify if the rest of the entries are not higher than 60.
        elif int(lenght_MM) > 60 or int(lapse) > 60 or  \
        int(break_time_SS) > 60:
            RelaxApp_MessageBox_Options(self.root, "Invalid Time")
        elif len(lenght_HH) == 1 or len(lenght_MM) == 1 or \
        len(lapse) == 1 or len(break_time_MM) == 1 or \
        len(break_time_SS) == 1:
            RelaxApp_MessageBox_Options(self.root, "One Value")
        elif int(break_time_MM) * 60 + int(break_time_SS) > \
        int(lapse) * 60:
            RelaxApp_MessageBox_Options(self.root, "Over Lapse")
        elif int(lapse) == 0:
            RelaxApp_MessageBox_Options(self.root, "No Lapse")
        elif int(break_time_MM) == 0 and int(break_time_SS) < 30:
            RelaxApp_MessageBox_Options(self.root, "No Break")
        
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

            # Varible "self.values" is saved in the database inside the "Configuracion_visual" column.
            if self.visual_options_values == True:
                base_datos.configuraciones_usuario(databases["database1"], tables["settings_table"], 
                                                   user["login"], "Configuracion_visual", self.values)

            # Varible "self.values" is saved in the database inside the "Configuracion_estirar" column.    
            elif self.stretch_options_values == True:
                base_datos.configuraciones_usuario(databases["database1"], tables["settings_table"], 
                                                   user["login"], "Configuracion_estirar", self.values)

            self.window.destroy()
        
    def cancel_settings(self):
        self.window.destroy()


##########################################################
###  Class that contains the user's personal settings  ###
##########################################################

class RelaxApp_User_Main_Menu_Sounds(RelaxApp_User_Settings_Structure):
    """This class opens a new window to set the user's personal sounds 
       of the App. Inherit all structure from parent."""
    
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        # An empty string which is going to save all values when user save a configuration.
        self.final_sound = ""
        self.lapse_sound = ""

        # Frame at the back.
        self.frame.configure(fg_color=colors["black"])
        self.frame.pack(pady=0, padx=0, fill="both")  

        # Frame that contains the alert configuration label.
        self.frame1 = ctk.CTkFrame(self.frame, height=50, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame1.pack(pady=10, padx=10)

        # Frame that contains the lenght configuration label.
        self.frame2 = ctk.CTkFrame(self.frame, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame2.pack(pady=1, padx=10)

        # Frame that contains the lapse configuration label.
        self.frame3 = ctk.CTkFrame(self.frame, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame3.pack(pady=1, padx=10)

        # Frame that contains the break time configuration label.
        self.frame4 = ctk.CTkFrame(self.frame, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame4.pack(pady=1, padx=10)

        # Frame that contains the sound configuration checkbox.
        self.frame5 = ctk.CTkFrame(self.frame, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame5.pack(pady=1, padx=10)

        # Frame that contains the save and cancel buttons.
        self.frame6 = ctk.CTkFrame(self.frame, height=40, width=250, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame6.pack(pady=10, padx=10)

        # Alert configuration label.
        self.setting_title = ctk.CTkLabel(self.frame1, text="Configurar Sonidos", font=(font, 15), 
                                          corner_radius=5, fg_color=colors["soft_green"])
        self.setting_title.place(rely=0.5, relx=0.5, anchor="center")

        # Image of a play simbol.
        self.play_button_image = ctk.CTkImage(Image.open(image_path + "Play.png").resize((40,40)))

        # Image of a play simbol.
        self.pause_button_image = ctk.CTkImage(Image.open(image_path + "Pause.png").resize((40,40)))

        # Sound by default label.
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

    # Funtion to run and stop defaults sounds.
    def sound_default(self, action, sound):
        pygame.mixer.init()
        if action == "Play":
            if sound == "Final":
                pygame.mixer.music.load(sounds_path + "Final.mp3")
            elif sound == "Lapse":
                pygame.mixer.music.load(sounds_path + "Lapse.mp3")
            pygame.mixer.music.play(loops=0)
        elif action == "Pause":
            pygame.mixer.quit()

    # Funtion to load sounds.
    def sound_load(self, value):
        if value == "1":
            self.sound_loaded1_path = ctk.filedialog.askopenfilename(title="Cargar Sonido Final", filetypes=audio_accepted_files)
        elif value == "2":
            self.sound_loaded2_path = ctk.filedialog.askopenfilename(title="Cargar Sonido Alerta", filetypes=audio_accepted_files)

    # Funtion to run and stop loaded sounds.
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

    def save_settings(self):
        try:
            # Final sound is choosen.
            if self.sound_alert_choice1.get() == 0:
                self.final_sound = sounds_path + "Final.mp3"
            elif self.sound_alert_choice1.get() == 1:
                self.final_sound = sounds_path + "Lapse.mp3"
            elif self.sound_alert_choice1.get() == 2:
                self.final_sound = self.sound_loaded1_path
            elif self.sound_alert_choice1.get() == 3:
                self.final_sound = self.sound_loaded2_path
        except:
            self.final_sound = ""

        try:
            # Lapse sound is choosen.
            if self.sound_alert_choice2.get() == 0:
                self.lapse_sound = sounds_path + "Final.mp3"
            elif self.sound_alert_choice2.get() == 1:
                self.lapse_sound = sounds_path + "Lapse.mp3"
            elif self.sound_alert_choice2.get() == 2:
                self.lapse_sound = self.sound_loaded1_path
            elif self.sound_alert_choice2.get() == 3:
                self.lapse_sound = self.sound_loaded2_path
        except:
            self.lapse_sound = ""

        # MessageBox is called when user try to save a configuration with a loaded sound before loading.
        if self.final_sound == "" or self.lapse_sound == "":
            RelaxApp_MessageBox_Options(self.root, "No Sound")
        else:
            # Varible "self.final_sound" is saved in the database inside the "Configuracion_Sonidos_Final" column.
            base_datos.configuraciones_usuario(databases["database1"], tables["settings_table"], 
                                            user["login"], "Configuracion_Sonidos_Final", self.final_sound)
            
            # Varible "self.lapse_sound" is saved in the database inside the "Configuracion_Sonidos_Lapse" column.
            base_datos.configuraciones_usuario(databases["database1"], tables["settings_table"], 
                                            user["login"], "Configuracion_Sonidos_Lapse", self.lapse_sound)
            
            self.window.destroy()

    def cancel_settings(self):
        self.window.destroy()

    # Function that show information about how to use the sound settings.
    def show_info(self ,text):
        self.text = text
        ctk.CTkLabel(self.root, text=f' "{self.text}" ', font=("Segoe Print", 22),
        fg_color=colors["soft_grey"]).pack()


####################################################
###  Class that contains all pop-ups of the App  ###
####################################################

class RelaxApp_MessageBox_Options(RelaxApp_MessageBox_Structure):
    """This class defines all pop-ups of the App.
       Inherit all structure from parent."""
    
    def __init__(self, root, message, user=None):
        super().__init__(root)
        self.root = root
        self.message = message
        self.user = user
        # Variable to set when the button "Accept", "Cancel" is activated
        self.select_button1 = False
        # Variable to set when the button "Continue" is activated
        self.select_button2 = False
        # Variable to set when the button "Return" is activated
        self.select_button3 = False

        if message == "Sign up":
            # Label ask/cancel user registration.
            self.ask_cancel_label = ctk.CTkLabel(self.window, text="¿Está seguro que desea dar de alta el usuario indicado?", 
                                                 font=(font,14), bg_color=colors["soft_grey"])
            self.ask_cancel_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Cancel":
            # Label ask/cancel to cancel user registration.
            self.ask_cancel_label = ctk.CTkLabel(self.window, text="¿Está seguro que desea cancelar el alta del usuario indicado?", 
                                                 font=(font,14), bg_color=colors["soft_grey"])
            self.ask_cancel_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Continue":
            # Label confirm user registration.
            self.continue_registration = ctk.CTkLabel(self.window, text=base_datos.mensaje, font=(font,14), 
                                                      bg_color=colors["soft_grey"])
            self.continue_registration.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button2 = True

        elif message == "Error":
            # Label confirm user registration.
            self.continue_registration = ctk.CTkLabel(self.window, text=base_datos.mensaje, font=(font,14), 
                                                      bg_color=colors["soft_grey"])
            self.continue_registration.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button3 = True

        elif message == "Password Correct":
            # Label to confirm or not to change the password.
            self.pw_match = ctk.CTkLabel(self.window, text="¿Está seguro que desea actualizar su contraseña?", 
                                         font=(font,14), bg_color=colors["soft_grey"])
            self.pw_match.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Password Incorrect":
            # Label to inform that the password 1 does not match with password 2.
            self.pw_unmatch = ctk.CTkLabel(self.window, text="Las contraseñas introducidas no coinciden entre sí. \nVuelva a introducirlas.", 
                                           font=(font,14), bg_color=colors["soft_grey"])
            self.pw_unmatch.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Cancel Change PW":
            # Label ask/cancel to cancel to change password.
            self.pw_ask_cancel_label = ctk.CTkLabel(self.window, text="¿Está seguro que desea cancelar el cambio de contraseña?", 
                                                    font=(font,14), bg_color=colors["soft_grey"])
            self.pw_ask_cancel_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Sign Out":
            # Label ask/cancel to sign out.
            self.pw_ask_cancel_label = ctk.CTkLabel(self.window, text=f"¿Está seguro que desea cerrar la sesión de '{self.user}'?", 
                                                    font=(font,14), bg_color=colors["soft_grey"])
            self.pw_ask_cancel_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Empty":
            # Label to alert not to leave entries unfilled.
            self.empty_entry_label = ctk.CTkLabel(self.window, text="Debes configurar todos los campos antes de guardalos.", 
                                                  font=(font,14), bg_color=colors["soft_grey"])
            self.empty_entry_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button3 = True

        elif message == "Extra Hours":
            # Label to alert not to work extra hours.
            self.extra_hours_label = ctk.CTkLabel(self.window, text="No puedes configurar mas de 16hs. Recuerda que mínimo \ndebes dormir 8hs.", 
                                                  font=(font,14), bg_color=colors["soft_grey"])
            self.extra_hours_label.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button3 = True
        
        elif message == "Invalid Time":
            # Label to alert not to set over 60 minutes or seconds.
            self.invalid_time_label = ctk.CTkLabel(self.window, text="Los minutos o los segundos no deben ser mayores a 60.", 
                                                   font=(font,14), bg_color=colors["soft_grey"])
            self.invalid_time_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button3 = True

        elif message == "One Value":
            # Label to alert not to set one value.
            self.one_value_label = ctk.CTkLabel(self.window, text="Cada campo a configurar debe tener 2 valores.", 
                                                font=(font,14), bg_color=colors["soft_grey"])
            self.one_value_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button3 = True

        elif message == "Over Lapse":
            # Label to alert not to set breaktime over lapse time.
            self.over_lapse_label = ctk.CTkLabel(self.window, text="El tiempo de descanso no puede ser superior al intervalo \nde alertas configurado.", 
                                                 font=(font,14), bg_color=colors["soft_grey"])
            self.over_lapse_label.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button3 = True
        
        elif message == "No Lapse":
            # Label to alert to set at least 1 minute between alerts.
            self.no_lapse_label = ctk.CTkLabel(self.window, text="El tiempo de intervalo entre alertas debe tener al menos 1 minuto.", 
                                               font=(font,14), bg_color=colors["soft_grey"])
            self.no_lapse_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button3 = True
        
        elif message == "No Break":
            # Label to alert to set at least 1 minute between alerts.
            self.no_break_label = ctk.CTkLabel(self.window, text="El tiempo de descanso debe tener al menos 30 segundos.", 
                                               font=(font,14), bg_color=colors["soft_grey"])
            self.no_break_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button3 = True

        elif message == "No Settings":
            # Label to alert to set at least one value (Visual or Stretch Break) to start the App.
            self.no_settings_label = ctk.CTkLabel(self.window, text="Debes seleccionar al menos una opción antes de iniciar la aplicación.", 
                                                  font=(font,14), bg_color=colors["soft_grey"])
            self.no_settings_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button3 = True

        elif message == "No Sound":
            # Label to alert that a load sounds is trying to save but no file is loaded.
            self.no_sound_label = ctk.CTkLabel(self.window, text="No puedes guardar una configuración con un sonido propio \nsin cargarlo previamente.", 
                                               font=(font,14), bg_color=colors["soft_grey"])
            self.no_sound_label.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button3 = True
            

        if self.select_button1 == True:
            # Button to accept user registration.
            self.accept_ask_cancel_button = ctk.CTkButton(self.window, width=80, height=17, text="Aceptar", font=(font,14), 
                                                          command=lambda: self.accept_button(message), corner_radius=10,
                                                          hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"], 
                                                          bg_color=colors["soft_grey"])
            self.accept_ask_cancel_button.place(rely=0.65, relx=0.25, anchor="w")

            # Button to cancel user registration.
            self.cancel_ask_cancel_button = ctk.CTkButton(self.window, width=80, height=17, text="Cancelar", font=(font,14), 
                                                          command=self.cancel_button, corner_radius=10, hover=True, 
                                                          fg_color=colors["soft_green"], hover_color=colors["dark_green"],
                                                          bg_color=colors["soft_grey"])
            self.cancel_ask_cancel_button.place(rely=0.65, relx=0.75, anchor="e")

        if self.select_button2 == True:
            # Button to continue to the main menu.
            self.continue_registration_button = ctk.CTkButton(self.window, width=80, height=17, text="Continuar", font=(font,14), 
                                                              command=self.continue_button, corner_radius=10, hover=True, 
                                                              fg_color=colors["soft_green"], hover_color=colors["dark_green"],
                                                              bg_color=colors["soft_grey"])
            self.continue_registration_button.place(rely=0.65, relx=0.5, anchor="center")

        if self.select_button3 == True:
            # Button to continue to the main menu.
            self.continue_registration_button = ctk.CTkButton(self.window, width=80, height=17, text="Volver", font=(font,14), 
                                                              command=self.return_button, corner_radius=10, hover=True,
                                                              fg_color=colors["soft_green"], hover_color=colors["dark_green"],
                                                              bg_color=colors["soft_grey"])
            self.continue_registration_button.place(rely=0.65, relx=0.5, anchor="center")

    # Accept button to accept registration or accept cancelation
    def accept_button(self, message):
        if message == "Sign up":
            # App connects with the database to check if the information is valid or not.
            base_datos.editar_tabla(databases["database1"], tables["users_table"], self.user)
        elif message == "Password Correct":
             # App connects with the database to check if the information is valid or not. 
            base_datos.editar_tabla(databases["database1"], tables["users_table"], self.user)

        # User registration is canceled and turn back to main menu.
        elif message == "Cancel" or message == "Cancel Change PW" or message == "Sign Out":
            self.window.destroy()
            RelaxApp_Structure.close_create(self, RelaxApp_Initial_Frame)

        # User is registered.
        if base_datos.validacion_editar == True:
            # Registration pop-up window is closed.
            self.window.destroy()
            # "Continue" label is created.
            RelaxApp_MessageBox_Options(self.root, "Continue", user)
        
        # User is not registered.
        else:
            # Registration pop-up window is closed.
            self.window.destroy()
            # "Error" label is created.
            RelaxApp_MessageBox_Options(self.root, "Error", user)
 
    # Cancel button to accept cancelation or cancel cancelation.    
    def cancel_button(self):
        self.window.destroy()

    def continue_button(self):
        self.window.destroy()
        RelaxApp_Structure.close_create(self, RelaxApp_Initial_Frame)

    def return_button(self):
        self.window.destroy()
