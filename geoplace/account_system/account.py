import ast

class Account:
    """
    Класс, представляющий собой аккаунт пользователя.
    собственные аттрибуты: 
        login: str,
        password: str,
        name: str
    сам по себе класс нужен для доступа к истории посещений и собственным оценкам достопримечательностей
    """
    def __init__(self, login, password, name):
        with open(r"src\accounts_info.txt", "a+", encoding="utf-8") as file:
            file.seek(0)
            for account in file.readlines(): # проверка аккаунта, на существующие и вход в него при нахождении
                account = account.strip().split(maxsplit=3)
                print(account)
                SavedLogin = account[0]
                SavedPassword = account[1]
                if SavedLogin == login and SavedPassword == password: # случай, если аккаунт существует
                    self.__login = SavedLogin
                    self.__password = SavedPassword
                    self.__name = account[2]
                    self.__story = ast.literal_eval(account[3])
                    break
            else: # создание нового аккаунта
                self.__login = login
                self.__password = password
                self.__name = name
                self.__story = {}
                file.write(f"\n{self.__login} {self.__password} {self.__name} {self.__story}")
                print("Account created!\n")
    
    @property
    def login(self):
        return self.__login
    
    @property
    def password(self):
        return self.__password
    
    @property
    def name(self):
        return self.__name
    
    @property
    def story(self):
        return self.__story
    
    @login.setter
    def login(self, login):
        self.__login = login
    
    @password.setter
    def password(self, password):
        self.__password = password
    
    @name.setter
    def name(self, name):
        self.__name = name
    
    def SaveNewRate(self, rate: dict): # rate = {(name: str, adress: str): (rate: int, rateext: str)}
        """
        сохраняет новую оценку в словарь и в файл
        """
        # name = list(rate.keys())[0][0]
        # adress = list(rate.keys())[0][1]
        # rating = list(rate.values())[0][0]
        # txt = list(rate.values())[0][1]
        self.__story[list(rate.keys())[0]] = list(rate.values())[0]
        with open(r"src\accounts_info.txt", "r", encoding="utf-8") as file:
            file.seek(0)
            lines = file.readlines()
        lineNum = 0
        print(lines)
        with open(r"src\accounts_info.txt", "w", encoding="utf-8") as file:
            file.seek(0)
            for line in lines:
                if line.split()[0] == self.__login and line.split()[1] == self.__password:
                    lines[lineNum] = f"{self.__login} {self.__password} {self.__name} {self.__story}\n"
                    break
                lineNum += 1
            #print(lines)
            file.writelines(lines)
    
    def GetInfo(self): 
        """вывод информации о пользователе(в консоль)"""
        print(f"{self.__login} {self.__password} {self.__name} {self.__story}")