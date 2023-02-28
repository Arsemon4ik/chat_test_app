## Installation
Install the dependencies and start the server.
```sh
python -m venv venv
pip install -r requirements.txt
```

Django websocket app

```sh
cd djangochat
python manage.py runserver
```

Test in Postman
(In every request you should put Token into the header)
```sh
/start - create thread
/:thread_id - get thread information
/thread_messages - get all thread messages
/delete_thread - delete thread
/view_message - view message (is_read=True)
/users - view list of users

```
Connection using websocket (don't forget to use Token in header)

```sh
ws://localhost:8000/ws/chat/:thread_id/ - connect
body:
{"message": "Your message here..."}
```

- 2 моделі з полями ✓
- У Thread можливо лише 2 користувача(participant'а) part

- створення (якщо Thread з такими user'ами існує - повертаємо його) або видалення
Thread'а;  ✓

- одержання списку Thread'ів для будь-якого user'a (у кожному Thread'e має лежати
останнє повідомлення, якщо таке є); ✓
- створення чи отримання списку Message для Thread'a; ✓
- позначки що одне чи кілька Message прочитано(is_read=True); part
- отримання кількості непрочитаних повідомлень для користувача. ✓


1. Додати адмінку Джанго. ✓
2. Додати pagination(LimitOffsetPagination) ✓
3. Валідація в урлах - ОБОВ'ЯЗКОВО, коментарі вітаються! ✓
4. Requirements:
    - Django;
    ії BackEnd iSi Technology
    - Реалізувати – DRF; ✓
    - djangorestframework-jwt (це для того, щоб можна було взяти в адмінці токен і
    перевірити це завдання); ✓
    - база даних – SQLite; ✓