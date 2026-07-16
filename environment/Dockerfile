FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bash \
        curl \
        tmux \
        asciinema \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/0.7.13/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

COPY attendance/ /app/attendance/
COPY data/ /app/data/
COPY run_report.py /app/run_report.py

# Pre-build test venv with pytest
RUN uv venv /app/.tbench-testing && \
    uv pip install --python /app/.tbench-testing/bin/python pytest==8.4.1