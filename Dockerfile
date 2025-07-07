# Use official Python image
FROM python:3.11-slim

# Set environment
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

VOLUME [ "/data" ]
