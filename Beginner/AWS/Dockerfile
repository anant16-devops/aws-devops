# Use official Python base image
FROM python:3.11.13-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Download spaCy English model
RUN python -m spacy download en_core_web_sm

# Copy your script into the container
COPY parser.py .

# (Optional) Set the default command to run your script
# You can override this with docker run arguments if needed
CMD ["python", "parser.py"]
