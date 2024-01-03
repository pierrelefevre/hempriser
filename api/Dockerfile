FROM python

WORKDIR /app
COPY ./api/requirements.txt /app/
RUN pip install -r requirements.txt
COPY ./api /app

EXPOSE 8080

CMD ["python", "server.py"]