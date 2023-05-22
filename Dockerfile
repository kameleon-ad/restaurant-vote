# Base image
FROM python:3.10.4-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy source code to working directory
COPY . /app

# update apt packages, install python and pip Install packages from requirements.txt and run migrations
RUN apt-get update && \
    apt-get install -y postgresql libpq-dev gcc
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
RUN python3 manage.py makemigrations

ENV LANG en_US.utf8

# Expose the port that the Flask application will run on
ENV LISTEN_PORT=5000
EXPOSE 5000

# Set environment variables for Django

# Run server at container launch
CMD [ "python3", "manage.py", "runserver", "80" ]
