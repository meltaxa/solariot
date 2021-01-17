FROM python:3.9

WORKDIR /solariot
COPY . /solariot/

RUN pip3 install --upgrade pip wheel && pip3 install --upgrade -r requirements.txt

CMD ["solariot.py"]
