import numpy as np #Библиотека работы с массивами
import pandas as pd # Библиотека для работы с базами

from sklearn.preprocessing import StandardScaler 
from tensorflow.keras import utils #Используем для to_categoricallS
from keras.models import load_model
from tensorflow.keras.layers import Input

def estimation(rooms, metro,metroDistance,floor,floors,area,isLastFloor, wc, balcon, houseTypeStr):
    roomsCountStr = rooms #Получаем строку с числом комнат    
    roomsCount = int(roomsCountStr) #Пробуем превратить строку в число
    roomsCount = utils.to_categorical(roomsCount, 5)

    metroTypeClasses = 6 #Число классов метро
    metroType = metroTypeClasses - 1 #Изначально считаем последний класс
    metroNamesInsideCircle = ["Китай-Город","Библиотека им.Ленина", "Площадь Революции", "Арбатская", "Смоленская", "Красные Ворота", "Красные ворота", "Чистые пруды", "Лубянка", "Охотный Ряд", "Охотный ряд", "Библиотека имени Ленина", "Кропоткинская", "Сухаревская", "Тургеневская", "Китай-город", "Китай-Город" "Третьяковская", "Трубная", "Сретенский бульвар", "Цветной бульвар", "Чеховская", "Боровицкая", "Полянка", "Маяковская", "Тверская", "Театральная", "Новокузнецкая", "Пушкинская", "Кузнецкий Мост", "Кузнецкий мост", "Китай-город", "Александровский сад", "Александровский Сад"]
    metroNamesCircle = ["Баррикадная", "Марксистская", "Чкаловская", "Менделеевская", "Киевская", "Парк Культуры", "Парк культуры", "Октябрьская", "Добрынинская", "Павелецкая", "Таганская", "Курская", "Комсомольская", "Проспект Мира", "Новослободская", "Белорусская", "Краснопресненская", "Серпуховская"]
    metroNames13FromCircle = ["Улица 1905 года", "Лужники", "Москва-Товарная", "Бауманская", "Электрозаводская", "Семеновская", "Площадь Ильича", "Авиамоторная", "Шоссе Энтузиастов", "Римская", "Крестьянская Застава", "Дубровка", "Пролетарская", "Волгоградский проспект", "Текстильщики", "Автозаводская", "Технопарк", "Коломенская", "Тульская", "Нагатинская", "Нагорная", "Шаболовская", "Ленинский проспект", "Академическая", "Фрунзенская", "Спортивная", "Воробьевы горы", "Воробьевы Горы", "Студенческая", "Кутузовская", "Фили", "Парк Победы", "Выставочная", "Международная", "Улица 1905", "улица 1905", "Беговая", "Полежаевская", "Динамо", "Петровский Парк", "Аэропорт (старая)", "Аэропорт", "Сокол", "Деловой центр", "Хорошевская", "ЦСКА", "Петровский парк", "Савеловская", "Дмитровская", "Тимирязевская", "Достоевская", "Марьина Роща", "Марьина роща", "Бутырская", "Фонвизинская", "Рижская", "Алексеевская", "ВДНХ", "Красносельская", "Сокольники", "Преображенская площадь", "Калитники", "Новохохловская", "Минская", "Славянский бульвар"]
    metroNames48FromCircle = ["Каховская", "Перерва", "Новаторская", "Депо", "Румянцево", "Юго-Западная", "Народное ополчение", "Проспект Вернадского", "Говорово", "Лефортово", "Мневники", "Строгино", "Лианозово", "Нахимовский проспект", "Красный Балтиец", "Бескудниково", "Москворечье", "Домодедовская", "Озерная", "Раменки", "Крылатское", "Аминьевская", "Мякинино", "Стахановская", "Тестовская", "Зорге", "Ростокино", "ЗИЛ", "Партизанская", "Измайловская", "Первомайская", "Щелковская", "Новокосино", "Новогиреево", "Перово", "Кузьминки", "Рязанский проспект", "Выхино", "Лермонтовский проспект", "Жулебино", "Партизанская", "Измайловская", "Первомайская", "Щелковская", "Новокосино", "Новогиреево", "Перово", "Кузьминки", "Рязанский проспект", "Выхино", "Лермонтовский проспект", "Жулебино", "Улица Дмитриевского", "улица Дмитриевского", "Кожуховская", "Печатники", "Волжская", "Люблино", "Братиславская", "Коломенская", "Каширская", "Кантемировская", "Царицыно", "Орехово", "Севастопольская", "Чертановская", "Южная", "Пражская", "Варшавская", "Профсоюзная", "Новые Черемушки", "Калужская", "Беляево", "Коньково", "Университет", "Багратионовская", "Филевский парк", "Пионерская", "Кунцевская", "Молодежная", "Октябрьское Поле", "Октябрьское поле", "Щукинская", "Спартак", "Тушинская", "Сходненская", "Войковская", "Стрешнево", "Панфиловская", "Балтийская", "Водный стадион", "Речной вокзал", "Беломорская", "Ховрино", "Петровско-Разумовская", "Владыкино", "Отрадное", "Бибирево", "Алтуфьево", "Фонвизинская", "Окружная", "Верхние Лихоборы", "Селигерская", "ВДНХ", "Ботанический сад", "Свиблово", "Бабушкинская", "Медведково", "Преображенская площадь", "Черкизовская", "Бульвар Рокоссовского", "Воронцовская", "Терехово", "Угрешская", "Мичуринский проспект", "Давыдково", "Ломоносовский проспект"]
    metroNames9AndMoreFromCircle = ["Алма-Атинская", "Бульвар Адмирала Ушакова", "Силикатная", "Новоясеневская", "Новопеределкино", "Улица Скобелевская", "Улица Старокачаловская", "Красный Строитель", "Нахабино","Щербинка", "Филатов Луг", "Сколково", "Окская", "Пятницкое шоссе", "Юго-Восточная", "Курьяново", "Марьино", "Некрасовка", "Саларьево", "Рассказовка", "Боровское шоссе", "Сетунь", "Митино", "Теплый Стан","Бутово", "Улица Горчакова", "Лесопарковая", "Шипиловская", "Зябликово", "Бульвар Дмитрия","Марк", "Трикотажная", "Аннино","Бунинская Аллея", "Бунинская аллея", "Коммунарка", "Ольховая", "Долгопрудная", "Улица Академика", "улица Академика", "Бульвар Адмирала", "Прокшино"]
    MCCNames = ["Окружная", "Владыкино", "Ботанический сад", "Ростокино", "Белокаменная", "Бульвар Рокоссовского", "Локомотив", "Измайлово", "Соколиная Гора", "Шоссе Энтузиастов", "Андроновка", "Нижегородская", "Новохохловская", "Угрешская", "Дубровка", "Автозаводская", "ЗИЛ", "Верхние Котлы", "Верхние котлы", "Крымская", "Площадь Гагарина", "Лужники", "Кутузовская", "Деловой центр", "Шелепиха", "Хорошево", "Зорге", "Панфиловская", "Стрешнево", "Балтийская", "Коптево", "Лихоборы"]
    metroNamesInsideCircle = [x.lower() for x in metroNamesInsideCircle]
    metroNamesCircle = [x.lower() for x in metroNamesCircle]
    metroNames13FromCircle = [x.lower() for x in metroNames13FromCircle]
    metroNames48FromCircle = [x.lower() for x in metroNames48FromCircle]
    metroNames9AndMoreFromCircle = [x.lower() for x in metroNames9AndMoreFromCircle]
    metro = metro.lower()
    if (metro in metroNamesInsideCircle):
        metroType = 0
    if (metro in metroNamesCircle):
        metroType = 1
    if (metro in metroNames13FromCircle):
        metroType = 2
    if (metro in metroNames48FromCircle):
        metroType = 3
    if (metro in MCCNames):
        metroType = 4
    if (metro in metroNames9AndMoreFromCircle):
        metroType = 5
    print(metroType)
    metroType = utils.to_categorical(metroType, metroTypeClasses)

    if (metroDistance[-1] == "п"):
            metroDistanceType = 1 #Пешком
    elif (metroDistance[-1] == "т"):
            metroDistanceType = 2 #На транспорте
    metroDistance = metroDistance[:-1]
    metroDistance = int(metroDistance)
    if (metroDistance < 3):
        distance = 1
    elif (metroDistance < 6):
        distance = 2
    elif (metroDistance < 10):
        distance = 3
    elif (metroDistance < 15):
        distance = 4
    elif (metroDistance < 20):
        distance = 5
    else:
        distance = 6

    metroDistanceClasses = 7
    if (metroDistanceType == 2):
        distance += metroDistanceClasses #Для типа "Транспортом" добавляем 7
    if (metroDistanceType == 0):
        distance += 2*metroDistanceClasses #Для неопознанного типа добавляем 14
    #Превращаем в категории
    distance = utils.to_categorical(distance, 3*metroDistanceClasses)
    # global floor
    # global floors
    # global isLastFloor
    floorSave = int(floor)
    if (floorSave < 5):
        floor = 2
    if (floorSave < 10):
        floor = 3
    if (floorSave < 20):
        floor = 4
    if (floorSave >= 20):
        floor = 5
    if (floorSave == 1): #Первый этаж выделяем в отдельную категорию
        floor = 1 

    if (floor == floors): #Если этаж последний, включаем индикатор последнего этажа
        isLastFloor = 1 

    floorsSave = int(floors)
    if (floorsSave < 5):
        floors = 1
    if (floorsSave < 10):
        floors = 2
    if (floorsSave < 20):
        floors = 3
    if (floorsSave >= 20):
        floors = 4
    floor = utils.to_categorical(floor, 6)
    floors = utils.to_categorical(floors, 5)

    balconyVariants = ['Л', 'Б', '2Б', '-', '2Б2Л', 'БЛ', '3Б', '2Л', 'Эрк', 'Б2Л', 'ЭркЛ', '3Л', '4Л', '*Л', '*Б']

    if (balcon == balcon):
        balcon = balconyVariants.index(balcon)+1 #Находим индекс строки балкона во всех строках
    else:
        balcon = 0
    
    
    balcon = utils.to_categorical(balcon, 16)
  
    wcVariants = ['2', 'Р', 'С', '-', '2С', '+', '4Р', '2Р', '3С', '4С', '4', '3', '3Р']
    if (wc == wc):
        wc = wcVariants.index(wc)+1 
    else:
        wc = 0
    wc = utils.to_categorical(wc, 14)

    houseType = 0
    if (len(houseTypeStr) > 0):
        if ("М" in houseTypeStr): 
          houseType = 1
        if ("К" in houseTypeStr): 
          houseType = 2
        if ("П" in houseTypeStr): 
          houseType = 3
        if ("Б" in houseTypeStr): 
          houseType = 4
        if ("?" in houseTypeStr): 
          houseType = 5
        if ("-" in houseTypeStr): 
          houseType = 6
    houseType = utils.to_categorical(houseType, 7)
    


    out = list(roomsCount)
    out.extend(metroType)
    out.extend(distance)
    out.extend(floor)
    out.extend(floors)
    out.append(isLastFloor)
    out.extend(houseType)
    out.extend(balcon)
    out.extend(wc)
    out.append(int(area))

    xTrain = np.array(out)
    xTeach = np.load('./xTrain2.npy')
    yTeach = np.load('./yTrain2.npy')

    yScaler = StandardScaler() #Делаемнормальный нормировщик
    yScaler.fit(yTeach.reshape(-1, 1)) #Обучаем на ценах квартир


    xScaler = StandardScaler() #Создаём нормировщик нормальным распределением
    xScaler.fit(xTeach[:,-1].reshape(-1, 1)) #Обучаем его на площадях квартир (последня колонка в xTrain)
    xTrainScaled = xTrain.copy()
    xTrainScaled[-1] = xScaler.transform(xTrain[-1].reshape(1, -1)) #Нормируем данные нормировщиком
    yScaler = StandardScaler() #Делаемнормальный нормировщик
    yScaler.fit(yTeach.reshape(-1, 1)) #Обучаем на ценах квартир
    model = load_model("./neiroWeb2.h5")
    print(xTeach[0].shape)
    print(xTrainScaled)
    preds = model.predict([xTrainScaled[True]])
    predUnscaled = yScaler.inverse_transform(preds).flatten()
    return predUnscaled[0]