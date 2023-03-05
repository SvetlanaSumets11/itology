FROM python:3.9

WORKDIR /usr/src/app/

COPY pyproject.toml /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . /usr/src/app/
