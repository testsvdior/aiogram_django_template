FROM python:3.8.5

WORKDIR /bot

# Copy only requirements to cache them in docker layer
COPY ./requirements.txt /bot/
RUN pip install -r requirements.txt

# Creating folders, and files for a project:
COPY . /bot

CMD ["python", "main.py"]
