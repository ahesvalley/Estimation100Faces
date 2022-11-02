# -*- coding: utf-8 -*-
from cmath import nan
import numpy as np #Библиотека работы с массивами
import pandas as pd # Библиотека для работы с базами

from sklearn.preprocessing import StandardScaler 
from tensorflow.keras import utils #Используем для to_categoricall

df = pd.read_csv('./moscow.csv', sep=";") #Загружаем данные в data frame
df = df.iloc[::2,:]
print(df.head(20))
df = df[['Комнат', 'Метро / ЖД станции', 'От станции', 'Дом', 'Площадь', 'Цена, руб.', 'Балкон', 'Санузел']]
df = df.dropna()
print(df.head(20))
print(df.shape)
data = df.values

allRoomsCount = list(df['Комнат'].unique())
print(allRoomsCount)
def getRoomsCount(d, maxRoomCount):
  roomsCountStr = d[0] #Получаем строку с числом комнат

  roomsCount = 0
  try:
    roomsCount = int(roomsCountStr) #Пробуем превратить строку в число
    if (roomsCount > maxRoomCount): 
      roomsCount = maxRoomCount #Если число комнат больше максимального, то присваиваем максимальное
  except: #Если не получается превратить строку в число
    if (roomsCountStr == roomsCountStr): #Проверяем строку на nan (сравнение с самим собой)
      if ("Ст" in roomsCountStr): #Еcть строка = "Ст", значит это Студия
        roomsCount = maxRoomCount + 1

  return roomsCount

def getRoomsCountCategory(d, maxRoomCount):
  roomsCount = getRoomsCount(d, maxRoomCount) #Получаем число комнат
  roomsCount = utils.to_categorical(roomsCount, maxRoomCount+2) #Превращаем в категорию
  #maxRoomCount+2 потому что 0 зарезервирован на неопознаное число комнат, а maxRoomCount+1 на "Студию"
  return roomsCount

