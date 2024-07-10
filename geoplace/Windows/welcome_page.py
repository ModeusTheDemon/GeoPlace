from tkinter import *
from re import match
from Windows.window import ClearWindow
from Windows.account_creation_page import AccountCreationPage
from Windows.main_page import MainPage
from account_system.account import Account

def WelcomePage(window) -> None:
    """
    приветственная страница с возможность входа в аккаунт или создания нового
    """
    
    errmsg = StringVar() # текст сообщения ошибки
    ErrorLabel = Label(window, foreground="red",
                       font = ("Arial", 10),
                       textvariable=errmsg, wraplength=300) # сообщение ошибки
    
    # приветственные слова
    WelcomeLabel = Label(window, text="Welcome to GeoPlace!",
                         font = ("Arial", 25, "bold"),
                         pady= 20)
    WelcomeLabel.pack()
    
    # подпись к вводу логина
    LoginLabel = Label(window, text="Login:",
                       font = ("Arial", 10, "bold"))
    LoginLabel.pack()
    
    # функция валидации логина при вводе
    def IsValLog(login): 
        result = match(r"^[^\d]\w{5,12}$", login) is not None
        if not result and (len(login) < 5 or len(login) > 12):
            errmsg.set("Login must be from 5 to 12 symbols long!")
        else:
            errmsg.set("")
        return result
    
    LogCheck = (window.register(IsValLog), "%P")
    
    # место для ввода логина
    LoginEntry = Entry(window, justify="center",
                       width=20,
                       font=("Arial", 15),
                       validate="focusin",
                       validatecommand=LogCheck)
    LoginEntry.pack(pady=5)
    
    # подпись к вводу пароля
    PasswordLabel = Label(window, text="Password:",
                          font = ("Arial", 10, "bold"))
    PasswordLabel.pack()
    
    # функция валидации пароля при вводе
    def IsValPass(password): 
        result = match(r"^(?=.*\d)(?=.*[a-zA-Z])(?=.*\W).{6,12}$", password) is not None
        if not result and (len(password) < 6 or len(password) > 12):
            errmsg.set("Password must be from 6 to 12 symbols long!")
        else:
            errmsg.set("")
        return result
    
    PassCheck = (window.register(IsValPass), "%P")

    # место для ввода пароля
    PasswordEntry = Entry(window, justify="center",
                          width=20,
                          font=("Arial", 15),
                          validate="focusin",
                          validatecommand=PassCheck)
    PasswordEntry.pack(pady=5)
    
    ErrorLabel.pack()
    
    def Enter(): 
        """
        функция, проверяющаю уже существующие зарегестрированные аккаунты на соответствие введеным данным
        """
        login = LoginEntry.get().strip()
        password = PasswordEntry.get().strip()
        with open(r"src\accounts_info.txt", "r") as file:
            for account in file.readlines():
                account = account.strip().split()
                SavedLogin = account[0]
                SavedPassword = account[1]
                if login == SavedLogin and password == SavedPassword:
                    print("вход в аккаунт успешен")
                    name = account[2]
                    account = Account(login, password, name)
                    ClearWindow(window)
                    MainPage(window, account)
        errmsg.set("can't find any account with this login and password! Are you sure you entered them correctly?")  
    
    # кнопка входа в аккаунт
    EnterButton = Button(window, text="enter",
                         command=Enter)
    EnterButton.pack()
    
    # подпись к кнопке создания аккаунта
    NewAccountLabel = Label(window, text="Don't have an account?",
                          font = ("Arial", 10, "bold"))
    NewAccountLabel.pack(padx=15, pady=10,
                         anchor="s")
    
    def Create():
        print("создание аккаунта")
        ClearWindow(window)
        AccountCreationPage(window)
    
    # кнопка создания аккаунта
    EnterButton = Button(window, text="create",
                         command=Create)
    EnterButton.pack()