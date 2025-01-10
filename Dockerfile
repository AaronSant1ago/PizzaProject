# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port 8080 to the outside world (as specified by Fly's config)
EXPOSE 8080

# Run the application when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
