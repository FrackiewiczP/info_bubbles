FROM python:3.10

COPY ./requirements.txt /
RUN pip install -r requirements.txt

COPY ./Simulation ./Simulation
COPY ./main.py /

CMD [ "python", "./main.py" ]
