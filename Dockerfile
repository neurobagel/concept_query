# FROM python:3.9-slim-buster
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# WORKDIR /concept_query
# COPY . /concept_query
# RUN pip install pipenv
# RUN pipenv install --system --deploy --ignore-pipfile
# RUN pipenv install --system --deploy --ignore-pipfile -d
# RUN python manage.py makemigrations
# RUN python manage.py migrate
# RUN python manage.py collectstatic 

# FROM python:3.9-slim-buster

# ARG YOUR_ENV

# ENV YOUR_ENV=${YOUR_ENV}
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONFAULTHANDLER=1
# ENV PYTHONUNBUFFERED=1
# ENV PYTHONHASHSEED=random
# ENV PIP_NO_CACHE_DIR=off
# ENV PIP_DISABLE_PIP_VERSION_CHECK=on
# ENV PIP_DEFAULT_TIMEOUT=100
# ENV POETRY_VERSION=1.1.12

# # System deps:
# RUN pip install "poetry==$POETRY_VERSION"

# # Copy only requirements to cache them in docker layer
# WORKDIR /concept_query
# COPY poetry.lock pyproject.toml /concept_query/

# # Project initialization:
# RUN poetry config virtualenvs.create false \
#   && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# # Creating folders, and files for a project:
# COPY . /concept_query

# # Django migrations
# RUN python manage.py makemigrations
# RUN python manage.py migrate

# # Django static files
# RUN python manage.py collectstatic 

# FROM python:3.9-slim-buster
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /concept_query

# Creating folders, and files for a project:
COPY . /concept_query

# System deps:
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Django migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Django static files
# This should be done by developers during commit and not during container setup
# RUN python manage.py collectstatic

# Start Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]