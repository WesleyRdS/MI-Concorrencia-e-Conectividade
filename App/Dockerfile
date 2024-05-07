
FROM python:3.12-slim


WORKDIR /Client


COPY . .


RUN pip install requests

EXPOSE 9985

CMD ["python", "Client/app_cliente.py"]