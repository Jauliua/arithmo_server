# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install flask flask_cors pandas

# Run app.py when the container launches
CMD ["python", "api.py"]