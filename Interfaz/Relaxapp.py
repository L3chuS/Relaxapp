import tkinter as tk
import customtkinter as ctk
import Base_Datos.base_datos as bd
from Base_Datos.valores_presets import usuario as user
from os import path
import ctypes

# Connect to the database.
base_datos = bd.BaseDatos(**bd.acceso_root)

# Get the windows resolution regardless of rescaling
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

# Get the parent folder path and the image folder path.
main_path = path.dirname(__file__)
image_path = main_path + "/Imagenes/"

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
        self.icon = self.root.iconbitmap(image_path + "logo.ico")
        
    # Method that creates a new root everytime the main root is destroyed.
    def close_create(self, new_window):
        self.root = ctk.CTk()
        app = new_window(self.root)
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
        self.frame = ctk.CTkFrame(self.window, height=300, width=250, fg_color=colors["soft_grey"])
        self.frame.pack(pady=10, padx=10, fill="both") 

        # Set the title and the logo of the app.
        self.title = self.window.title("RelaxApp")
        self.window.after(200, lambda: self.window.iconbitmap(image_path + "logo.ico"))


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
        self.entry_user.bind("<Button-1>", lambda borrar: self.entry_user.delete(0, tk.END))

        # Password label.
        self.password = ctk.CTkLabel(self.frame, text="Contraseña", font=(font,19))
        self.password.place(rely=0.54, relx=0.5, anchor="center")

        # Password entry.
        self.entry_password = ctk.CTkEntry(self.frame,font=(font,15), corner_radius=10, show="*")
        self.entry_password.place(rely=0.61, relx=0.5, anchor="center",)
        self.entry_password.insert(0, "**********")
        self.entry_password.bind("<Button-1>", lambda borrar: self.entry_password.delete(0, tk.END))

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
        base_datos.verificar_login("lechus", "usuarios", user)
        
        # ###########################################
        # #VARIABLE OCASIONAL PARA ENTRAR SIN USUARIO
        # ###########################################
        # base_datos.validacion_login = True
        if base_datos.validacion_login:
            self.root.destroy()
            self.close_create(RelaxApp_User_Main_Menu)

        else:
            self.error_login = ctk.CTkLabel(self.frame, text="Usuario o contraseña incorrecta. Vuelva a intentarlo.", 
                                            font=(font,11))
            self.error_login.place(rely=0.81, relx=0.5, anchor="center")

    
    # Method that register users.
    def sign_up(self):
        self.root.destroy()
        self.close_create(RelaxApp_User_Registration)

    # Method to change password.
    def change_password(self):
        self.root.destroy()
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
        self.name_entry.bind("<Button-1>", lambda borrar: self.name_entry.delete(0, tk.END))

        # Label to register the last name.
        self.last_name = ctk.CTkLabel(self.frame, text="Apellido:", font=(font,14))
        self.last_name.place(rely=0.3, relx=0.03)
        
        # Last name entry.
        self.last_name_entry = ctk.CTkEntry(self.frame, font=(font,14), width=180, height=10, corner_radius=10)
        self.last_name_entry.place(rely=0.3, relx=0.42)
        self.last_name_entry.bind("<Button-1>", lambda borrar: self.last_name_entry.delete(0, tk.END))

        # Label to register the username.
        self.username = ctk.CTkLabel(self.frame, text="Nombre Usuario:", font=(font,14))
        self.username.place(rely=0.4, relx=0.03)
        
        # Username entry.
        self.username_entry = ctk.CTkEntry(self.frame, font=(font,14), width=180, height=10, corner_radius=10)
        self.username_entry.place(rely=0.4, relx=0.42)
        self.username_entry.bind("<Button-1>", lambda borrar: self.username_entry.delete(0, tk.END))

        # Label to register the password.
        self.password = ctk.CTkLabel(self.frame, text="Contraseña:", font=(font,14))
        self.password.place(rely=0.5, relx=0.03)
        
        # Password entry.
        self.password_entry = ctk.CTkEntry(self.frame, font=(font,14), width=180, height=10, corner_radius=10, 
                                           show="*")
        self.password_entry.place(rely=0.5, relx=0.42)
        self.password_entry.bind("<Button-1>", lambda borrar: self.password_entry.delete(0, tk.END))

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
        self.name_entry.bind("<Button-1>", lambda borrar: self.name_entry.delete(0, tk.END))
       
        # Label to set the new password.
        self.pw1 = ctk.CTkLabel(self.frame, text="Nueva Contraseña:", font=(font,14))
        self.pw1.place(rely=0.3, relx=0.03)
        
        # Password entry 1.
        self.pw1_entry = ctk.CTkEntry(self.frame, font=(font,14), width=165, height=10, corner_radius=10, 
                                      show="*")
        self.pw1_entry.place(rely=0.3, relx=0.47)
        self.pw1_entry.bind("<Button-1>", lambda borrar: self.pw1_entry.delete(0, tk.END))

        # Label to confirm the new password.
        self.pw2 = ctk.CTkLabel(self.frame, text="Repetir Contraseña:", font=(font,14))
        self.pw2.place(rely=0.4, relx=0.03)
        
        # Password entry 2.
        self.pw2_entry = ctk.CTkEntry(self.frame, font=(font,14), width=165, height=10, corner_radius=10, 
                                      show="*")
        self.pw2_entry.place(rely=0.4, relx=0.47)
        self.pw2_entry.bind("<Button-1>", lambda borrar: self.pw2_entry.delete(0, tk.END))
        
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

    def __init__(self, root):
        super().__init__(root)
        self.root = root

        self.start = False

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
        self.menu_archieve.add_command(label=" Cargar Configuración  ", font=(font,9), command=self.load_configuration, 
                                       background=colors["soft_grey"], foreground=colors["white"], activebackground=colors["dark_green"], 
                                       hidemargin=True)
        self.menu_archieve.add_command(label=" Guardar Configuración  ", font=(font,9), command=self.save_configuration, 
                                       background=colors["soft_grey"], foreground=colors["white"], activebackground=colors["dark_green"], 
                                       hidemargin=True)
        
        # Label of help menu cascade.
        self.menu_help.add_command(label=" Conozca RelaxApp  ", font=(font,9), command=self.about_us, background=colors["soft_grey"], 
                                   foreground=colors["white"], activebackground=colors["dark_green"], hidemargin=True)

        # Options label.
        self.options = ctk.CTkLabel(self.frame_main, text="Configurar", font=(font, 16), corner_radius=10, height=35)
        self.options.place(rely=0.3, relx=0.5, anchor="center")

        if self.start == False:
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

            # Button to set start RelaxApp.
            self.start_relaxapp_button = ctk.CTkButton(self.frame_main, text="Iniciar", font=(font, 20), 
                                                    command=self.start_relaxapp, height=70, corner_radius=50, 
                                                    hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
            self.start_relaxapp_button.place(rely=0.7, relx=0.5, anchor="center")

        elif self.start == True:
            self.test = ctk.CTkButton(self.frame_main, text="COMENZADO", font=(font, 20), 
                                                    height=70, corner_radius=50, 
                                                    hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
            self.test.place(rely=0.7, relx=0.5, anchor="center")


    ###################################################################
    ###### TO SET ######
    def load_configuration(self):
        ###### TO SET ######
        print("load_configuration EN DESARROLLO")
        ###### TO SET ######

    ###### TO SET ######
    def save_configuration(self):
        ###### TO SET ######
        print("save_configuration EN DESARROLLO")
        ###### TO SET ######

    ###### TO SET ######
    def about_us(self):
        ###### TO SET ######
        print("about_us EN DESARROLLO")
        ###### TO SET ######

    ###### TO SET ######
    def set_visual_options(self):
        self.visual_options_values = True
        RelaxApp_User_Main_Menu_Settings(self.root, self.visual_options_values)

    def set_stretch_options(self):
        self.stretch_options_values = True
        RelaxApp_User_Main_Menu_Settings(self.root, None, self.stretch_options_values)

    def start_relaxapp(self):
        ###### TO SET ######
        print("start_relaxapp EN DESARROLLO")


        ###### TO SET ######
    ###################################################################

    # Function to sign out of the App.
    def sign_out(self):
        self.user = user["login"]
        RelaxApp_MessageBox_Options(self.root, "Sign Out", self.user)


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
                                          corner_radius=10, fg_color=colors["soft_green"])
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
        self.lenght_entryHH.bind("<Button-1>", lambda borrar: self.lenght_entryHH.delete(0, tk.END))

        # Two points separator.
        self.twopoints_lenght_entry = ctk.CTkLabel(self.frame2, text=":", font=(font, 14))
        self.twopoints_lenght_entry.place(rely=0.5, relx=0.79, anchor="e")

        # Lenght entry minutes.
        self.lenght_entryMM = ctk.CTkEntry(self.frame2, font=(font,14), width=40, justify="center",
                                           validate="key", validatecommand=(self.min_sec_entry, "%P"))
        self.lenght_entryMM.place(rely=0.5, relx=0.97, anchor="e")
        self.lenght_entryMM.insert(0, "MM")
        self.lenght_entryMM.bind("<Button-1>", lambda borrar: self.lenght_entryMM.delete(0, tk.END))

        # Lapse label.
        self.lapse = ctk.CTkLabel(self.frame3, text="Intervalo Alertas", font=(font, 14))
        self.lapse.place(rely=0.5, relx=0.03, anchor="w")

        # Lapse entry.
        self.lapse_entry = ctk.CTkEntry(self.frame3, font=(font,14), width=40, justify="center",
                                        validate="key", validatecommand=(self.min_sec_entry, "%P"))
        self.lapse_entry.place(rely=0.5, relx=0.97, anchor="e")
        self.lapse_entry.insert(0, "MM")
        self.lapse_entry.bind("<Button-1>", lambda borrar: self.lapse_entry.delete(0, tk.END))

        # Break time label.
        self.break_time = ctk.CTkLabel(self.frame4, text="Tiempo Descanso", font=(font, 14))
        self.break_time.place(rely=0.5, relx=0.03, anchor="w")

        # Break time entry minutes.
        self.break_time_entryMM = ctk.CTkEntry(self.frame4, font=(font,14), width=40, justify="center",
                                               validate="key", validatecommand=(self.min_sec_entry, "%P"))

        self.break_time_entryMM.place(rely=0.5, relx=0.76, anchor="e")
        self.break_time_entryMM.insert(0, "MM")
        self.break_time_entryMM.bind("<Button-1>", lambda borrar: self.break_time_entryMM.delete(0, tk.END))

        # Two points separator.
        self.twopoints_break_time_entry = ctk.CTkLabel(self.frame4, text=":", font=(font, 14))
        self.twopoints_break_time_entry.place(rely=0.5, relx=0.79, anchor="e")

        # Break time entry seconds.
        self.break_time_entrySS = ctk.CTkEntry(self.frame4, font=(font,14), width=40, justify="center",
                                               validate="key", validatecommand=(self.min_sec_entry, "%P"))

        self.break_time_entrySS.place(rely=0.5, relx=0.97, anchor="e")
        self.break_time_entrySS.insert(0, "SS")
        self.break_time_entrySS.bind("<Button-1>", lambda borrar: self.break_time_entrySS.delete(0, tk.END))

        # Sound alert label.
        self.sound_alert = ctk.CTkLabel(self.frame5, text="Activar Sonido", font=(font, 14))
        self.sound_alert.place(rely=0.5, relx=0.03, anchor="w")

        # Sound alert checkbox.
        self.sound_alert_choice = ctk.IntVar()
        self.sound_alert_CB = ctk.CTkCheckBox(self.frame5, text=None, variable=self.sound_alert_choice, width=20, height=20, hover=True, 
                                              fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.sound_alert_CB.place(rely=0.5, relx=1, anchor="e")
        self.sound_alert_activated = False

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


    def save_settings(self):

        if self.sound_alert_choice.get() == 1:
            self.sound = True
        else:
            self.sound = False
        
        if self.lenght_entryHH.get() == "HH" or self.lenght_entryMM.get() == "MM" or \
        self.lapse_entry.get() == "MM" or self.break_time_entryMM.get() == "MM" or \
        self.break_time_entrySS.get() == "SS":
            RelaxApp_MessageBox_Options(self.root, "Empty")

        elif int(self.lenght_entryHH.get()) > 16:
            RelaxApp_MessageBox_Options(self.root, "Extra Hours")
        elif int(self.lenght_entryMM.get()) > 60 or int(self.lapse_entry.get()) > 60 or  \
        int(self.break_time_entryMM.get()) > 60 or int(self.break_time_entrySS.get()) > 60:
            RelaxApp_MessageBox_Options(self.root, "Invalid Time")

        else:
            print("visual options values: ", self.visual_options_values)
            print("stretch options values: ", self.stretch_options_values)

            self.values += self.lenght_entryHH.get()
            self.values += self.lenght_entryMM.get()
            self.values += self.lapse_entry.get()
            self.values += self.break_time_entryMM.get()
            self.values += self.break_time_entrySS.get()
            self.values += str(self.sound)
            print("values: ", self.values)

            if self.visual_options_values == True:
                base_datos.configuraciones_usuario("lechus", "usuarios_configuraciones", "lechu1", "Configuracion_visual", self.values)

            elif self.stretch_options_values == True:
                base_datos.configuraciones_usuario("lechus", "usuarios_configuraciones", "lechu1", "Configuracion_estirar", self.values)

            print("visual options values: ", self.visual_options_values)
            print("stretch options values: ", self.stretch_options_values)

            print("########################################")
            self.window.destroy()
        
    def cancel_settings(self):
        self.window.destroy()






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
            # Label ask/cancel to alert not to work extra hours.
            self.invalid_time_label = ctk.CTkLabel(self.window, text="Los minutos o los segundos no deben ser mayores a 60.", 
                                                   font=(font,14), bg_color=colors["soft_grey"])
            self.invalid_time_label.place(rely=0.3, relx=0.5, anchor="center")
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
            base_datos.editar_tabla("lechus", "usuarios", self.user)
        elif message == "Password Correct":
             # App connects with the database to check if the information is valid or not. 
            base_datos.editar_tabla("lechus", "usuarios", self.user)

        # User registration is canceled and turn back to main menu.
        elif message == "Cancel" or message == "Cancel Change PW" or message == "Sign Out":
            self.root.destroy()
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
        self.root.destroy()
        RelaxApp_Structure.close_create(self, RelaxApp_Initial_Frame)

    def return_button(self):
        self.window.destroy()
