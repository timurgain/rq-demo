FROM python:3.10.8-slim

RUN pip install poetry==1.2.1
RUN poetry config virtualenvs.in-project true
RUN poetry new rq-demo

WORKDIR /rq-demo
COPY rq_demo/ rq_demo/

COPY pyproject.toml .
RUN poetry install

ENV FLASK_APP=rq_demo.app
CMD [ "poetry", "run", "flask", "run", "--host=0.0.0.0" ]
