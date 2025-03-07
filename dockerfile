# Use an official lightweight Python image
FROM python:3.11-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*  # Cleanup to reduce image size

# Set the working directory
WORKDIR /app

# Copy the entire project to the container
COPY . .

# Install dependencies
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "8000"]
