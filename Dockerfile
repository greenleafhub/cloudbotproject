FROM python

WORKDIR /app
COPY waterbot.py /app
COPY requirements.txt /app

RUN pip install pip update
RUN pip install -r requirements.txt

RUN apt-get update \
    &&  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
    
RUN TZ=Asia/Hong_Kong \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata 

CMD python waterbot.py
