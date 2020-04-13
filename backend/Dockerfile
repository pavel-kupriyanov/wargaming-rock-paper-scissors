FROM python:3.7.2

WORKDIR /opt/app

COPY ./ .
RUN pip install -r requirements.txt

ENTRYPOINT python3 run.py
