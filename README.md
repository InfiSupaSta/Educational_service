    Educational_service test for MetaLamp Company.


Обучающий сервис на Django, REST API на Django Rest Framework и документация в Swagger с использование библиотеки
drf-yasg.

> Основные эндпоинты:

- /swagger - описание всех эндпоинтов с доступными методами

- /api/v1 - отправная точка для API

- /api/v1/themes - список всех тем и создание темы, GET/POST

- /api/v1/themes/id - тема по id, GET/PUT/PATCH

- /api/v1/questions - список всех вопросов и создание вопроса, GET/POST

- /api/v1/questions/id - вопрос по id, GET/PUT/PATCH/DELETE

- /api/v1/answers - список ответов и создание ответа, GET/POST

- /api/v1/answers/id - ответ по id, GET/PUT/PATCH

- /api/v1/right-answers - список правильных ответов и создание ответа, GET/POST

- /api/v1/right-answers/id - правильный ответ по id, GET/PUT/PATCH

- /api/v1/results - список с результатом прохождений тестов

- /api/v1/user - список всех пользователей, доступно только для админов

Версия проекта для ознакомления на Heroku:

> https://educational-service--metalamp.herokuapp.com/