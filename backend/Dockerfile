FROM python:3.10 as base

COPY ./requirements.txt /
RUN pip install -r requirements.txt
RUN pip install ptvsd

COPY src /src
WORKDIR /src

######################################

FROM base as debug
CMD [ "python", "-m", "ptvsd", "--host", "0.0.0.0", "--port", "8888", "--wait", "--multiprocess", "./main.py" ]

######################################

FROM base as dev
CMD [ "python", "./main.py" ]
