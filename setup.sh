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
sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -oP '(?<=tag_name": "v)[^"]*')/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify Docker Compose installation
docker-compose --version

# Clone the GitHub repository
git clone https://github.com/valazeinali/Valatility-Crypto-Gang.git
cd Valatility-Crypto-Gang

# Build and run the Docker container
sudo docker-compose build
sudo docker-compose up -d
