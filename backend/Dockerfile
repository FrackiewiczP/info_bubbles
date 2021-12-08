FROM python:3.10

COPY ./requirements.txt /
RUN pip install -r requirements.txt

COPY src /src
WORKDIR /src
CMD [ "python", "./main.py" ]
