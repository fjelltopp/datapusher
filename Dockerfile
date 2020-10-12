FROM python:3.8

COPY . /var/www/datapusher

WORKDIR /var/www/datapusher
RUN pip install --upgrade pip &&\
    pip install -r requirements.txt
ENV LC_ALL=C
ENTRYPOINT ["./datapusher-entrypoint.sh"]
CMD [ "python3", "datapusher/main.py", "deployment/datapusher_settings.py"]
