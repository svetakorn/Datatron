#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Содержит сообщения для взаимодействия с пользователем
"""

from json import dumps

CMD_START_MSG = "Вас приветствует экспертная система Datatron!"

TELEGRAM_START_MSG = '''Я – экспертная система Datatron😊 Со мной вы можете быстро получить доступ к финансовым данным как России в целом, так и любого ее региона.

Бот принимает запросы на естественном языке в формате текста и голоса.

*Текстовый режим*
Просто напишите ваш запрос на естественном языке. Если не знаете, какой задать вопрос, нажмите команду /idea!

*Голосовой режим*
Воспользуйтесь встроенной в Telegram записью голоса.'''

ABOUT_MSG = '''*Описание:*
Дататрон предоставляет пользователю доступ к открытым финансовым данным России и её субъектов.

*Функционал:*
Поиск экономических данных по запросу на естественном языке в текстовом и голосовом формате.

*Разработчики:*
Студенты Высшей школы экономики с факультетов Бизнес-информатики и Программной инженерии, а также студенты факультета ВМК МГУ, которые стараются изменить мир к лучшему.

*Обратная связь*
Для нас важно ваше мнение о работе Datatron. Вы можете оставить отзыв о боте, написав его через пробел после команды /fb, или нажав кнопку "Оценить".

*Дополнительно:*
Использует [Yandex SpeechKit Cloud](https://tech.yandex.ru/speechkit/cloud/).

Подробное описание функций доступно по команде /help.'''

ABOUT_KEYBOARD = dumps({
    'inline_keyboard': [
        [
            {'text': 'Оценить', 'url': 'https://telegram.me/storebot?start=datatron_bot'}
        ],
        [
            {'text': 'Ознакомительный ролик', 'callback_data': 'intro_video'}
        ]
    ]
})
    
HELP_MSG = '''*Список доступных команд при взаимодействии с ботом:*

/start - Начало работы
/help - Помощь
/idea - Вопросы, которые задавали другие пользователи
/fb - Оставить отзыв
/about - О проекте

Для поиска финансовой информации в базе достаточно просто сформулировать свой запрос и отправить его боту, например:
    
```
Внутренняя задолженность России
Долг странам Парижского договора в 2013 году```

Также бот понимает голосовые запросы – просто отправьте ему голосовое сообщение с интересующим вас вопросом – всё устроено точно так же, как и текстовое общение.
'''

RESPONSE_QUALITY = dumps({
    'inline_keyboard': [
        [
            {'text': '👍', 'callback_data': 'correct_response'},
            {'text': '😒', 'callback_data': 'incorrect_response'}
        ],
    ]
})

ERROR_CANNOT_UNDERSTAND_VOICE = 'Не удалось распознать текст сообщения😥 Попробуйте еще раз!'
ERROR_NULL_DATA_FOR_SUCH_REQUEST = 'К сожалению, этих данных в системе нет🤕'
ERROR_SERVER_DOES_NOT_RESPONSE = 'К сожалению, сейчас сервер не доступен😩 Попробуйте снова чуть позже!'
ERROR_NO_DOCS_FOUND = 'Datatron не нашел ответ на Ваш запрос :('

MSG_WE_WILL_FORM_DATA_AND_SEND_YOU = "Спасибо! Сейчас я сформирую ответ и отправлю его вам🙌"
MSG_NO_BUTTON_SUPPORT = 'Кнопочный режим более *не поддерживается*'
MSG_LEAVE_YOUR_FEEDBACK = 'Напишите после команды /fb ваш отзыв.\nНапример: `/fb Мне нравится, что...`'
MSG_WE_GOT_YOUR_FEEDBACK = 'Cпасибо! Ваш отзыв записан :)'
MSG_LOG_HISTORY_IS_EMPTY = 'Истории логов еще нет😔 Не растраивай Datatron, задай вопрос!'

# Constants for m2
ERROR_PARSING = 'Что-то пошло не так🙃 Проверьте ваш запрос на корректность'
ERROR_GENERAL = 'Что-то пошло не так🙃 Данные получить не удалось:('

# Список ключевых слов, которые служат триггером для ответа бота одной из фраз из кортежа HELLO_ANSWER
HELLO = ('хай', 'привет', 'здравствуйте', 'приветствую', 'прифки', 'дратути', 'hello')
HELLO_ANSWER = ('Привет! Начни работу со мной командой /search или сделай голосовой запрос',
                'Здравствуйте! Самое время ввести команду /search',
                'Приветствую!',
                'Здравствуйте! Пришли за финансовыми данными? Задайте мне вопрос!',
                'Доброго времени суток! С вами Datatron😊, и мы начинаем /search')

# Список ключевых слов, которые служат триггером для ответа бота одной из фраз из кортежа HOW_ARE_YOU_ANSWER
HOW_ARE_YOU = ('дела', 'поживаешь', 'жизнь')
HOW_ARE_YOU_ANSWER = ('У меня все отлично, спасибо :-)',
                      'Все хорошо! Дела идут в гору',
                      'Замечательно!',
                      'Бывало и лучше! Без твоих запросов только и делаю, что прокрастинирую🙈',
                      'Чудесно! Данные расходятся, как горячие пирожки! 😄')
