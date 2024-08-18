FROM python:3.11

COPY . /app/
WORKDIR /app/

RUN pip3 install -U pip
RUN pip3 install -U -r requirements.txt

CMD ["python3", "-m", "manager"]
