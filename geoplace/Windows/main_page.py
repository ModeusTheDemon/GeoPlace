import osmnx as ox
from itertools import islice
from tkinter import *
from tkinter import ttk
from geocoder import ip
from geopy.geocoders import Nominatim
from account_system.account import Account

def MainPage(window: Tk, account: Account):
    """
    основная страница, на которой пользователь может увидеть историю своих посещений оценку
    достопримечатьностей с их описанием от пользователя
    """
    
    window.geometry("600x600")
    
    errmsg = StringVar() # текст сообщения ошибки
    errmsg2= StringVar() # текст сообщения ошибки 2
    ErrorLabel = Label(window, foreground="red",
                       font = ("Arial", 10),
                       textvariable=errmsg, 
                       wraplength=300) # сообщение ошибки
    
    WelcomeLabel = Label(window, text=f"Welcome, {account.name}",
                         font=("Arial", 15, "bold"))
    WelcomeLabel.pack()
    
    def GetCurrentLocation(): # текущее местоположение в долготе и широте через ip адрес
        location = ip('me')
        latitude = location.latlng[0]
        longitude = location.latlng[1]
        return latitude, longitude
    
    geolocator = Nominatim(user_agent="MyGeocodingApp")
    
    def GetAddressFromCoordinates(latitude, longitude): # адрес через долготу и широту
        location = geolocator.reverse((latitude, longitude))
        address = location.address
        return address

    lat, lng = GetCurrentLocation() # примерное местоположение пользователя
    
    addres = GetAddressFromCoordinates(lat, lng).split(', ')[0:3] # приблизительный адресс пользователя
    
    CurrentLocationLabel = Label(window, text=f"Current location: {addres[0]}, {addres[1]}, {addres[2]}",
                                 font=("Arial", 10))
    
    CurrentLocationLabel.pack()
    
    
    # краткая история 
    First3Elements = dict(islice(account.story.items(), 3))
    First3ElementsKeys = list(First3Elements.keys())
    LastHystoryLabel = Label(window, text=f"""Last 3 visited places:
{First3ElementsKeys[0][0] + ": " + str(First3Elements[First3ElementsKeys[0]]) if len(First3Elements) > 0 else "-"}
{First3ElementsKeys[1][0] + ": " + str(First3Elements[First3ElementsKeys[1]]) if len(First3Elements) > 1 else "-"}
{First3ElementsKeys[2][0] + ": " + str(First3Elements[First3ElementsKeys[2]]) if len(First3Elements) > 2 else "-"}""",
                             font=("Arial", 10))
    LastHystoryLabel.pack()
    
    # функция нахождения ближайших достопримечательностей через OpenStreetMaps
    def NearestSights():
        global Rating, RateExpText, RateVariants
        NearSights = ox.features_from_point((GetCurrentLocation()), 
                                        tags={
                                            'tourism': 'attraction',
                                            'amenity': 'tourist_attraction',
                                            'historic': 'yes',
                                            'leisure': 'park',
                                            'landmark': 'yes'
                                            }, 
                                        dist=5000)
        Sights = {} # (имя, адрес): (оценка пользователя, отзыв пользователя)
        for i in range(5):
            sight = dict(NearSights.iloc[i]) 
            # (имя, адрес): (оценка пользователя, отзыв пользователя)
            Sights[(sight["name"], ", ".join(GetAddressFromCoordinates(sight["geometry"].y, sight["geometry"].x).split(', ')[0:3]))] = ()
        variants = [f"{name}: {addres}" for name, addres in list(Sights.keys())] # 5 ближайщих мест (имя, адрес)
        
        # ближайшие 5 достопримечательностей
        NearestSightsLabel = Label(window, text=f"""Nearest 5 Sights:
1. {variants[0] if len(variants[0]) < 50 else variants[0][0:60] + "..." if len(variants) > 0 else "-"}
2. {variants[1] if len(variants[0]) < 50 else variants[1][0:60] + "..." if len(variants) > 1 else "-"}
3. {variants[2] if len(variants[0]) < 50 else variants[2][0:60] + "..." if len(variants) > 2 else "-"}
4. {variants[3] if len(variants[0]) < 50 else variants[3][0:60] + "..." if len(variants) > 3 else "-"}
5. {variants[4] if len(variants[0]) < 50 else variants[4][0:60] + "..." if len(variants) > 4 else "-"}""",
                             font=("Arial", 10),)
        NearestSightsLabel.pack()
        
        #подпись к оценке мест
        QuestionLabel = Label(window, text="Want to rate any nearest sight?",
                            font=("Arial", 15))
        QuestionLabel.pack()
        
        # список мест для оценки
        RateVariants = ttk.Combobox(values=variants,
                                    width=100)
        RateVariants.pack()

        # подпись к оценке в баллах
        RateLabel = Label(window, text="Rating from 1 to 10:")
        RateLabel.pack()
        
        # сообщение о вводе некоректной оценки
        ErrorLabel2 = Label(window, foreground="red",
                            font = ("Arial", 10),
                            textvariable=errmsg2, 
                            wraplength=300)
        
        def CheckRate(Rating):
            try:
                Rating = int(Rating)
            except:
                errmsg2.set("Incorrect rating!")
                Rating = 0
            if Rating < 1 or Rating > 10:
                errmsg2.set("Incorrect rating!")
                Rating = 0
            else:
                errmsg2.set("")
            return Rating
        
        RatePass = (window.register(CheckRate), "%P")
        
        # оценка места
        Rating = Entry(window, justify="center",
                       width=10,
                       font=("Arial", 15),
                       validate="focusin",
                       validatecommand=RatePass)
        Rating.pack()
        
        ErrorLabel2.pack()
        
        # подпись к описанию оценки
        RateExpLabel = Label(window, text="Explain your rate(optional):")
        RateExpLabel.pack()
        
        # поле для описания
        RateExpText = Text(window, wrap="word",
                           width=30,
                           height= 5,
                           font=("Arial", 15))
        RateExpText.pack()
        
        # удаляем кнопку с ближайшими достопримечательностями
        NearestSightsButton.pack_forget()
        
        # функция сохранения оценки достопримечательности
        def SaveRating():
            place = tuple(RateVariants.get().split(": "))
            rate = int(Rating.get())
            txt = RateExpText.get("1.0", "end").strip()
            if 0 < rate < 11:
                account.SaveNewRate({place: (rate, txt)})
            else:
                errmsg2.set("Invalid rating!")
        
        # кнопка сохранения оценки места
        SavedRatingButton = Button(window, text="Save rating",
                                command=SaveRating)
        SavedRatingButton.place(x=275, y=550)
    
    # кнопка для получения ближайших достопримечательностей
    NearestSightsButton = Button(window, text="Get nearest sights",
                                 command=NearestSights)
    NearestSightsButton.pack(pady=5)
    
    ErrorLabel.pack()