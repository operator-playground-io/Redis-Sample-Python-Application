FROM python:3.8-slim

RUN pip install flask==1.1.2
RUN pip install redis==3.5.3

EXPOSE 6000

WORKDIR project

COPY . .

CMD python app.py $HOST $PORT $PASSWORD
