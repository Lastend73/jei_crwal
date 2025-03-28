# Use the official Python image from the Docker Hub
FROM python:3.13.2-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirement.txt .

# Install the dependencies
RUN pip install -r requirement.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "apps.py"]
