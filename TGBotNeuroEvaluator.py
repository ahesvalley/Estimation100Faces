# -*- coding: utf-8 -*-
from matplotlib.pyplot import text
import telebot
from telebot import types
from cmath import nan
import numpy as np #Библиотека работы с массивами
import pandas as pd # Библиотека для работы с базами
from readExcel import readExcel

from sklearn.preprocessing import StandardScaler 
from tensorflow.keras import utils #Используем для to_categoricallS
from keras.models import load_model
from tensorflow.keras.layers import Input
from estimate import estimation
from tokens import botToken as token

bot = telebot.TeleBot(token)
rooms = 0
metro = ''
metroDistance = 0
floor = 0
floors = 0
area = 0
isLastFloor = 0
balcon = ''
wc = ''
houseType = ''
listOfBalcon = {'Лоджия':'Л', 'Балкон':'Б'}
listOfWC = {'Раздельный':'Р', 'Совмещенный':'С'}
listOfHouseType = {'Монолитный':'М', 'Кирпичный':'К', 'Панельный':'П', 'Не знаю':'-'}
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Привет, давайте оценим квартиру?'
    if message.text.lower() == "/start":
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напишите /start")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
@bot.callback_query_handler(func=lambda call: call.data == 'go')
def addButtons(call):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Шаг назад")
    item2 = types.KeyboardButton("Начать заново")	
    item3 = types.KeyboardButton("Закончить")	
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.send_message(call.message.chat.id, text='Начнем. Напишите количество комнат в квартире.', reply_markup=markup)
    bot.register_next_step_handler(call.message, askRooms)

@bot.callback_query_handler(func=lambda call: call.data == 'oneFlat' or call.data == 'uploadFile')
def chooseVariant(call):
    if call.data == "oneFlat":
        keyboard = types.InlineKeyboardMarkup();
        go = types.InlineKeyboardButton(text='Далее', callback_data='go');
        keyboard.add(go)
        bot.send_message(call.message.chat.id, text='Всегда можешь начать заново, нажав на кнопку', reply_markup=keyboard)
    elif call.data == "uploadFile":
        # bot.send_message(call.message.chat.id, 'Пока работаем над этим.')
        bot.send_message(call.message.chat.id, text="Загрузите файл по шаблону")
        with open('./6 задача_пример расчета.xlsx', "rb") as file:
            bot.send_document(call.message.chat.id, document=file)
        bot.register_next_step_handler(call.message, uploadFile)

@bot.callback_query_handler(func=lambda call: call.data == 'yes' or call.data == 'no')
def isEstimate(call):
    if call.data == "yes":
        keyboard = types.InlineKeyboardMarkup();
        oneFlat = types.InlineKeyboardButton(text='Ввести данные вручную', callback_data='oneFlat'); #кнопка «Да»
        keyboard.add(oneFlat);
        upload= types.InlineKeyboardButton(text='Загрузить файл', callback_data='uploadFile')
        keyboard.add(upload)
        question = 'Выберите вариант'
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Дай знать, как буду нужен')

@bot.callback_query_handler(func=lambda call: call.data == 'walk' or call.data == 'drive')
def walkOrDrive(call):
    global metroDistance
    if call.data == "walk":
        metroDistance = 'п'
        bot.send_message(call.message.chat.id, 'Сколько минут занимает путь до метро?')
        bot.register_next_step_handler(call.message, askDistance)
    elif call.data == "drive":
        metroDistance = 'т'
        bot.send_message(call.message.chat.id, 'Сколько минут занимает путь до метро?')
        bot.register_next_step_handler(call.message, askDistance)

@bot.callback_query_handler(func=lambda call: call.data in listOfHouseType.values())
def askHouseType(call):
    global houseType
    houseType = call.data
    keyboard = types.InlineKeyboardMarkup()
    for k,v in listOfWC.items():
        wc = types.InlineKeyboardButton(text=k, callback_data=v)
        keyboard.add(wc)
    bot.send_message(call.message.chat.id, text='Выберите тип санузла', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in listOfWC.values())
