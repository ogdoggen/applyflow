FROM python:3.14-slim
WORKDIR /code

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini ./alembic.ini
COPY ./tests ./tests
COPY ./pytest.ini ./pytest.ini
EXPOSE 8000

CMD ["uvicorn", "app.main:app","--host", "0.0.0.0","--port", "8000"]

