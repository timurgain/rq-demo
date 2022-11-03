# 0. Установить Python3, Redis, Poetry (или аналога)
# запуск виртуального окружения, установка Flask, rq, rq-dashboard

import time

from flask import Flask
from flask import render_template

from redis import Redis

from rq import Queue
import rq_dashboard


# 1. Создаем приложение или экземпляр Flask
app = Flask(__name__)

# 2. Redis запустить и проверить через терминал:
# redis-server
# redis-cli ping

# 3. Соединение с Redis
redis_db_queues = Redis()

# 4. Описываем очереди с разным приоритетом выполнения
# Приоритет зависит от порядка описания очереди, а не от ее имени
queue_high = Queue('high', connection=redis_db_queues)
queue_default = Queue('default', connection=redis_db_queues)
queue_low = Queue('low', connection=redis_db_queues)

# 5. Запустить worker на прослушку описанных очередей:
#  rq worker high default low


# 6. Имитация обращений к приложению, ендпоинты привязываем к очередям

@app.route('/')
def index():
    return render_template('index.html')


# 6.0 имитация задачи
def any_task(secunds: int, word: str) -> int:
    time.sleep(secunds)
    return len(word)


# 6.1 Постановка задачи в очередь с Low приоритетом
@app.route('/start-low-tasks/')
def start_low_tasks():
    hits = 30
    hit_delay = 0

    while hits > 1:
        queue_low.enqueue(
            f=any_task, kwargs={'secunds': 1, 'word': 'education'}
        )
        time.sleep(hit_delay)
        hits -= 1
    return '<p>Low priority tasks are queued</p>'


# 6.2 Постановка задачи в очередь со Default приоритетом
@app.route('/start-default-tasks/')
def start_default_tasks():
    hits = 10
    hit_delay = 3

    while hits > 1:
        queue_default.enqueue(f=any_task, args=(2, 'improvisation'))
        time.sleep(hit_delay)
        hits -= 1
    return '<p>Default priority tasks are queued</p>'


# 6.2 Постановка задачи в очередь с High приоритетом
@app.route('/start-high-tasks/')
def start_high_tasks():
    hits = 5
    hit_delay = 10

    while hits > 1:
        queue_high.enqueue(any_task, 3, 'procrastination')
        time.sleep(hit_delay)
        hits -= 1
    return '<p>High priority tasks are queued</p>'


# 7. Повторный запуск фейловой задачи


# 8. Имитация плановых задач, например, сходить за погодой в Гааге

# 9. Подключаем мониторинг задач и очередей
# web или в терминале rq info --interval 1
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")
