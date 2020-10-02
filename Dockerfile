FROM python:3.8
COPY requirements-dev.txt /tmp/requirements-dev.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip &&\
    pip3 install -r /tmp/requirements-dev.txt
WORKDIR /var/www/datapusher
ENV LC_ALL=C
ENTRYPOINT ["./datapusher-entrypoint.sh"]
CMD [ "python3", "datapusher/main.py", "deployment/datapusher_settings.py"]
