# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Upgrade to latest pip
RUN pip install --upgrade pip

# Copy requirements first for better Docker layer caching
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy TACO source code
COPY . /taco

# Set working directory to where TACO code is
WORKDIR /taco

CMD ["bash"]
