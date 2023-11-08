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
       Defines the appearance, dimensions and title."""

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

class RelaxApp_MessageBox_Structure:
    """This class defines the general structure of the pop-ups.
       Defines the appearance, dimensions and title."""

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
        corner_radius=90, width=100, height=20, hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.button_start.place(rely=0.72, relx=0.5, anchor="center")

        # "Register User" button..
        self.button_new_user = ctk.CTkButton(self.frame, width=10, height=10, text="Registrar Usuario", font=(font,12), command=self.sign_up,
        corner_radius=10, hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.button_new_user.place(rely=0.9, relx=0.04)

        # "Forget password" button.
        self.button_forget_pw = ctk.CTkButton(self.frame, width=10, height=10, text="Olvidé contraseña", font=(font,12), command=self.change_password,
        corner_radius=10, hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.button_forget_pw.place(rely=0.9, relx=0.6)

    # Method to log in.
    def sign_in(self):
        get_login = self.entry_user.get()
        get_password = self.entry_password.get()
        user["login"] = get_login
        user["password"] = get_password
        base_datos.verificar_login("lechus", "usuarios", user)
        
        ###########################################
        #VARIABLE OCASIONAL PARA ENTRAR SIN USUARIO
        ###########################################
        base_datos.validacion_login = True
        if base_datos.validacion_login:
            self.root.destroy()
            self.close_create(RelaxApp_User_Main_Menu)
            return user["login"]
        else:
            self.error_login = ctk.CTkLabel(self.frame, text="Usuario o contraseña incorrecta. Vuelva a intentarlo.", font=(font,11))
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
    """This class open a new window for users registrations. 
       Inherit all structure from parent."""

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        
        # Top bar of the register menu.
        self.top_bar = ctk.CTkLabel(self.frame, text=None, fg_color=colors["dark_green"], width=310, height=0, corner_radius=10)
        self.top_bar.place(rely=0.02, relx=0.03)

        # Bottom bar of the register menu.
        self.bottom_bar = ctk.CTkLabel(self.frame, text=None, fg_color=colors["dark_green"], width=310, height=0, corner_radius=10)
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
        self.password_entry = ctk.CTkEntry(self.frame, font=(font,14), width=180, height=10, corner_radius=10, show="*")
        self.password_entry.place(rely=0.5, relx=0.42)
        self.password_entry.bind("<Button-1>", lambda borrar: self.password_entry.delete(0, tk.END))

        # Button to accept the user registration.
        self.create_button = ctk.CTkButton(self.frame, text="Dar de Alta", font=(font,14), command= self.accept_sign_up,
        corner_radius=90, width=100, height=20, hover=True, fg_color=colors["soft_green"], hover_color="#0a4e50")
        self.create_button.place(rely=0.7, relx=0.5, anchor="center")

        # Button to cancel the user registration.
        self.cancel_button = ctk.CTkButton(self.frame, text="Cancelar", font=(font,14), command= self.cancel_sign_up,
        corner_radius=90, width=100, height=20, hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
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
    """This class open a new window to change the pasword. 
       Inherit all structure from parent."""

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        
        # Top bar of the change password menu.
        self.top_bar = ctk.CTkLabel(self.frame, text=None, fg_color=colors["dark_green"], width=310, height=0, corner_radius=10)
        self.top_bar.place(rely=0.02, relx=0.03)

        # Bottom bar of the change password menu.
        self.bottom_bar = ctk.CTkLabel(self.frame, text=None, fg_color=colors["dark_green"], width=310, height=0, corner_radius=10)
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
        self.pw1_entry = ctk.CTkEntry(self.frame, font=(font,14), width=165, height=10, corner_radius=10, show="*")
        self.pw1_entry.place(rely=0.3, relx=0.47)
        self.pw1_entry.bind("<Button-1>", lambda borrar: self.pw1_entry.delete(0, tk.END))

        # Label to confirm the new password.
        self.pw2 = ctk.CTkLabel(self.frame, text="Repetir Contraseña:", font=(font,14))
        self.pw2.place(rely=0.4, relx=0.03)
        
        # Password entry 2.
        self.pw2_entry = ctk.CTkEntry(self.frame, font=(font,14), width=165, height=10, corner_radius=10, show="*")
        self.pw2_entry.place(rely=0.4, relx=0.47)
        self.pw2_entry.bind("<Button-1>", lambda borrar: self.pw2_entry.delete(0, tk.END))
        
        # Button to confirm to change the password.
        self.change_pw_button = ctk.CTkButton(self.frame, text="Cambiar Contraseña", font=(font,14), command= self.accept_change_pw,
        corner_radius=90, width=100, height=20, hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        self.change_pw_button.place(rely=0.55, relx=0.5, anchor="center")

        # Button to cancel to change the password.
        self.cancel_change_pw_button = ctk.CTkButton(self.frame, text="Cancelar", font=(font,14), command= self.cancel_change_pw,
        corner_radius=90, width=100, height=20, hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
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

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        
        self.frame.configure(fg_color=colors["black"])
        self.frame.pack(pady=10, padx=0, fill="both")  

        self.frame_top_menu = ctk.CTkFrame(self.frame, height=30, width=350, fg_color=colors["soft_grey"], corner_radius=3)
        self.frame_top_menu.pack(pady=2, padx=10) 

        self.frame_main = ctk.CTkFrame(self.frame, height=450, width=350, fg_color=colors["soft_grey"])
        self.frame_main.pack(padx=10, fill="both")

        self.archieve_menu_button = tk.Menubutton(self.frame_top_menu, text="Archivo", font=(font,9),
        width=5, height=2, background=colors["soft_grey"], foreground=colors["white"], activebackground=colors["dark_green"], activeforeground=colors["white"])
        self.archieve_menu_button.place(rely=0.5, relx=0, anchor="w")

        self.help_button = tk.Menubutton(self.frame_top_menu, text="Ayuda", font=(font,9),
        width=4, height=2, background=colors["soft_grey"], foreground=colors["white"], activebackground=colors["dark_green"], activeforeground=colors["white"])
        self.help_button.place(rely=0.5, relx=0.18, anchor="w")
        
        # SE PUEDE BORRAR TODO ESTOS 
        # self.sign_out_button = tk.Menubutton(self.frame_top_menu, text="Cerrar Sesión", font=(font,9),
        # width=9, height=2, background=colors["soft_grey"], foreground=colors["white"], activebackground=colors["dark_green"], activeforeground=colors["white"])
        # self.sign_out_button.place(rely=0.5, relx=1, anchor="e")

        self.sign_out_button = ctk.CTkButton(self.frame_top_menu, width=10, height=50, text="Cerrar Sesión", font=(font,12), command=lambda:print(user["login"]),
        hover=True, fg_color=colors["soft_grey"], hover_color=colors["dark_green"])
        self.sign_out_button.place(rely=0.5, relx=1, anchor="e")

        self.menu_archieve = tk.Menu(self.archieve_menu_button, tearoff=0)
        self.archieve_menu_button.config(menu=self.menu_archieve)

        self.menu_help = tk.Menu(self.help_button, tearoff=0)
        self.help_button.config(menu=self.menu_help)

        self.menu_archieve.add_command(label=" Cargar Configuración  ", font=(font,9), command=lambda: print("imprimir"), background=colors["soft_grey"], foreground=colors["white"], activebackground=colors["dark_green"], hidemargin=True)
        self.menu_archieve.add_command(label=" Guardar Configuración  ", font=(font,9), command=lambda: print("imprimir"), background=colors["soft_grey"], foreground=colors["white"], activebackground=colors["dark_green"], hidemargin=True)

        self.menu_help.add_command(label=" Conozca RelaxApp  ", font=(font,9), command=lambda: print("imprimir"), background=colors["soft_grey"], foreground=colors["white"], activebackground=colors["dark_green"], hidemargin=True)


        # self.opciones_main_menu.add_command(label="Cargar Configuración")
        # self.opciones_main_menu.add_command(label="Guardar Configuración")
        # self.opciones_main_menu.add_separator()
        # self.opciones_main_menu.add_command(label="Salir", command=self.root.destroy) # MODIFICAR COMMAND


        # # Button to confirm to change the password.
        # self.change_pw_button = ctk.CTkButton(self.frame, text="Cambiar Contraseña", font=(font,14), command= self.accept_change_pw,
        # corner_radius=90, width=100, height=20, hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
        # self.change_pw_button.place(rely=0.55, relx=0.5, anchor="center")
    






















####################################################
###  Class that contains all pop-ups of the App  ###
####################################################

class RelaxApp_MessageBox_Options(RelaxApp_MessageBox_Structure):
    """This class defines all pop-ups of the App.
       Inherit all structure from parent."""
    
    def __init__(self, root, message, user):
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
            self.ask_cancel_label = ctk.CTkLabel(self.window, text="¿Está seguro que desea dar de alta \
el usuario indicado?", font=(font,14), bg_color=colors["soft_grey"])
            self.ask_cancel_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Cancel":
            # Label ask/cancel to cancel user registration.
            self.ask_cancel_label = ctk.CTkLabel(self.window, text="¿Está seguro que desea cancelar el alta \
del usuario indicado?", font=(font,14), bg_color=colors["soft_grey"])
            self.ask_cancel_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Continue":
            # Label confirm user registration.
            self.continue_registration = ctk.CTkLabel(self.window, text=base_datos.mensaje, font=(font,14), bg_color=colors["soft_grey"])
            self.continue_registration.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button2 = True

        elif message == "Error":
            # Label confirm user registration.
            self.continue_registration = ctk.CTkLabel(self.window, text=base_datos.mensaje, font=(font,14), bg_color=colors["soft_grey"])
            self.continue_registration.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button3 = True

        elif message == "Password Correct":
            # Label to confirm or not to change the password.
            self.pw_match = ctk.CTkLabel(self.window, text="¿Está seguro que desea actualizar su contraseña?", font=(font,14), bg_color=colors["soft_grey"])
            self.pw_match.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Password Incorrect":
            # Label to inform that the password 1 does not match with password 2.
            self.pw_unmatch = ctk.CTkLabel(self.window, text="Las contraseñas introducidas no coinciden entre sí. \
\nVuelva a introducirlas.", font=(font,14), bg_color=colors["soft_grey"])
            self.pw_unmatch.place(rely=0.35, relx=0.5, anchor="center")
            self.select_button1 = True

        elif message == "Cancel Change PW":
            # Label ask/cancel to cancel to change passwor.
            self.pw_ask_cancel_label = ctk.CTkLabel(self.window, text="¿Está seguro que desea cancelar el cambio de contraseña?", font=(font,14), bg_color=colors["soft_grey"])
            self.pw_ask_cancel_label.place(rely=0.3, relx=0.5, anchor="center")
            self.select_button1 = True

        if self.select_button1 == True:
            # Button to accept user registration.
            self.accept_ask_cancel_button = ctk.CTkButton(self.window, width=80, height=17, text="Aceptar", font=(font,14), command=lambda: self.accept_button(message),
            corner_radius=10, hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
            self.accept_ask_cancel_button.place(rely=0.65, relx=0.25, anchor="w")

            # Button to cancel user registration.
            self.cancel_ask_cancel_button = ctk.CTkButton(self.window, width=80, height=17, text="Cancelar", font=(font,14), command=self.cancel_button,
            corner_radius=10, hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
            self.cancel_ask_cancel_button.place(rely=0.65, relx=0.75, anchor="e")

        if self.select_button2 == True:
            # Button to continue to the main menu.
            self.continue_registration_button = ctk.CTkButton(self.window, width=80, height=17, text="Continuar", font=(font,14), command=self.continue_button,
            corner_radius=10, hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
            self.continue_registration_button.place(rely=0.65, relx=0.5, anchor="center")

        if self.select_button3 == True:
            # Button to continue to the main menu.
            self.continue_registration_button = ctk.CTkButton(self.window, width=80, height=17, text="Volver", font=(font,14), command=self.return_button,
            corner_radius=10, hover=True, fg_color=colors["soft_green"], hover_color=colors["dark_green"])
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
        elif message == "Cancel" or message == "Cancel Change PW":
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

