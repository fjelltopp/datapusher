FROM python:3.8
ARG DEVELOPMENT
COPY . /var/www/datapusher

WORKDIR /var/www/datapusher
RUN pip install --upgrade pip
RUN if [ "$DEVELOPMENT" = "true" ] ; then pip install -r requirements-dev.txt; else pip install -r requirments.txt; fi

ENV LC_ALL=C
ENTRYPOINT ["./datapusher-entrypoint.sh"]
CMD [ "python3", "datapusher/main.py", "deployment/datapusher_settings.py"]
