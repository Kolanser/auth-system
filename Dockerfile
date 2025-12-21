FROM python:3.14-slim

ENV PATH="${PATH}:/root/.local/bin" \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_NO_CACHE_DIR=off \
  PORT=8000 \
  PYTHONDONTWRITEBYTECODE=1 \
  # https://pythonspeed.com/articles/python-c-extension-crashes/
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  # poetry
  POETRY_VERSION=2.2.1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR="/var/cache/pypoetry"

RUN apt-get update && apt-get install -y --no-install-recommends \
  curl \
  xz-utils \
  build-essential \
  git \
  && echo "\nInstalling poetry package manager:" \
  && echo "https://github.com/python-poetry/poetry" \
  && curl -sSL --compressed "https://install.python-poetry.org" | python3 \
  && poetry --version \
  && echo "\nCleaning cache:" \
  && apt purge --autoremove -y curl xz-utils build-essential git \
  && apt clean -y \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /root/.cache;

WORKDIR /project
COPY pyproject.toml poetry.lock ./

EXPOSE ${PORT}

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  git \
  && poetry install --no-root \
  && echo "\nCleaning cache:" \
  && apt purge --autoremove -y build-essential git \
  && apt clean -y \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /root/.cache \
  && rm -rf ${POETRY_CACHE_DIR};
COPY . .

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:${PORT}"]
