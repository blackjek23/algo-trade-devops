# Dockerfile
FROM python:3.12-slim 
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set default environment variables
ENV TWS_HOST=host.docker.internal
ENV TWS_PORT=4002
ENV CLIENT_ID=1
ENV TIMEOUT=10

# Run the application
CMD ["python", "main.py"]

# ===================================
# docker-compose.yml
# ===================================
# version: '3.12-slim'
# 
# services:
#   tws-positions:
#     build: .
#     environment:
#       - TWS_HOST=host.docker.internal  # For Windows/Mac Docker Desktop
#       - TWS_PORT=4002                  # 4001 for live, 4002 for paper
#       - CLIENT_ID=1
#       - TIMEOUT=10
#     extra_hosts:
#       - "host.docker.internal:host-gateway"  # Linux Docker support

# ===================================
# .env (optional - for docker-compose)
# ===================================
# TWS_HOST=host.docker.internal
# TWS_PORT=4002
# CLIENT_ID=1
# TIMEOUT=10

# ===================================
# Build and Run Commands
# ===================================

# Build the image:
# docker build -t tws-positions .

# Run with default settings:
# docker run --rm tws-positions

# Run with custom settings:
# docker run --rm -e TWS_HOST=192.168.1.100 -e TWS_PORT=4002 tws-positions

# Run with docker-compose:
# docker-compose up

# For Linux Docker (if host.docker.internal doesn't work):
# docker run --rm --network host -e TWS_HOST=127.0.0.1 -e TWS_PORT=4002 tws-positions