FROM python:3
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
WORKDIR /var/www/datapusher
ENV LC_ALL=C
ENTRYPOINT ["./datapusher-entrypoint.sh"]
CMD [ "python3", "datapusher/main.py", "deployment/datapusher_settings.py"]