def getMetroType(d):
    metroTypeStr = d[1] #Получаем строку метро
    metroTypeClasses = 6 #Число классов метро
    metroType = metroTypeClasses - 1 #Изначально считаем последний класс
    try:
        metroTypeStr = metroTypeStr.split()
        if metroTypeStr[-1] == '(МЦК)': 
            metroTypeStr = " ".join(metroTypeStr[:-2])
        else: metroTypeStr = " ".join(metroTypeStr[:-1])
    except: 
        print(metroTypeStr)
    #Метро внутри кольца
    metroNamesInsideCircle = ["Китай-Город","Библиотека им.Ленина", "Площадь Революции", "Арбатская", "Смоленская", "Красные Ворота", "Красные ворота", "Чистые пруды", "Лубянка", "Охотный Ряд", "Охотный ряд", "Библиотека имени Ленина", "Кропоткинская", "Сухаревская", "Тургеневская", "Китай-город", "Китай-Город" "Третьяковская", "Трубная", "Сретенский бульвар", "Цветной бульвар", "Чеховская", "Боровицкая", "Полянка", "Маяковская", "Тверская", "Театральная", "Новокузнецкая", "Пушкинская", "Кузнецкий Мост", "Кузнецкий мост", "Китай-город", "Александровский сад", "Александровский Сад"]
    #Метро на кольце
    metroNamesCircle = ["Баррикадная", "Марксистская", "Чкаловская", "Менделеевская", "Киевская", "Парк Культуры", "Парк культуры", "Октябрьская", "Добрынинская", "Павелецкая", "Таганская", "Курская", "Комсомольская", "Проспект Мира", "Новослободская", "Белорусская", "Краснопресненская", "Серпуховская"]
    #Метро 1-3 станции от кольца
    metroNames13FromCircle = ["Улица 1905 года", "Лужники", "Москва-Товарная", "Бауманская", "Электрозаводская", "Семеновская", "Площадь Ильича", "Авиамоторная", "Шоссе Энтузиастов", "Римская", "Крестьянская Застава", "Дубровка", "Пролетарская", "Волгоградский проспект", "Текстильщики", "Автозаводская", "Технопарк", "Коломенская", "Тульская", "Нагатинская", "Нагорная", "Шаболовская", "Ленинский проспект", "Академическая", "Фрунзенская", "Спортивная", "Воробьевы горы", "Воробьевы Горы", "Студенческая", "Кутузовская", "Фили", "Парк Победы", "Выставочная", "Международная", "Улица 1905", "улица 1905", "Беговая", "Полежаевская", "Динамо", "Петровский Парк", "Аэропорт (старая)", "Аэропорт", "Сокол", "Деловой центр", "Хорошевская", "ЦСКА", "Петровский парк", "Савеловская", "Дмитровская", "Тимирязевская", "Достоевская", "Марьина Роща", "Марьина роща", "Бутырская", "Фонвизинская", "Рижская", "Алексеевская", "ВДНХ", "Красносельская", "Сокольники", "Преображенская площадь", "Калитники", "Новохохловская", "Минская", "Славянский бульвар"]
    #Метро 4-8 станций от кольа
    metroNames48FromCircle = ["Каховская", "Перерва", "Новаторская", "Депо", "Румянцево", "Юго-Западная", "Народное ополчение", "Проспект Вернадского", "Говорово", "Лефортово", "Мневники", "Строгино", "Лианозово", "Нахимовский проспект", "Красный Балтиец", "Бескудниково", "Москворечье", "Домодедовская", "Озерная", "Раменки", "Крылатское", "Аминьевская", "Мякинино", "Стахановская", "Тестовская", "Зорге", "Ростокино", "ЗИЛ", "Партизанская", "Измайловская", "Первомайская", "Щелковская", "Новокосино", "Новогиреево", "Перово", "Кузьминки", "Рязанский проспект", "Выхино", "Лермонтовский проспект", "Жулебино", "Партизанская", "Измайловская", "Первомайская", "Щелковская", "Новокосино", "Новогиреево", "Перово", "Кузьминки", "Рязанский проспект", "Выхино", "Лермонтовский проспект", "Жулебино", "Улица Дмитриевского", "улица Дмитриевского", "Кожуховская", "Печатники", "Волжская", "Люблино", "Братиславская", "Коломенская", "Каширская", "Кантемировская", "Царицыно", "Орехово", "Севастопольская", "Чертановская", "Южная", "Пражская", "Варшавская", "Профсоюзная", "Новые Черемушки", "Калужская", "Беляево", "Коньково", "Университет", "Багратионовская", "Филевский парк", "Пионерская", "Кунцевская", "Молодежная", "Октябрьское Поле", "Октябрьское поле", "Щукинская", "Спартак", "Тушинская", "Сходненская", "Войковская", "Стрешнево", "Панфиловская", "Балтийская", "Водный стадион", "Речной вокзал", "Беломорская", "Ховрино", "Петровско-Разумовская", "Владыкино", "Отрадное", "Бибирево", "Алтуфьево", "Фонвизинская", "Окружная", "Верхние Лихоборы", "Селигерская", "ВДНХ", "Ботанический сад", "Свиблово", "Бабушкинская", "Медведково", "Преображенская площадь", "Черкизовская", "Бульвар Рокоссовского", "Воронцовская", "Терехово", "Угрешская", "Мичуринский проспект", "Давыдково", "Ломоносовский проспект"]
    #Метро 9+ станций от кольа
    metroNames9AndMoreFromCircle = ["Алма-Атинская", "Бульвар Адмирала Ушакова", "Силикатная", "Новоясеневская", "Новопеределкино", "Улица Скобелевская", "Улица Старокачаловская", "Красный Строитель", "Нахабино","Щербинка", "Филатов Луг", "Сколково", "Окская", "Пятницкое шоссе", "Юго-Восточная", "Курьяново", "Марьино", "Некрасовка", "Саларьево", "Рассказовка", "Боровское шоссе", "Сетунь", "Митино", "Теплый Стан","Бутово", "Улица Горчакова", "Лесопарковая", "Шипиловская", "Зябликово", "Бульвар Дмитрия","Марк", "Трикотажная", "Аннино","Бунинская Аллея", "Бунинская аллея", "Коммунарка", "Ольховая", "Долгопрудная", "Улица Академика", "улица Академика", "Бульвар Адмирала", "Прокшино"]
    MCCNames = ["Окружная", "Владыкино", "Ботанический сад", "Ростокино", "Белокаменная", "Бульвар Рокоссовского", "Локомотив", "Измайлово", "Соколиная Гора", "Шоссе Энтузиастов", "Андроновка", "Нижегородская", "Новохохловская", "Угрешская", "Дубровка", "Автозаводская", "ЗИЛ", "Верхние Котлы", "Верхние котлы", "Крымская", "Площадь Гагарина", "Лужники", "Кутузовская", "Деловой центр", "Шелепиха", "Хорошево", "Зорге", "Панфиловская", "Стрешнево", "Балтийская", "Коптево", "Лихоборы"]
    
    if (metroTypeStr in metroNamesInsideCircle):
        metroType = 0
    if (metroTypeStr in metroNamesCircle):
        metroType = 1
    if (metroTypeStr in metroNames13FromCircle):
        metroType = 2
    if (metroTypeStr in metroNames48FromCircle):
        metroType = 3
    if (metroTypeStr in MCCNames):
        metroType = 4
    if (metroTypeStr in metroNames9AndMoreFromCircle):
        metroType = 5
    #Превращаем результат в категорию
    metroType = utils.to_categorical(metroType, metroTypeClasses)
    return metroType

