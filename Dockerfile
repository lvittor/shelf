# Creating a python base with shared environment variables
FROM python:3.8.1-slim as python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# builder-base is used to build dependencies
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION=1.1.8
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev 

# 'development' stage installs all dev deps and can be used to develop code.
# For example using docker-compose to mount local volume under /shelf
FROM python-base as development

# Copying poetry and venv into image
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# venv already has runtime deps installed we get a quicker install
WORKDIR $PYSETUP_PATH
RUN poetry install && apt-get update && apt-get install --no-install-recommends -y git nano

WORKDIR /shelf
COPY . .

RUN cd shelf && pip install --editable . 

RUN git config --global user.email "test@test.com" && git config --global user.name "test"
#RUN cp shelf/hook_samples/commit-msg tests/shelf/.git/hooks/ && chmod +x tests/shelf/.git/hooks/commit-msg

# 'lint' stage runs black and isort
# running in check mode means build will fail if any linting errors occur
FROM development AS lint
RUN black --config ./pyproject.toml --check shelf tests
RUN isort --settings-path ./pyproject.toml --check-only shelf tests
CMD ["tail", "-f", "/dev/null"]

# 'test' stage runs our unit tests with pytest and coverage.
FROM development AS test
RUN coverage run --rcfile ./pyproject.toml -m pytest ./tests

# 'production' stage uses the clean 'python-base' stage and copyies
# in only our runtime deps that were installed in the 'builder-base'
FROM python-base as production
COPY --from=builder-base $VENV_PATH $VENV_PATH

COPY . /shelf
WORKDIR /shelf/tests/shelf
