                                                   ИНСТРУКЦИЯ !!!

1. ```Сделать git clone https://github.com/isko18/Aiogram-H-W-```

2. ```Работать строго на этом файле где сделали клон репозитория!!!```

3. ```После завершения домашнего задания написать мне для получения доступа к репохиторию (мой тг https://t.me/itb_18)```

4. ```Откройте новую ветку с вашим именем и загрузите в GitHub```


                                                 Задание: Создание Telegram бота для записи новых студентов на DemoDay

Разработать Telegram бота, который будет записывать новых студентов на мероприятие DemoDay. Данные студентов должны сохраняться в базу данных.

- Используйте SQLite

Таблица должна содержать следующие поля:

- id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- first_name (TEXT)
- last_name (TEXT)
- username (TEXT)
- direction (TEXT)
- number (TEXT)


Telegram бот:

1. Используйте библиотеку aiogram для создания бота.
2. Бот должен принимать команды и ответы от пользователя, чтобы собрать необходимые данные.
 

Логика работы бота:

При запуске команды ```/start``` бот приветствует пользователя и объясняет, что он может записаться на DemoDay.
Бот последовательно запрашивает у пользователя:

Имя (first_name)
Фамилию (last_name)
Никнейм (username)
Направление (direction)
Номер телефона (number)

После ввода всех данных бот сохраняет их в базу данных и подтверждает регистрацию.

 
                                                  ДОПЗАДАНИЕ:
 1. Поставить логотип к телеграм боту и отправить ссылку на бот вместе со ссылкой на GitHub
 2. Загрузить код в GitHub с .gitginore и config.py файлам

Дедлайн: 09.07.2024г 
время: 00:00
