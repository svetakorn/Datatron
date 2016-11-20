from json import dumps

CMD_START_MSG = '''
Вас приветствует экспертная система Datatron!'''

TELEGRAM_START_MSG = '''
Я - экспертная система Datatron😊 Со мной вы можете быстро получить доступ к финансовым данным как России в целом, так и любого ее региона.

Бот поддерживает три режима работы: запрос на естественном языке в формате текста и голоса, а также inline-режим.

<b>Текстовый режим</b>
После команды /search через пробел напишите ваш запрос. Наример:
<code>/search расходы Москвы на спорт в 2013 году
/search дефицит Ярославской области</code>

<b>Голосовой режим</b>
Воспользуйтесь встроенной в Telegram записью голоса.'''
HELP_MSG = '''<b>Описание:</b>
Дататрон предоставляет пользователю доступ к открытым финансовым данным России и её субъектов.

<b>Функционал:</b>
Доступны inline-режим, ввод на естественном языке в текстовом и голосовом формате.

<b>Разработчики:</b>
Студенты Высшей школы экономики с факультетов Бизнес-информатики и Программной инженерии, которые стараются изменить мир к лучшему.

<b>Обратная связь</b>
Для нас важно ваше мнение о работе Datatron. Вы можете оставить отзыв о боте, написав на почту datatron.bot@gmail.com или нажав кнопку "Оценить".

<b>Дополнительно:</b>
Использует <a href="https://tech.yandex.ru/speechkit/cloud/">Yandex SpeechKit Cloud</a>.'''
HELP_KEYBOARD = dumps({
    'inline_keyboard': [
        [
            {'text': 'Inline-режим', 'callback_data': '',
             'switch_inline_query': 'расходы Ростовской области на социальную политику в прошлом году'},
            {'text': 'Оценить', 'url': 'https://telegram.me/storebot?start=datatron_bot'}
        ],
        [
            {'text': 'Руководство пользователя', 'callback_data': 'full_documentation'},
        ],
        [
            {'text': 'Ознакомительный ролик', 'callback_data': 'intro_video'}
        ]
    ]
})

ERROR_CANNOT_UNDERSTAND_VOICE = 'Не удалось распознать текст сообщения😥 Попробуйте еще раз!'
ERROR_NULL_DATA_FOR_SUCH_REQUEST_LONG = 'К сожалению, этих данных у меня нет🤕 Не отчаивайтесь! Есть много ' \
                                        'других цифр😉 Нажмите /search'
ERROR_NULL_DATA_FOR_SUCH_REQUEST_SHORT = 'К сожалению, этих данных в системе нет🤕'
ERROR_SERVER_DOES_NOT_RESPONSE = 'К сожалению, сейчас сервер не доступен😩 Попробуйте снова чуть позже!'
MSG_WE_WILL_FORM_DATA_AND_SEND_YOU = "Спасибо! Сейчас я сформирую ответ и отправлю его вам🙌"
MSG_NO_BUTTON_SUPPORT = 'Кнопочный режим более <b>не поддерживается</b>, так как не позволяет составлять ' \
                        'запрос достаточно быстро'

# Constants for m2
ERROR_PARSING = 'Что-то пошло не так🙃 Проверьте ваш запрос на корректность'
ERROR_INCORRECT_YEAR = 'Введите год из промежутка c 2007 по %s🙈'
MSG_IN_DEVELOPMENT = 'Данный запрос еще в стадии разработки'
ERROR_NO_DATA_GOT = 'Что-то пошло не так🙃 Данные получить не удалось:('

USELESS_PILE_OF_CRAP = (
    'в', 'без', 'до', 'из', 'к', 'на', 'по', 'о', 'от', 'перед', 'при', 'через', 'с', 'у', 'за', 'над', 'об', 'под',
    'про', 'для', 'не',
    'республика', 'республики',
    'республики', 'республик',
    'республике', 'республикам',
    'республику', 'республики',
    'республикой',
    'республикою', 'республиками',
    'республике', 'республиках',
    'область', 'области', 'областью', 'областей', 'областям', 'областями', 'областях',
    'автономный', 'автономного', 'автономному', 'автономного', 'автономным', 'автономном', 'автномном', 'автономная',
    'автономной', 'автономную', 'автономною', 'автономна', 'автономные', 'автономных', 'автономными',
    'федеральный', 'федерального', 'федеральному', 'федеральным', 'федеральном', 'федерален', 'федеральных',
    'федеральным', 'федеральными',
    'край', 'края', 'краю', 'краем', 'крае', 'краев', 'краям', 'краями', 'краях', 'год', 'году')

HELLO = ('хай',
         'привет',
         'здравствуйте',
         'приветствую',
         'прифки',
         'дратути',
         'hello')

HELLO_ANSWER = ('Привет! Начни работу со мной командой /search или сделай голосовой запрос',
                'Здравствуйте! Самое время ввести команду /search',
                'Приветствую!',
                'Здравствуйте! Пришли за финансовыми данными? Задайте мне вопрос!',
                'Доброго времени суток! С вами Datatron😊, и мы начинаем /search')

HOW_ARE_YOU = ('дела', 'поживаешь', 'жизнь')

HOW_ARE_YOU_ANSWER = ('У меня все отлично, спасибо :-)',
                      'Все хорошо! Дела идут в гору',
                      'Замечательно!',
                      'Бывало и лучше! Без твоих запросов только и делаю, что прокрастинирую🙈',
                      'Чудесно! Данные расходятся, как горячие пирожки! 😄')