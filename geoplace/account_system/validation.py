import re

class Validation:
    """
    класс, отвечающий за валидацию всех входных данных(паролей, логинов).
    """
    def LoginValidation(login: str) -> bool:
        """
        валидация логина при создании аккаунта
        """
        if re.match(r"^[^\d]\w{5,12}$", login):
            print("логин действителен")
            return True
        else:
            print("логин не действителен")
            return False
    
    def PasswordValidation(password: str) -> bool:
        """
        валидация пароля при создании аккаунта
        """
        if re.match(r"^(?=.*\d)(?=.*[a-zA-Z])(?=.*\W).{6,12}$", password):
            print("пароль действителен")
            return True
        else:
            print("пароль не действителен")
            return False