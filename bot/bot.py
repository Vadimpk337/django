import requests

from .models import User, Phone, Message, Information, Phone_operator, Comment
from freexel import settings

import requests
from bs4 import BeautifulSoup

import time


def wrap(data):
    try:
        chat_id = data['message']['chat']['id']
        telegram_id = data['message']['from']['id']
        first_name = data['message']['from']['first_name']
        date = data['message']['date']
        text = data['message']['text']

        save_message(telegram_id, chat_id, text, date)
        user, status = check_user_by_register(telegram_id, first_name)

        if text[0] == '?':
            send_message(chat_id, save_comment(telegram_id, text, date))

        elif text == '/res':
            send_message(chat_id, message_res()) 

        elif status == 'B':
            send_message(chat_id, message_B())

        elif text == '/start':
            if user is True:
                send_message(chat_id, '👋  Добро пожаловать! \n\n Используйте /help для получения информации.')
            else:
                send_message(chat_id, '🎉 С возвращением! \n\n Используйте /help для получения информации.')

        elif text == '/help':
            if status == 'U':
                send_message(chat_id, message_help_U())  
            if status == 'A':
                send_message(chat_id, message_help_A())


        elif text == '/comments':
            if status == 'A':
                perm_get_comments(chat_id)
            else: send_message(chat_id, 'Недостаточно прав!')

        elif text[:5] == '/send':
            if status == 'A':
                perm_send_message(text)
            else: send_message(chat_id, 'Недостаточно прав!')

        elif text == '/update':
            if status == 'A':
                perm_parse_7sot()
                send_message(chat_id, 'Обновление базы закончилось!') 
            else: send_message(chat_id, 'Недостаточно прав!')

        elif text == '/last':
            if status == 'A':
                perm_last_messages(chat_id, 10) 
            else: send_message(chat_id, 'Недостаточно прав!')

            

        elif normalize_phone(text) is not None and status != 'B':

            request = find_phone(normalize_phone(text))
            if request is not None:
                compose_message(chat_id, request)
                if request.IIN != '':
                    send_message(chat_id, get_info_by_iin(request.IIN))

            else: send_message(chat_id, 'Телефон не найден в базе!')
        elif len(text)== 12 and text[0] != '+' and status != 'B':
            request = find_information_by_IIN(text)
            if request is not None:
                compose_message(chat_id, request)
            send_message(chat_id, get_info_by_iin(text))

        else: send_message(chat_id, 'Неверный формат!')

    except KeyError: pass


def send_message(chat_id, text):
    send_result = requests.get(
        f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage',
        params={'chat_id': chat_id, 'text': text})


def check_user_by_register(telegram_id, first_name):
    user = User.objects.get_or_create(pk = telegram_id, first_name=first_name)
    return (user[1], user[0].status)

def save_message(telegram_id, chat_id, text, date):
    Message.objects.create(telegram_id=telegram_id, chat_id=chat_id, text=text, date=date)

def find_phone(phone):
    response = Information.objects.filter(phone__number=phone).first()
    if response is not None:
        return response
    else: return None

def find_information_by_IIN(text):
    response = Information.objects.filter(IIN=text).first()
    if response is not None:
        return response
    else: return None


def normalize_phone(phone):
    try:
        if phone is None:
            return None
        elif len(phone) == 12 and phone[0] == '+':
            if ' ' in phone:
                return normalize_phone(phone.replace(' ', ''))
            return phone
        elif len(phone) == 11:
            if phone[0] == '8':
                phone = '+7'+phone[1:]
                return phone
            elif phone[0] == '+':
                phone = '+7'+phone[1:]
                return phone
            else: 
                phone = '+'+phone
                return phone
        elif len(phone) == 10:
            phone = '+7'+phone
            return phone
        elif len(phone) == 9:
            phone = '+77'+phone
            return phone
        elif ' ' in phone:
            return normalize_phone(phone.replace(' ', ''))
        elif ' ' in phone:
            return normalize_phone(phone.replace(' ', ''))
        elif '-' in phone:
            return normalize_phone(phone.replace('-', ''))
        elif '–' in phone:
            return normalize_phone(phone.replace('–', ''))
        elif '(' or ')' in phone:
            return normalize_phone(phone.replace('(', '').replace(')', ''))
        else:
            print(f'{phone} - is not deformed!')    
            return None
    except RecursionError:
        return None

