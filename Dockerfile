FROM python:3.10.0-slim-buster

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/calendar-analyzer"

RUN apt-get update \
    && apt-get install --no-install-recommends -y htop g++ libpcre3 libpcre3-dev make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/calendar-analyzer

ADD requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader stopwords

COPY ./ /usr/src/calendar-analyzer
