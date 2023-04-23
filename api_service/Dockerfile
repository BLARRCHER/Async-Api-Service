FROM python:3.10

WORKDIR /opt/api_service

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
COPY wait_for_it.sh wait_for_it.sh

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt \
     && sed $'s/\r$//' ./wait_for_it.sh > ./wait_for_it.unix.sh \
     && chmod +x wait_for_it.unix.sh

COPY . .

ENTRYPOINT ["bash", "wait_for_it.unix.sh", "service_db:5432", "--", "python3", "src/main.py"]
