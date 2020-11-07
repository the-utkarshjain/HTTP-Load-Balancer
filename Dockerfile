# Dockerfile

FROM python:3.6

RUN pip install flask
COPY ./app.py /app/app.py
ENV FLASK_APP=/app/app.py

CMD ["python", "/app/app.py"]