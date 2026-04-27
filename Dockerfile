FROM python:3.10
RUN pip3 install uwsgi pipenv
RUN apt update && apt install rsync curl -y && \
    rm -rf /var/lib/apt/lists/*

ENV DATAPUSHER_DIR /var/www/datapusher

ARG DEVELOPMENT
COPY . $DATAPUSHER_DIR

WORKDIR $DATAPUSHER_DIR
RUN pip install --upgrade pip
RUN if [ "$DEVELOPMENT" = "true" ] ; then pip install -r requirements-dev.txt; else pip install -r requirements.txt; fi
RUN pip install uwsgi

RUN chown -R www-data:www-data $DATAPUSHER_DIR

ENV LC_ALL=C
ENTRYPOINT ["./datapusher-entrypoint.sh"]
CMD /usr/local/bin/uwsgi --ini-paste $DATAPUSHER_DIR/deployment/datapusher-uwsgi.ini
