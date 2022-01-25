FROM python:3.9-alpine

WORKDIR /solariot

RUN addgroup -g 2000 solariot && adduser -D -u 2000 -G solariot solariot
COPY . /solariot/
RUN apk add --no-cache gcc musl-dev && pip3 install --no-cache-dir --upgrade -r requirements.txt && apk del --no-cache gcc musl-dev

USER solariot
ENV PYTHONPATH="/config:$PYTHONPATH"
CMD ["python3", "solariot.py", "-v"]
