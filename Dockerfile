FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
ENV PG_URL='postgresql://postgres:edge9527@host.docker.internal:5432/dev_tenant'
ENV PORT=5000
EXPOSE 5000
CMD ["python","./app.py"]
