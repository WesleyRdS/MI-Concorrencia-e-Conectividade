
FROM python:3


WORKDIR /Broker


COPY . .


RUN pip install flask


EXPOSE 5000
EXPOSE 54310
EXPOSE 54020

CMD ["python", "Broker/broker.py"]