import tkinter as tk
from tkinter import ttk 
from gui_module import UserInterface as ui

class DataAnalyzerApp:
    def __init__(self):
        ui_obj = ui()
        ui_obj.insert_documents_to_db()
        ui_obj.design_gui()


if __name__ == "__main__":
    DataAnalyzerApp()
    tk.mainloop()
