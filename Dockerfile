FROM python:3.11-slim

WORKDIR /app

# install poetry
RUN pip install poetry

# copy dependency files
COPY pyproject.toml poetry.lock ./

# install deps
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

# copy code
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]