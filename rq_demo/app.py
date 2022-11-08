# 0. Установить Python3, Redis, Poetry (или аналог)
# запуск виртуального окружения, подтянуть Flask, rq, rq-dashboard, requests

import time
from datetime import timedelta

import requests
import rq_dashboard
from flask import Flask, render_template
from redis import Redis
from rq import Queue, Retry, registry

# 1. Создаем приложение (экземпляр Flask)
app = Flask(__name__)

# 2. Подключаем мониторинг задач и очередей
# web или в терминале rq info --interval 1
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

# 3. Запустить Redis и проверить через терминал:
# redis-server
# redis-cli ping

# 4. Создаем связь с Redis (вроде канала)
redis_q = Redis()

# 5. Описываем очереди с разным приоритетом выполнения

# Сообщения с job из очередей публикуются в Redis, в нашем канале redis_q
# Приоритет зависит от порядка описания очереди, а не от ее имени
queue_high = Queue('high', connection=redis_q)
queue_default = Queue('default', connection=redis_q)
queue_low = Queue('low', connection=redis_q)
queues = (queue_high, queue_default, queue_low)

# 6. Запустить worker и подписать его на канал в Redis

# терминал из папки с проектом, предполагаю так воркер находит канал redis_q
# for (MacOS users + requests lib + rq) put in a terminal:
#   export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
# rq worker high default low --with-scheduler (для Retry и плановых задач)

# Можно запустить программно, но как-то отдельно
# worker = Worker(queues=queues, connection=redis_q)
# worker.work(with_scheduler=True)


# 7. Имитация обращений к приложению, ендпоинты привязываем к очередям

@app.route('/')
def index():
    return render_template('index.html')


# 7.1 Постановка задачи в очередь с Low приоритетом
@app.route('/start-low-tasks/')
def start_low_tasks() -> str:
    hits = 10
    hit_delay = 0
    for _ in range(hits):
        queue_low.enqueue(
            f=any_task, kwargs={'secunds': 1, 'word': 'education'}
        )
        time.sleep(hit_delay)
    return render_template('index.html')


# 7.2 Постановка задачи в очередь с Default приоритетом
@app.route('/start-default-tasks/')
def start_default_tasks() -> str:
    hits = 10
    hit_delay = 0
    for _ in range(hits):
        queue_default.enqueue(f=any_task, args=(2, 'improvisation'))
        time.sleep(hit_delay)
    return render_template('index.html')


# 7.3 Постановка задачи в очередь с High приоритетом
@app.route('/start-high-tasks/')
def start_high_tasks() -> str:
    hits = 10
    hit_delay = 0
    for _ in range(hits):
        queue_high.enqueue(any_task, 2, 'procrastination', job_timeout=4)
        time.sleep(hit_delay)
    return render_template('index.html')


def any_task(secunds: int, word: str) -> int:
    time.sleep(secunds)
    return len(word)


# 8. Передача задачи в очередь с перепостановкой в случае неудачи

@app.route('/retry-failed-tasks/')
def retry_failed_tasks() -> str:
    hits = 5
    hit_delay = 0
    for _ in range(hits):
        queue_default.enqueue(
            failed_task, 67, retry=Retry(max=3, interval=[3, 5, 7])
        )
        time.sleep(hit_delay)
    return render_template('index.html')


def failed_task(num: int) -> ZeroDivisionError:
    time.sleep(2)
    return num / 0


# 9. Очистка очередей и списка Failed

@app.route('/empty-queues/')
def empty_queues() -> str:
    for queue in queues:
        queue.empty()
    return render_template('index.html')


@app.route('/empty-failed/')
def empty_failed() -> str:
    for queue in queues:
        failed_registry = registry.FailedJobRegistry(queue=queue)
        for job_id in failed_registry.get_job_ids():
            failed_registry.remove(job_id, delete_job=True)
    return render_template('index.html')


# 10. Демонстрация плановых задач, например, сходить за погодой

@app.route('/start-scheduled-task/')
def start_scheduled_task() -> str:
    queue_low.enqueue_in(timedelta(seconds=20), get_weather, 'Hague')
    return render_template('index.html')


def get_weather(city: str) -> str:
    url = f'http://wttr.in/{city}'
    wttr_params = {'format': 3}
    try:
        response = requests.get(url, params=wttr_params)
        print(response.text.strip())
    except Exception:
        print('Something went wrong')


@app.route('/get-scheduled-list/')
def get_scheduled_list() -> str:
    schedule_list = '<p>Scheduled job list:</p>'
    for queue in queues:
        scheduled_registry = registry.ScheduledJobRegistry(queue=queue)
        for job_id in scheduled_registry.get_job_ids():
            scheduled_time = scheduled_registry.get_scheduled_time(job_id)
            job = queue.fetch_job(job_id)
            schedule_list += (f'<p>{job.origin} queue - {job.get_status()} on'
                              f' {scheduled_time} - {job.description}</p>')
    return schedule_list


@app.route('/empty-scheduled-list/')
def empty_scheduled_list() -> str:
    for queue in queues:
        scheduled_registry = registry.ScheduledJobRegistry(queue=queue)
        for job_id in scheduled_registry.get_job_ids():
            scheduled_registry.remove(job_id, delete_job=True)
    return render_template('index.html')
