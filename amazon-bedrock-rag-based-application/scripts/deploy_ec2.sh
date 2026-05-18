#!/bin/bash
# ============================================================
# FILE: scripts/deploy_ec2.sh
# PURPOSE: Shell script to set up your EC2 server and deploy
#          the Streamlit app. Run these commands on the EC2 instance
#          after SSH-ing in.
#
# HOW TO USE:
# 1. SSH into EC2: ssh -i key.pem ec2-user@YOUR_IP
# 2. Run: bash deploy_ec2.sh
# ============================================================

# --- Update the server's package list ---
# yum = package manager on Amazon Linux (like pip but for the whole OS)
sudo yum update -y
# -y = automatically say "yes" to all prompts

# --- Install Python 3 and pip ---
sudo yum install python3 python3-pip git -y
# git = version control tool (to clone your code from GitHub)

# --- Install Python packages from requirements.txt ---
pip3 install -r requirements.txt

# --- (OPTIONAL) Clone your project from GitHub ---
# If your code is on GitHub, use this:
# git clone https://github.com/YOUR_USERNAME/enterprise-rag-system.git
# cd enterprise-rag-system

# --- Start the Streamlit app in the BACKGROUND ---
# nohup = "no hangup" — keeps the process running after you close SSH
# & = run in background (don't block the terminal)
# > logs/app.log = save all output to a log file (for debugging)
mkdir -p logs    # create logs folder if it doesn't exist
nohup streamlit run app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    > logs/app.log 2>&1 &
# 0.0.0.0 = listen on ALL network interfaces (required for EC2)
# 2>&1 = redirect error output to the same log file

# --- Print the public URL ---
echo "App is running!"
echo "Visit: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8501"
# curl -s ... = fetches the EC2 instance's public IP from AWS metadata service