# Use an official lightweight Python image
FROM python:3.11-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*  # Cleanup to reduce image size

# Set the working directory
WORKDIR /app

# Copy the entire project (including subdirectories)
COPY . /app/

# Install dependencies first to leverage Docker's caching
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Ensure API keys are available
COPY .env /app/

# Run the full pipeline during the build (optional, but ensures forecast files exist)
RUN python main.py

# Expose the FastAPI/Flask port (if applicable)
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "8000"]
