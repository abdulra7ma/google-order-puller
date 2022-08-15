FROM python:3.10 as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc cron

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends cron

# CREATE and switch to a new user
RUN groupadd -r -g 2001 cusers \
    && useradd -r -m -u 1001 -g cusers user
WORKDIR /home/user

# Install application into container
RUN mkdir code/
WORKDIR /home/user/code/
RUN mkdir logs
COPY . .

# RUN chmod 644 /etc/crontab 
RUN chmod +x ./docker-entrypoint.sh

RUN ./docker-entrypoint.sh
