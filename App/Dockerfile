
FROM python:3


WORKDIR /Client


COPY . .


RUN pip install requests

EXPOSE 5000

CMD ["python", "Client/app_cliente.py"]