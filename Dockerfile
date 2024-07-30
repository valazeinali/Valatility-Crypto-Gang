# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install cloudflared
RUN apt-get update && apt-get install -y wget && \
    wget -O cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && \
    dpkg -i cloudflared.deb && \
    cloudflared service install cloudfareauthtokenfake && \
    rm cloudflared.deb

# Copy the rest of the application code
COPY . .

# Install pre-commit and set up hooks
RUN pip install pre-commit
RUN pre-commit install --install-hooks
RUN bash install_hooks.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8000", "dashboard:server"]
