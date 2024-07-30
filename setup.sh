#!/bin/bash

# Update package list and install prerequisites
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common git

# Add Docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker’s official APT repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Update package list again and install Docker
sudo apt-get update
sudo apt-get install -y docker-ce

# Start Docker and enable it to start on boot
sudo systemctl start docker
sudo systemctl enable docker

# Verify Docker installation
sudo docker run hello-world

# Install Docker Compose
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -oP '(?<=tag_name": "v)[^"]*')
sudo curl -L "https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Apply executable permissions to the Docker Compose binary
sudo chmod +x /usr/local/bin/docker-compose

# Verify Docker Compose installation
if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose could not be installed"
    exit 1
else
    echo "Docker Compose installed successfully: $(docker-compose --version)"
fi

# Clone the GitHub repository
if [ ! -d "Valatility-Crypto-Gang" ]; then
    git clone https://github.com/valazeinali/Valatility-Crypto-Gang.git
fi
cd Valatility-Crypto-Gang

# Build and run the Docker container
sudo docker-compose build
sudo docker-compose up -d

