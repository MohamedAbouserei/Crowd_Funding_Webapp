FROM python:3.7-slim

USER root
RUN python -m pip install --upgrade pip

WORKDIR djangoApp

COPY . .

RUN pip install -r requirements.txt

RUN python manage.py makemigrations

RUN python manage.py migrate

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]