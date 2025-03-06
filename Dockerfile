# Use Python as base image
FROM python:3.9

# Define working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for FastAPI
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "8000"]
