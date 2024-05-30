# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8080

# Command to run the app
CMD ["gunicorn", "Online_Shop_fin.wsgi:application", "--bind", "0.0.0.0:8080"]
