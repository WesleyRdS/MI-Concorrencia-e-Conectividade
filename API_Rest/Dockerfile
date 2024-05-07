
FROM python:3.12-slim


WORKDIR /Broker


COPY . .


RUN pip install flask


EXPOSE 9985
EXPOSE 54310
EXPOSE 54020

CMD ["python", "Broker/broker.py"]