# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies first to leverage Docker's caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the FastAPI/Flask port (if applicable)
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]
