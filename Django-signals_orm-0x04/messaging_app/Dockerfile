# Step 1: Use the official Python 3.10 image from Docker Hub
FROM python:3.10

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements.txt into the container at /app
COPY requirements.txt .

# Step 4: Install dependencies from the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your application code into the container
COPY . .

# Step 6: Expose port 8000 (default port for Django)
EXPOSE 8000

# Step 7: Set the command to run your Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Step 8: Run the app
RUN docker run -p 8000:8000 messaging_app
