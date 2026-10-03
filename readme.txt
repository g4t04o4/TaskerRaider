Небольшое FastAPI приложение для менеджмента задач с хранением данных в SQLite базе данных

Приложение хранит задачу (название задачи, дедлайн, опциональное описание и id категории задачи), а также типы/категории задач (название категории и опциональное описание).

Функционал:
    добавить задачу
        без id с использованием автоинкремента
        с id для контроля id
    получить задачу
        по id
        весь список задач
    изменить задачу
    удалить задачу
        по id
        весь список задач

    добавить категорию задач
        без id с автоинкрементов
        с id для контроля id
    получить категорию задач
        по id
        весь список
    изменить категорию задач
    удалить категорию задач
        по id
        весь список

TODO: 
    make a basic handler to duplicate less code
    gui (jinja2/html/css)
        update methods
        delete task/type
        prettify
        date input
        select tasktype from dropdown menu
    pretty gui (htmx/react/vue.js?)
    actual web security
    session storage
    universal server config
    api routers
    postgresql db
    async/await (after postgres)
    separate error handler for a whole project (?)
    session dependency database access
    docker .env for port and (?) service name/container name