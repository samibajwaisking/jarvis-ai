FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    JARVIS_HOME=/data \
    JARVIS_HOST=0.0.0.0

WORKDIR /app
COPY pyproject.toml README.md ./
COPY jarvis ./jarvis
RUN pip install ".[web]"

VOLUME /data
EXPOSE 8000
CMD ["jarvis", "serve"]
