#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define variables
APP_NAME="alert-gateway"  # Replace with your Fly.io app name
REGION="yyz"             # Replace with your preferred Fly.io region

# Load environment variables from .env file
if [ -f ".env" ]; then
  source .env
else
  echo "Error: .env file not found!"
  exit 1
fi

# Escape the JSON string for SUBSCRIPTIONS
ESCAPED_SUBSCRIPTIONS=$(echo "$SUBSCRIPTIONS" | sed 's/"/\\"/g')

# Authenticate with Fly.io
flyctl auth login

# Initialize Fly.io app if not already initialized
if [ ! -f "fly.toml" ]; then
  flyctl launch --name "$APP_NAME" --region "$REGION" --no-deploy
fi

# Set environment variables
flyctl secrets set TWILIO_ACCOUNT_SID="$TWILIO_ACCOUNT_SID" \
                  TWILIO_AUTH_TOKEN="$TWILIO_AUTH_TOKEN" \
                  SUBSCRIPTIONS="$ESCAPED_SUBSCRIPTIONS"

# Deploy the application
flyctl deploy

# Output the application URL
flyctl info | grep "Hostname" | awk '{print $2}'