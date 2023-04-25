ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}

WORKDIR /src
COPY src/setup.py README.md LICENSE ./
COPY src/excel_db/__init__.py ./excel_db/__init__.py
WORKDIR /src
RUN pip install -e .[dev]

COPY src .
