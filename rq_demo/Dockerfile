FROM python:3.10.8-slim

RUN pip install poetry==1.2.1

# виртуальное окружение проекта будет отдельно файлов проекта
# иначе сложности с volumes для папки с файлами проекта
RUN poetry config virtualenvs.in-project false
RUN poetry new rq-demo

WORKDIR /rq-demo
COPY rq_demo/ rq_demo/

COPY pyproject.toml .
RUN poetry install --without dev

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP=rq_demo.app
CMD [ "poetry", "run", "flask", "run" ]
