from tkinter import *
from re import match
from Windows.window import ClearWindow
from Windows.main_page import MainPage
from account_system.validation import Validation
from account_system.account import Account

def AccountCreationPage(window) -> None:
    """
    страница создания нового аккаунта
    """
    
    window.geometry("500x400")
    
    errmsg = StringVar() # текст сообщения ошибки
    ErrorLabel = Label(window, foreground="red",
                       font = ("Arial", 10),
                       textvariable=errmsg, 
                       wraplength=300) # сообщение
    
    # приветственный текст
    AccCrtLabel = Label(window, text="welcome to account creation!",
                        font= ("Arial", 15, "bold"))
    AccCrtLabel.pack()
    
    # правила создания аккаунта
    RulesLabel = Label(window, text="When creating an account, login must be from 5 to 12 characters in length, must not contain characters other than numbers, letters and underscores, and must not begin with a number.\nPassword must be from 6 to 12 characters in length and must contain letters, numbers and special characters.\nName can by anything",
                       font= ("Arial", 10),
                       wraplength=500)
    RulesLabel.pack()
    
    # подпись к созданию логина
    LoginCreationLabel = Label(window, text="Login: ",
                               font= ("Arial", 10, "bold"),
                               pady= 10)
    LoginCreationLabel.pack()
    
    # функция валидации логина при вводе
    def IsValLog(login): 
        result = match(r"^[^\d]\w{5,12}$", login) is not None
        if not result and (len(login) < 5 or len(login) > 12):
            errmsg.set("Login must be from 5 to 12 symbols long!")
        else:
            errmsg.set("")
        return result
    
    LogCheck = (window.register(IsValLog), "%P")
    
    # поле создания логина
    LoginCreationEntry = Entry(window, justify="center",
                               width=20,
                               font=("Arial", 15),
                               validate="focusin",
                               validatecommand=LogCheck)
    LoginCreationEntry.pack()
    
    # подпись к созданию пароля
    PasswordCreationLabel = Label(window, text="Password: ",
                                  font= ("Arial", 10, "bold"),
                                  pady= 10)
    PasswordCreationLabel.pack()
    
    # функция валидации пароля при вводе
    def IsValPass(password): 
        result = match(r"^(?=.*\d)(?=.*[a-zA-Z])(?=.*\W).{6,12}$", password) is not None
        if not result and (len(password) < 6 or len(password) > 12):
            errmsg.set("Password must be from 6 to 12 symbols long!")
        else:
            errmsg.set("")
        return result
    
    PassCheck = (window.register(IsValPass), "%P")
    
    # поле создания пароля
    PasswordCreationEntry = Entry(window, justify="center",
                                  width=20,
                                  font=("Arial", 15),
                                  validate="focusin",
                                  validatecommand=PassCheck)
    PasswordCreationEntry.pack()
    
    # подпись к созданию имени
    NameCreationLabel = Label(window, text="Name: ",
                                  font= ("Arial", 10, "bold"),
                                  pady= 10)
    NameCreationLabel.pack()
    
    # поле создания имени
    NameCreationEntry = Entry(window, justify="center",
                                  width=20,
                                  font=("Arial", 15),
                                  validate="focusin")
    NameCreationEntry.pack()
    
    ErrorLabel.pack()
    
    # функция создания аккаунта
    def AccountCreate():
        login = LoginCreationEntry.get()
        password = PasswordCreationEntry.get()
        name = NameCreationEntry.get().strip() if len(NameCreationEntry.get().strip()) > 0 else login
        if (Validation.LoginValidation(login) and 
        Validation.PasswordValidation(password)):
            print("аккаунт создан!")
            account = Account(login, password, name)
            ClearWindow(window)
            MainPage(window, account)
        else:
            print("не удалось создать аккаунт")
            errmsg.set("An incorrect login or password has been entered")
    
    # кнопка создания аккаунта
    CreationButton = Button(window, text="Create",
                            command=AccountCreate)
    CreationButton.pack()