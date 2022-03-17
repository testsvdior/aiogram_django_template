FROM python:3.8.5

WORKDIR /django

# Copy only requirements to cache them in docker layer
COPY ./requirements.txt /django/
RUN pip install -r requirements.txt

# Creating folders, and files for a project:
COPY . /django
