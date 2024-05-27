# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables to avoid buffering and set the working directory
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /opt

# Copy the requirements file into the container at /opt
COPY requirements.txt /opt/

# Install any dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /opt
COPY ../Django /opt/

# Make port 8000 and 5000 available to the world outside this container
EXPOSE 8000
EXPOSE 5000

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=ecommerce.settings
ENV PYTHONPATH=/opt

# Run the command to start the Django server
CMD ["python", "manage.py", "runserver", "127.0.0.1:5000"]