def compose_message(chat_id, data):

    text = f'🕵️  Найденная информация: \n\n'

    number = data.phone.number
    if number != '':
        text = text +'☎️   Номер: '+number+'\n\n'

    operator = data.phone.operator.title
    if operator != '':
        text = text +'🌐  Оператор: '+operator+'\n\n'

    country = data.phone.operator.country
    if operator != '':
        text = text +'🗺  Стана: '+country+'\n\n'

    IIN = data.IIN
    if IIN != '':
        text = text +'🇰🇿  ИИН: '+IIN+'\n\n'
        
    bio = data.bio
    if bio != '':
        text = text +'👽  Прочая информация: '+bio+'\n\n'

    first_name = data.first_name
    if first_name != '':
        text = text +'🙊  Имя: '+first_name+'\n\n'

    famaly_name = data.famaly_name
    if famaly_name != '':
        text = text +'👨‍👩‍👧‍👦  Фамилия: '+famaly_name+'\n\n'

    last_name = data.last_name
    if last_name != '':
        text = text +'👨‍👧‍👦  Отчество: '+last_name+'\n\n'

    email = data.email
    if email != '':
        text = text +'📩  Почта: '+email+'\n\n'
        
    birthday = data.birthday
    if birthday != '':
        text = text +'🎂  День рождения: '+birthday+'\n\n'

    city = data.city
    if city != '':
        text = text +'🏘  Город: '+city+'\n\n'

    
    send_message(chat_id, text)


def message_B():
    text = ' Вы являетесь заблокированным пользователем\
        \n\n у Вас нет доступа к командам бота!\
        \n\n Вы можете оставить обращение используя формат (?текст обращения)'


    return text
def message_help_U():
    text = ' Отправьте мне номер телефона, либо ИИН для поиска.\
        \n\n Формат телефона может быть любым. Можно использовать тире, пробелы, скобки\
        \n\n Формат ИИНа - 12 цифр без пробелов и тире'

    return text

def message_help_A():
    text = ' Команды администратора бота:\
        \n\n /comments - новые обращения\
        \n\n /update - обновить базу мошенников\
        \n\n /last - посмотреть последние 10 сообщений боту\
        \n\n /send ID текст - отправить сообщение пользователю'
    return text

def message_res():
    text = ' Чтобы задать вопрос, оставить отзыв или пожаловаться\
    \n\n используйте перед вашим сообщением знак вопроса ( ?ваше обращение ) '

    return text


def save_comment(telegram_id, text, date):
    user = User.objects.get(pk=telegram_id)
    comment = Comment.objects.create(user=user, description=text[1:], date=date)
    return f' Ваше обращение №{date} зарегистрировано.'



def get_info_by_iin(iin):
    url = f"https://pk.uchet.kz/p/iin/{iin}/full/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    info = []
    if 'info-value col' in page.text:
        
        for block in soup.find_all('div', class_='info-value col'):
            if block.text.replace('\n', '') != 'Нет':
                info.append(block.text.replace('\n', ''))
            else:
                continue

        text = '🕵️  Найденая информация по ИИНу:'
        for t in info:
            if len(t) == 12:
                continue
            if len(t) == 10 and len(t.split('.')) == 3:
                continue
            if 'лет' in t:
                t = f'Возвраст: {t}'
            if len(t.split(' ')) == 3:
                t = t.title()
            text += "\n\n  "+t
        return text

    else : return '😔 Информация по ИИНу не найдена.'


def perm_send_message(text):
    try:
        chat = text.split(' ')[1]
        text = text[text.index(chat)+len(chat):]
        send_message(chat, text)
    except IndexError: send_message(chat_id, 'Используй /send ID текст')


def perm_get_comments(chat_id):
    qs = Comment.objects.filter(completed=False)
    for query in qs:
        text = f'Обращение №{query.date}: {query.description}  \n~{query.user.first_name}'
        send_message(chat_id, text)


def perm_last_messages(chat_id, count):
    queryset = Message.objects.order_by('-date')[:count]
    messages = reversed(list(queryset))
    msg = 1
    for message in messages:
        text = f'{msg}| {message.text}'
        send_message(chat_id, text)
        msg += 1


def perm_parse_7sot():
    page_number = 1
    while True:
        print(f'Поиск номеров на странице {page_number}')

        page = requests.get(f'https://7sot.info/complaints?page={page_number}')
        soup = BeautifulSoup(page.text, "html.parser")
        counter = 0
        for block in soup.find_all('div', class_='p-5 bg-gray-500 text-white space-y-3 rounded'):

            gr = block.find('a', class_='mr-2 mb-2 md:mb-0 text-gray-800 bg-yellow-300 hover:bg-yellow-200 rounded py-1 px-2 inline-block').text.replace('  ', '').replace('\n', '')
            ph = block.find('a', class_='bg-gray-600 rounded px-2 py-1').text.replace(' ', '').replace('\n', '')

            gr = 'Найден в базе телефонных мошенников: '+gr
            operator = Phone_operator.objects.get_or_create(code=ph[:5])[0]
            phone = Phone.objects.get_or_create(number=ph, operator=operator)
            if phone[1] is True:
                counter += 1
                bio = Information.objects.update_or_create(bio=gr, phone=phone[0])

        page_number += 1  
        if counter < 6:
            break






    







