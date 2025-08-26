# Dockerfile
FROM python:3.12-slim 
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY positions.py .

# Set default environment variables
ENV TWS_HOST=host.docker.internal
ENV TWS_PORT=4002
ENV CLIENT_ID=1
ENV TIMEOUT=10

# Run the application
CMD ["python", "positions.py"]

# ===================================
# requirements.txt
# ===================================
# beautifulsoup4==4.13.4
# certifi==2025.8.3
# cffi==1.17.1
# charset-normalizer==3.4.3
# curl_cffi==0.13.0
# eventkit==1.0.3
# frozendict==2.4.6
# ib-insync==0.9.86
# idna==3.10
# multitasking==0.0.12
# nest-asyncio==1.6.0
# numpy==2.3.2
# pandas==2.3.1
# peewee==3.18.2
# platformdirs==4.3.8
# protobuf==6.32.0
# pycparser==2.22
# python-dateutil==2.9.0.post0
# pytz==2025.2
# requests==2.32.4
# six==1.17.0
# soupsieve==2.7
# typing_extensions==4.14.1
# tzdata==2025.2
# urllib3==2.5.0
# websockets==15.0.1
# yfinance==0.2.65

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