def askWC(call):
    global wc
    wc = call.data
    keyboard = types.InlineKeyboardMarkup()
    for k,v in listOfBalcon.items():
        balcon = types.InlineKeyboardButton(text=k, callback_data=v)
        keyboard.add(balcon)
    bot.send_message(call.message.chat.id, text='Выберите тип балкона', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in listOfBalcon.values())
def askBalkon(call):    
    global balcon
    balcon = call.data
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='right'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='wrong')
    keyboard.add(key_no)
    bot.send_message(call.message.chat.id, f'Итоговые данные: ')
    bot.send_message(call.message.chat.id, f'Комнат: {rooms},')
    bot.send_message(call.message.chat.id, f'Ближайшее метро: {metro}')
    bot.send_message(call.message.chat.id, f'Путь до метро: {metroDistance}')
    bot.send_message(call.message.chat.id, f'Этаж: {floor} из {floors}')
    bot.send_message(call.message.chat.id, f'Площадь: {area}')
    bot.send_message(call.message.chat.id, f'Площадь: {houseType}')
    bot.send_message(call.message.chat.id, f'Санузел: {wc}')
    bot.send_message(call.message.chat.id, f'Балкон {balcon}')
    bot.send_message(call.message.chat.id, f'Все верно?', reply_markup=keyboard)
        


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global isLastFloor
    if call.data == "right" :
        if (floor == floors):
            isLastFloor = 1
        print([rooms, metro,metroDistance,floor,floors,area,isLastFloor,wc,balcon, houseType])
        predUnscaled = estimation(1, metro,metroDistance,floor,floors,area,isLastFloor,wc,balcon, houseType)
        bot.send_message(call.message.chat.id, text=f'Стоимость квартиры: {predUnscaled} рублей')
        bot.send_message(call.message.chat.id, text='Начнем заново, /start', reply_markup=types.ReplyKeyboardRemove())
    elif call.data == "wrong":
        bot.send_message(call.message.chat.id, text='Начнем заново, /start', reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(content_types=['text'])
def askRooms (message):
    global rooms
    text = message.text
    if text.isdigit():
        if int(text) < 6:
            rooms = text
            bot.send_message(message.from_user.id, "Напишите ближайшее метро.")
            bot.register_next_step_handler(message, askMetro)
        else: 
            bot.send_message(message.from_user.id, "Слишком много.")
            bot.register_next_step_handler(message, askRooms)
            return
    elif text == "Начать заново":
        again(message)
    elif text == "Шаг назад":
        again(message)
    elif text == "Закончить":
        bot.send_message(message.from_user.id, 'Дай знать, как буду нужен, /start', reply_markup=types.ReplyKeyboardRemove()) 
    else: 
        bot.send_message(message.from_user.id, "Некорректно. Цифрами, пожалуйста.")
        bot.register_next_step_handler(message, askRooms)

def askMetro (message) :
    global metro
    text = message.text

    metroNamesInsideCircle = ["Китай-Город","Библиотека им.Ленина", "Площадь Революции", "Арбатская", "Смоленская", "Красные Ворота", "Красные ворота", "Чистые пруды", "Лубянка", "Охотный Ряд", "Охотный ряд", "Библиотека имени Ленина", "Кропоткинская", "Сухаревская", "Тургеневская", "Китай-город", "Китай-Город" "Третьяковская", "Трубная", "Сретенский бульвар", "Цветной бульвар", "Чеховская", "Боровицкая", "Полянка", "Маяковская", "Тверская", "Театральная", "Новокузнецкая", "Пушкинская", "Кузнецкий Мост", "Кузнецкий мост", "Китай-город", "Александровский сад", "Александровский Сад"]
    metroNamesCircle = ["Баррикадная", "Марксистская", "Чкаловская", "Менделеевская", "Киевская", "Парк Культуры", "Парк культуры", "Октябрьская", "Добрынинская", "Павелецкая", "Таганская", "Курская", "Комсомольская", "Проспект Мира", "Новослободская", "Белорусская", "Краснопресненская", "Серпуховская"]
    metroNames13FromCircle = ["Улица 1905 года", "Лужники", "Москва-Товарная", "Бауманская", "Электрозаводская", "Семеновская", "Площадь Ильича", "Авиамоторная", "Шоссе Энтузиастов", "Римская", "Крестьянская Застава", "Дубровка", "Пролетарская", "Волгоградский проспект", "Текстильщики", "Автозаводская", "Технопарк", "Коломенская", "Тульская", "Нагатинская", "Нагорная", "Шаболовская", "Ленинский проспект", "Академическая", "Фрунзенская", "Спортивная", "Воробьевы горы", "Воробьевы Горы", "Студенческая", "Кутузовская", "Фили", "Парк Победы", "Выставочная", "Международная", "Улица 1905", "улица 1905", "Беговая", "Полежаевская", "Динамо", "Петровский Парк", "Аэропорт (старая)", "Аэропорт", "Сокол", "Деловой центр", "Хорошевская", "ЦСКА", "Петровский парк", "Савеловская", "Дмитровская", "Тимирязевская", "Достоевская", "Марьина Роща", "Марьина роща", "Бутырская", "Фонвизинская", "Рижская", "Алексеевская", "ВДНХ", "Красносельская", "Сокольники", "Преображенская площадь", "Калитники", "Новохохловская", "Минская", "Славянский бульвар"]
    metroNames48FromCircle = ["Каховская", "Перерва", "Новаторская", "Депо", "Румянцево", "Юго-Западная", "Народное ополчение", "Проспект Вернадского", "Говорово", "Лефортово", "Мневники", "Строгино", "Лианозово", "Нахимовский проспект", "Красный Балтиец", "Бескудниково", "Москворечье", "Домодедовская", "Озерная", "Раменки", "Крылатское", "Аминьевская", "Мякинино", "Стахановская", "Тестовская", "Зорге", "Ростокино", "ЗИЛ", "Партизанская", "Измайловская", "Первомайская", "Щелковская", "Новокосино", "Новогиреево", "Перово", "Кузьминки", "Рязанский проспект", "Выхино", "Лермонтовский проспект", "Жулебино", "Партизанская", "Измайловская", "Первомайская", "Щелковская", "Новокосино", "Новогиреево", "Перово", "Кузьминки", "Рязанский проспект", "Выхино", "Лермонтовский проспект", "Жулебино", "Улица Дмитриевского", "улица Дмитриевского", "Кожуховская", "Печатники", "Волжская", "Люблино", "Братиславская", "Коломенская", "Каширская", "Кантемировская", "Царицыно", "Орехово", "Севастопольская", "Чертановская", "Южная", "Пражская", "Варшавская", "Профсоюзная", "Новые Черемушки", "Калужская", "Беляево", "Коньково", "Университет", "Багратионовская", "Филевский парк", "Пионерская", "Кунцевская", "Молодежная", "Октябрьское Поле", "Октябрьское поле", "Щукинская", "Спартак", "Тушинская", "Сходненская", "Войковская", "Стрешнево", "Панфиловская", "Балтийская", "Водный стадион", "Речной вокзал", "Беломорская", "Ховрино", "Петровско-Разумовская", "Владыкино", "Отрадное", "Бибирево", "Алтуфьево", "Фонвизинская", "Окружная", "Верхние Лихоборы", "Селигерская", "ВДНХ", "Ботанический сад", "Свиблово", "Бабушкинская", "Медведково", "Преображенская площадь", "Черкизовская", "Бульвар Рокоссовского", "Воронцовская", "Терехово", "Угрешская", "Мичуринский проспект", "Давыдково", "Ломоносовский проспект"]
    metroNames9AndMoreFromCircle = ["Алма-Атинская", "Бульвар Адмирала Ушакова", "Силикатная", "Новоясеневская", "Новопеределкино", "Улица Скобелевская", "Улица Старокачаловская", "Красный Строитель", "Нахабино","Щербинка", "Филатов Луг", "Сколково", "Окская", "Пятницкое шоссе", "Юго-Восточная", "Курьяново", "Марьино", "Некрасовка", "Саларьево", "Рассказовка", "Боровское шоссе", "Сетунь", "Митино", "Теплый Стан","Бутово", "Улица Горчакова", "Лесопарковая", "Шипиловская", "Зябликово", "Бульвар Дмитрия","Марк", "Трикотажная", "Аннино","Бунинская Аллея", "Бунинская аллея", "Коммунарка", "Ольховая", "Долгопрудная", "Улица Академика", "улица Академика", "Бульвар Адмирала", "Прокшино"]
    MCCNames = ["Окружная", "Владыкино", "Ботанический сад", "Ростокино", "Белокаменная", "Бульвар Рокоссовского", "Локомотив", "Измайлово", "Соколиная Гора", "Шоссе Энтузиастов", "Андроновка", "Нижегородская", "Новохохловская", "Угрешская", "Дубровка", "Автозаводская", "ЗИЛ", "Верхние Котлы", "Верхние котлы", "Крымская", "Площадь Гагарина", "Лужники", "Кутузовская", "Деловой центр", "Шелепиха", "Хорошево", "Зорге", "Панфиловская", "Стрешнево", "Балтийская", "Коптево", "Лихоборы"]
    metroList = metroNamesInsideCircle + metroNamesCircle + metroNames13FromCircle + metroNames48FromCircle + metroNames9AndMoreFromCircle + MCCNames
    metroList = [x.lower() for x in metroList]
    if text == "Начать заново":
        again(message)
    elif text == "Шаг назад":
        bot.send_message(message.from_user.id, "Сколько комнат в квартире?")
        bot.register_next_step_handler(message, askRooms)
    elif text == "Закончить":
        bot.send_message(message.from_user.id, 'Дай знать, как буду нужен, /start', reply_markup=types.ReplyKeyboardRemove()) 
    elif text.lower() not in metroList:
        bot.send_message(message.from_user.id, "Такого метро нет в нашей базе.")
        bot.register_next_step_handler(message, askMetro)
    else:
        keyboard = types.InlineKeyboardMarkup();
        key_yes = types.InlineKeyboardButton(text='пешком', callback_data='walk');
        keyboard.add(key_yes);
        key_no= types.InlineKeyboardButton(text='на транспорте', callback_data='drive')
        keyboard.add(key_no)
        question = 'Как вы добираетесь до метро?'
        metro = message.text
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
def askDistance(message):
    global metroDistance
    text = message.text
    if text == "Начать заново":
        again(message)
    elif text == "Шаг назад":
        bot.send_message(message.from_user.id, "Напишите ближайшее метро.")
        bot.register_next_step_handler(message, askMetro)
    elif text == "Закончить":
        bot.send_message(message.from_user.id, 'Дай знать, как буду нужен, /start', reply_markup=types.ReplyKeyboardRemove()) 
    elif text.isdigit():
        metroDistance = text + metroDistance 
        bot.send_message(message.from_user.id, 'На каком этаже находится квартира?')
        bot.register_next_step_handler(message, askFloor)
    else: 
        bot.send_message(message.from_user.id, "Некорректно. Цифрами, пожалуйста.")
        bot.register_next_step_handler(message, askDistance)

def askFloor(message):
    global floor
    text = message.text
    if text == "Начать заново":
        again(message)
    elif text == "Шаг назад":
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_yes = types.InlineKeyboardButton(text='пешком', callback_data='walk'); #кнопка «Да»
        keyboard.add(key_yes); #добавляем кнопку в клавиатуру
        key_no= types.InlineKeyboardButton(text='на транспорте', callback_data='drive')
        keyboard.add(key_no)
        question = 'Как вы добираетесь до метро?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    elif text == "Закончить":
        bot.send_message(message.from_user.id, 'Дай знать, как буду нужен, /start', reply_markup=types.ReplyKeyboardRemove()) 
    elif text.isdigit():
        floor = text 
        bot.send_message(message.from_user.id, 'Сколько всего этажей?')
        bot.register_next_step_handler(message, askFloors)
    else: 
        bot.send_message(message.from_user.id, "Некорректно. Цифрами, пожалуйста.")
        bot.register_next_step_handler(message, askFloor)

def askFloors(message):
    global floors
    text = message.text
    if text == "Начать заново":
        again(message)
    elif text == "Шаг назад":
        bot.send_message(message.from_user.id, "На каком этаже находится квартира?")
        bot.register_next_step_handler(message, askFloor)
    elif text == "Закончить":
        bot.send_message(message.from_user.id, 'Дай знать, как буду нужен, /start', reply_markup=types.ReplyKeyboardRemove()) 
    elif text.isdigit():
        if int(floor) > int(message.text):
            bot.send_message(message.from_user.id, "Да ладно?")
            bot.send_message(message.from_user.id, 'Сколько всего этажей?')
            bot.register_next_step_handler(message, askFloors)
        else:
            floors = text 
            bot.send_message(message.from_user.id, 'Какая площадь квартиры м2?')
            bot.register_next_step_handler(message, askArea)
    else: 
        bot.send_message(message.from_user.id, "Некорректно. Цифрами, пожалуйста.")
        bot.register_next_step_handler(message, askFloors)

def askArea(message):
    global area
    text = message.text
    if text == "Начать заново":
        again(message)
    elif text == "Шаг назад":
        bot.send_message(message.from_user.id, "Сколько всего этажей?")
        bot.register_next_step_handler(message, askFloors)
    elif text == "Закончить":
        bot.send_message(message.from_user.id, 'Дай знать, как буду нужен, /start', reply_markup=types.ReplyKeyboardRemove()) 
    elif text.isdigit():
        area = text
        keyboard = types.InlineKeyboardMarkup()
        for k,v in listOfHouseType.items():
            houseType = types.InlineKeyboardButton(text=k, callback_data=v)
            keyboard.add(houseType)
        bot.send_message(message.from_user.id, text='Выберите тип дома', reply_markup=keyboard)
    else: 
        bot.send_message(message.from_user.id, "Некорректно. Цифрами, пожалуйста.")
        bot.register_next_step_handler(message, askArea)



# def modelling(message):
# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
def again(message):
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    oneFlat = types.InlineKeyboardButton(text='Ввести данные вручную', callback_data='oneFlat'); #кнопка «Да»
    keyboard.add(oneFlat); #добавляем кнопку в клавиатуру
    upload= types.InlineKeyboardButton(text='Загрузить файл', callback_data='uploadFile')
    keyboard.add(upload)
    question = 'Выберите вариант'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.message_handler(content_types=['document'])
def uploadFile(message):
    # try:
    chat_id = message.chat.id

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    print(file_info.file_path)
    src = f'./{message.document.file_name}';
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Обрабатываем")
    l = readExcel(src)
    predUnscaled = estimation(l['rooms'], l['metro'], l['metroDistance'], l['floor'], l['floors'], l['area'], l['isLastFloor'], l['wc'], l['balcon'], l['houseType'])
    bot.reply_to(message, text=f'Стоимость квартиры: {predUnscaled} рублей')
    # except Exception as e:
    #     bot.reply_to(message, f'ошибка {e}')
    
bot.polling(none_stop=True, interval=0)

