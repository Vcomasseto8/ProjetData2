# Use an official lightweight Python image
FROM python:3.11-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*  # Cleanup to reduce image size

# Set the working directory
WORKDIR /app

# Copy the application files
COPY predict.py /app/


# Install dependencies first to leverage Docker's caching
COPY requirements.txt .
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Expose the FastAPI/Flask port (if applicable)
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "8000"]
