FROM ubuntu:24.04
LABEL maintainer="Karlos Helton Braga <Konkah>"

RUN apt update
RUN apt upgrade -y
RUN apt autoremove -y
RUN apt autoclean -y

RUN apt install -y curl
RUN apt install -y nano
RUN apt install -y unzip
RUN apt install -y net-tools

RUN apt install -y python3.12 
RUN apt install python3-pip -y
RUN apt install python3-dev -y 

COPY study_shoes_store /var/www/study_shoes_store
RUN rm /var/www/study_shoes_store/db.sqlite3

RUN python3 -m pip install -U pip
RUN python3 -m pip install -U setuptools
RUN python3 -m pip install -U wheel

WORKDIR /var/www/study_shoes_store
RUN python3 -m pip install -r requirements.txt

RUN python3 manage.py migrate

ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@admin.com
ENV DJANGO_SUPERUSER_PASSWORD=admin
RUN python3 manage.py createsuperuser --no-input

EXPOSE 8000

#CMD bash
CMD python3 manage.py runserver