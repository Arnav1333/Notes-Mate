# Step 1: Use the official Python image from the Docker Hub as a base image
FROM python:3.12-slim

# Step 2: Set environment variables
# Disable buffering to prevent issues with output in the terminal
ENV PYTHONUNBUFFERED 1

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Install any OS-level dependencies required
# We install gcc and psycopg2 dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Step 6: Copy the entire project code into the container
COPY . /app/

# Step 7: Collect static files (optional if your app has static files)
RUN python manage.py collectstatic --noinput

# Step 8: Expose the port that your app will run on
EXPOSE 8000

# Step 9: Define the command to run the app with Gunicorn
CMD ["gunicorn", "notes_mate.wsgi:application", "--bind", "0.0.0.0:8000"]