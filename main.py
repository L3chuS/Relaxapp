import Interface.relaxapp as app

if __name__ == "__main__":
    root = app.ctk.CTk()
    app = app.RelaxApp_Structure(root)
    root.mainloop()