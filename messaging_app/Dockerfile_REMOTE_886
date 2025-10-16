# Use official Python base image
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Copy requirements file into the image
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port Django runs on
EXPOSE 8000

# Default command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
