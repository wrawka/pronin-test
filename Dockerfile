FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1

RUN apk update && apk upgrade && apk add make

COPY . /app
WORKDIR /app

RUN uv sync --locked
ENV PATH="/app/.venv/bin:$PATH"

CMD ["sleep", "infinity"]
