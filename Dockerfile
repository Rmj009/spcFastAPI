FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /Servingstats/app

COPY requirements.txt ./
RUN pip install -r requirements.txt


COPY . /Servingstats/app/
COPY . /main.py


COPY . .
ENV PG_URL='postgresql://postgres:edge9527@host.docker.internal:5432/dev_tenant'
ENV PORT=8000
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# ENTRYPOINT ["./gunicorn_starter.sh"]