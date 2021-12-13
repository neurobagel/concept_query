
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

# Run tests
RUN pytest

# Start Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]