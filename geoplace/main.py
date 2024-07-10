from Windows.window import CreateWindow
from Windows.welcome_page import WelcomePage

window = CreateWindow(size="500x350") # создаем окно

WelcomePage(window)

window.mainloop() # запуск окна с приложением