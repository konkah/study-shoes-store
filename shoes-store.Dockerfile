FROM python:3.13-slim
LABEL maintainer="Karlos Helton Braga <Konkah>"

ENV PIP_TRUSTED_HOST="pypi.org files.pythonhosted.org pypi.python.org"

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ca-certificates curl git gnupg nano unzip net-tools \
    && apt-get autoremove -y \
    && apt-get autoclean -y \
    && rm -rf /var/lib/apt/lists/*

COPY study_shoes_store /var/www/study_shoes_store

WORKDIR /var/www/study_shoes_store
RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

CMD ["/entrypoint.sh"]
