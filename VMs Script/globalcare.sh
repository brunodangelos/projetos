#!/bin/bash

# Atualiza o sistema
sudo apt update

# Instala os pacotes necessários para adicionar um repositório HTTPS
sudo apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common nmap snmp -y

# Adiciona a chave GPG oficial do Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Adiciona o repositório do Docker ao APT sources
sudo add-apt-repository --yes "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Atualiza novamente o APT
sudo apt update

# Instala o Docker
sudo apt install docker-ce docker-ce-cli containerd.io -y

# Cria os diretórios /opt/globalcare, /opt/globalcare/docker e /opt/globalcare/scripts
sudo mkdir -p /opt/globalcare/docker
sudo mkdir -p /opt/globalcare/scripts

# Adiciona o usuário atual ao grupo docker para permitir o uso do Docker sem precisar de sudo
sudo usermod -aG docker $USER

# Reinicia o Docker para aplicar as alterações
sudo systemctl restart docker

