from tkinter import *

def CreateWindow(size):
    """
    создает пустое окно приложения
    """
    def finish():
        '''
        метод закрытия окна
        '''
        window.destroy()
        print("закрытие окна")
    print("создание окна")
    window = Tk() # основное окно
    window.title("GeoPlace") # имя окна
    window.geometry(size) # размер окна
    window.resizable(False, False) # запрет на измененение размеров окна
    window.iconbitmap(default="src\icon.ico") # смена иконки окна
    window.protocol("WM_DELETE_WINDOW", finish) # протокол закрытия приложения
    return window

def ClearWindow(window):
    """
    отчистить окно от всех виджетов
    """
    for widget in window.winfo_children():
        widget.destroy()