#Вычисляем растояние до метро
def getMetroDistance(d):
    metroDistanceStr = d[2] #Получаем строку

    metroDistance = 0 #Расстояние до метро
    metroDistanceType = 0 #Тип расстояния - пешком или на транспорте

    #ЕСли строка не равна nan  
    if (metroDistanceStr == metroDistanceStr):
        if (len(metroDistanceStr) > 0):
            #Определяем тип расстояния
            if (metroDistanceStr[-1] == "п"):
                metroDistanceType = 1 #Пешком
            elif (metroDistanceStr[-1] == "т"):
                metroDistanceType = 2 #На транспорте

        #Выбрасываем последний символ, чтобы осталось только число
        metroDistanceStr = metroDistanceStr[:-1]
        try:
        #Разделяем дистанции на категории
            metroDistance = int(metroDistanceStr)
            if (metroDistance < 3):
                metroDistance = 1
            elif (metroDistance < 6):
                metroDistance = 2
            elif (metroDistance < 10):
                metroDistance = 3
            elif (metroDistance < 15):
                metroDistance = 4
            elif (metroDistance < 20):
                metroDistance = 5
            else:
                metroDistance = 6
        except: #Если в строке не число, то категория 0
            metroDistance = 0

    #Число классов дистанции
    metroDistanceClasses = 7

    #У нас 7 категорий дистанции по расстоянию
    #И 3 типа дистанции - неопознанный, пешком и транспортом
    #Мы создадим вектор длины 3*7 = 21
    #Будем преобразовывать индекс расстояния 0-6 в 0-20
    #Для типа "Пешком" - ничего не меняем
    if (metroDistanceType == 2):
        metroDistance += metroDistanceClasses #Для типа "Транспортом" добавляем 7
    if (metroDistanceType == 0):
        metroDistance += 2*metroDistanceClasses #Для неопознанного типа добавляем 14

    #Превращаем в категории
    metroDistance = utils.to_categorical(metroDistance, 3*metroDistanceClasses)
    return metroDistance

def getHouseTypeAndFloor(d):
  try:
    houseStr = d[3] #Получаем строку типа дома и этажей
  except:
    houseStr = ""
  
  houseType = 0 #Тип дома
  floor = 0 #Этаж квартиры
  floors = 0 #Этажность дома
  isLastFloor = 0 #Индикатор последнего этажа
  
  #Проверяем строку на nan
  if (houseStr == houseStr):
    if (len(houseStr) > 1):
    
      try:
        slashIndex = houseStr.index("/") #Ищем разделитель /
      except:
        print(houseStr)

      try:
        spaceIndex = houseStr.index(" ") #Ищем разделитель " "
      except:
        print(houseStr)

      #Вытаскиваем строки
      floorStr = houseStr[:slashIndex] #Строка этажа
      floorsStr = houseStr[slashIndex+1:spaceIndex] #Строка этажнгости дома
      houseTypeStr = houseStr[spaceIndex+1:] #Строка типа дома

      #Выбираем категорию этажа
      try:
        floor = int(floorStr) #Превращаем строку в число
        floorSave = floor
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
      except:
        floor = 0 #Если строка не парсится в число, то категория этажа = 0 (отдельная)

      #Выбираем категорию этажности дома
      try:
        floors = int(floorsStr) #Превращаем строку в число
        floorsSave = floors
        if (floorsSave < 5):
          floors = 1
        if (floorsSave < 10):
          floors = 2
        if (floorsSave < 20):
          floors = 3
        if (floorsSave >= 20):
          floors = 4
      except:
        floors = 0 #Если строка не парсится в число, то категория этажности = 0 (отдельная)

      #Определяем категорию типа дома
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
    
    #Превращаем все категории в one hot encoding
    floor = utils.to_categorical(floor, 6)
    floors = utils.to_categorical(floors, 5)
    houseType = utils.to_categorical(houseType, 7)
    
    
  return floor, floors, isLastFloor, houseType

