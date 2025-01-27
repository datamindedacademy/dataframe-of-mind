FROM mcr.microsoft.com/vscode/devcontainers/python:3.11-bookworm


# Install graphviz
RUN apt-get update && \
    apt-get -y install --no-install-recommends default-jdk graphviz && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Spark config
COPY spark-defaults.conf /app/spark-defaults.conf
ENV SPARK_CONF_DIR=/app

# Fetch uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
