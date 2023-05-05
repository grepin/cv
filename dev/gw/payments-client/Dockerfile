FROM python:3.10.4
RUN mkdir /home/logs
WORKDIR /app
COPY ./requirements.txt /
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt
COPY ./filebeat-6.2.4-amd64.deb .
RUN dpkg -i filebeat-6.2.4-amd64.deb
COPY ./filebeat.yml /etc/filebeat/
COPY . .
ENTRYPOINT ["bash", "entrypoint.sh"]
#ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]