#Определяем площадь
def getArea(d):
  areaStr = d[4] #Поулачем строку площади
  
  if ("/" in areaStr):
    slashIndex = areaStr.index("/") #Находим разделитель /
    try:
      area = float(areaStr[:slashIndex]) #Берём число до разделителя и превращаем в число
    except:
      area = 0 #Если не получается, возвращаем 0
  else:
    area = 0 #Или если нет разделителя, возвращаем 0
    
  return area

#Полуаем цену
def getCost(d):
  costStr = d[5] #Загружаем строку
  
  try:
    cost = float(costStr) #Пробуем превратить в число
  except:
    cost = 0 #Если не получается, возвращаем 0
  
  return (cost * 1.44)

#Вычисляем тип балкона
def getBalcon(d):
  balconyStr = d[6] #Полуаем строку

  balconyVariants = ['Л', 'Б', '2Б', '-', '2Б2Л', 'БЛ', '3Б', '2Л', 'Эрк', 'Б2Л', 'ЭркЛ', '3Л', '4Л', '*Л', '*Б']

  if (balconyStr == balconyStr):
    balcony = balconyVariants.index(balconyStr)+1 #Находим индекс строки балкона во всех строках
  else:
    balcony = 0
  
 
  balcony = utils.to_categorical(balcony, 16)
  
  return balcony

def getWC(d):
  wcStr = d[7] #Получаем строку
  #Выписываем все варианты санузлов в базе
  wcVariants = ['2', 'Р', 'С', '-', '2С', '+', '4Р', '2Р', '3С', '4С', '4', '3', '3Р']
  #Проверяем на nan
  if (wcStr == wcStr):
    wc = wcVariants.index(wcStr)+1 #Находим индекс строки санузла во всех строках
  else:
    wc = 0 #Индекс 0 выделяем на строку nan
  
  #Превращаем в one hot encoding
  wc = utils.to_categorical(wc, 14)
  
  return wc

#Объединяем все числовые параметры вместе
def getAllParameters(d):
  #Загружаем все данные по отдельности
  roomsCountType = getRoomsCountCategory(d, 3)
  metroType = getMetroType(d)
  metroDistance = getMetroDistance(d)
  floor, floors, isLastFloor, houseType = getHouseTypeAndFloor(d)
  area = getArea(d)
  balcon = getBalcon(d)
  wc = getWC(d)

  #Объединяем в один лист
  out = list(roomsCountType)
  out.extend(metroType)
  out.extend(metroDistance)
  out.extend(floor)
  out.extend(floors)
  out.append(isLastFloor)
  out.extend(houseType)
  out.extend(balcon)
  out.extend(wc)
  out.append(area)
  
  return out

#Генерируем обучающаюу выборку - xTrain
def getXTrain(data):
  
  #Получаем строку во всеми вариантами метро
  
  #Всевращаем все строки в data1 в векторы параметров и записываем в xTrain
  xTrain = [getAllParameters(d) for d in data]
  xTrain = np.array(xTrain)
  
  return xTrain

#Генерируем обучающую выборку - yTrain
def getYTrain(data):
  
  #Зашружаем лист всех цен квартир по всем строкам data1
  costList = [getCost(d) for d in data] 
  yTrain = np.array(costList)
  
  return yTrain

oneRoomMask = [getRoomsCount(d, 3) == 1 for d in data] #Делаем маску однокомнатных квартир, принцип (getRoomsCount(d, 30) == 1)
data1 = data[oneRoomMask] #В data1 оставляем только однокомнатные квартиры
print(data.shape)
print(data1.shape)

xTrain = getXTrain(data1)
yTrain = getYTrain(data1)

np.save('C:/Users/egora/OneDrive/Рабочий стол/Образование/МАгистратура/Диссертация/проект Нейронной сети/xTrain2',xTrain)
np.save('C:/Users/egora/OneDrive/Рабочий стол/Образование/МАгистратура/Диссертация/проект Нейронной сети/yTrain2',yTrain)