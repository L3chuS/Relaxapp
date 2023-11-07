import customtkinter as ctk
import tkinter as tk

root = ctk.CTk()

appearance = ctk.set_appearance_mode("dark")
color_theme = ctk.set_default_color_theme("green")

# Set the width, height, configuration and location of the windows.
width = 350
height = 500

dimentions = root.geometry(f"{width}x{height}")
maximize = root.resizable(False,False)

font = "Segoe Print"

# Set a frame at the background.
frame = ctk.CTkFrame(root, height=30, width=350, fg_color="#2b2b2b")
frame.pack(pady=10, padx=10, fill="both") 

frame2 = ctk.CTkFrame(root, height=440, width=350, fg_color="#2b2b2b")
frame2.pack(pady=0, padx=10, fill="both") 


options_menu_button = tk.Menubutton(frame, text="Archivo", font=(font,11),
width=30, height=1)
options_menu_button.place(rely=0.5, relx=0.01, anchor="w")

menu_archivo = tk.Menu(options_menu_button, tearoff=0)

menu_archivo.add_command(label="imprimir", command=lambda: print("imprimir"), background="#2b2b2b", foreground="white", activebackground="#0a4e50")
menu_archivo.add_command(label="imprimir2", command=lambda: print("imprimir"), background="#2b2b2b", foreground="white", activebackground="#0a4e50")

options_menu_button.config(menu=menu_archivo)
options_menu_button.pack(side="left")

canvas = tk.Canvas(height=40, width=40)
canvas.pack(side="top")


root.mainloop()