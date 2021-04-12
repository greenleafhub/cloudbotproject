FROM python

WORKDIR /app
COPY config.ini /app
COPY waterbot.py /app
COPY requirements.txt /app

RUN pip install pip update
RUN pip install -r requirements.txt

CMD python waterbot.py
