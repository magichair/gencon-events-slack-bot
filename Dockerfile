# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Configure Poetry to not use virtual environments
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install

# Expose the port the app runs on
EXPOSE 3000

VOLUME ["/app/data"]

# Command to run the application with gunicorn
CMD ["python", "app.py"]
