FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY .env .

# We can install dependencies from pyproject.toml usually via pip install .
RUN pip install --no-cache-dir .

COPY . /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
