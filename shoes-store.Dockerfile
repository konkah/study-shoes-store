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

RUN apt install -y python3.12 python3-pip python3-dev

COPY study_shoes_store /var/www/study_shoes_store

RUN pip3 install --break-system-packages setuptools wheel

WORKDIR /var/www/study_shoes_store
RUN pip3 install --break-system-packages -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

CMD ["/entrypoint.sh"]