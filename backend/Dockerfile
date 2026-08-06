# Step 1: Use an official lightweight Python image
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Step 4: Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Step 5: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the rest of the application code
COPY . .

# Step 7: Expose the port Flask runs on
EXPOSE 5000

# Step 8: Define the command to run the app
# Using 0.0.0.0 allows it to respond to external requests
CMD ["python", "app.py"]
