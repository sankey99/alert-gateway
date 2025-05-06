## Overview
Alert Gateway is a Python-based FastAPI application that acts as a proxy for sending alerts via Twilio. It allows you to send SMS messages to predefined subscribers using Twilio's messaging service.

## Features
- Exposes a FastAPI endpoint (`/alert`) to send SMS alerts.
- Uses Twilio for SMS delivery.
- Subscriber information and Twilio credentials are managed via environment variables.
- Automatically restarts the container on failure using Docker Compose.

## Prerequisites
- Python 3.8 or higher
- Docker and Docker Compose
- Twilio account with valid credentials

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a `.env` file in the project root with the following variables:
   ```dotenv
   TWILIO_ACCOUNT_SID=<your-twilio-account-sid>
   TWILIO_AUTH_TOKEN=<your-twilio-auth-token>
   TWILIO_FROM=<your-twilio-phone-number>
   SUBSCRIPTIONS={"<subscriber-id>": {"from": "<from-phone>", "to": "<to-phone>"}}
   ```

3. Install dependencies (if running locally):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running with Docker
1. Build and start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. The application will be available at `http://localhost:8000`.

### Sending Alerts
- Send a POST request to the `/alert` endpoint with the following JSON payload:
  ```json
  {
    "id": "<subscriber-id>",
    "message": "<your-alert-message>"
  }
  ```

- Example using `curl`:
  ```bash
  curl -X POST http://localhost:8000/alert \
       -H "Content-Type: application/json" \
       -d '{"id": "db45c8f1-d06f-45a4-97de-c5521ddf9151", "message": "Test alert"}'
  ```

## Project Structure
- `main.py`: Contains the FastAPI application logic.
- `docker-compose.yml`: Docker Compose configuration for containerized deployment.
- `requirements.txt`: Python dependencies.
- `.env`: Environment variables for Twilio credentials and subscriptions.

## Environment Variables
- `TWILIO_ACCOUNT_SID`: Your Twilio account SID.
- `TWILIO_AUTH_TOKEN`: Your Twilio authentication token.
- `TWILIO_FROM`: The Twilio phone number used to send messages.
- `SUBSCRIPTIONS`: A JSON object mapping subscriber IDs to their phone numbers.

## Dependencies
- `fastapi`: Web framework for building APIs.
- `uvicorn`: ASGI server for running FastAPI.
- `httpx`: HTTP client for making requests (optional).
- `twilio`: Twilio SDK for sending SMS.
- `python-dotenv`: For loading environment variables from `.env`.

## Deployment with Fly.io

### Prerequisites
- Install the Fly.io CLI: [Fly.io CLI Installation Guide](https://fly.io/docs/hands-on/install-flyctl/)
- Create a Fly.io account: [Sign Up for Fly.io](https://fly.io/)
- Ensure you have Docker installed and running.

### Steps to Deploy
 Run the script:
 ```bash
   flyctl auth login
  chmod   +x deploy.sh
  ./deploy.sh
   ```

## Fly.io Commands

```bash
### Authentication
flyctl auth login
# List all your Fly.io apps
flyctl apps list

# Create a new app
flyctl apps create <app-name>

# Destroy an app
flyctl destroy <app-name>

# List all secrets for an app
flyctl secrets list

# Set or update a secret
flyctl secrets set <KEY>=<VALUE>

# Remove a secret
flyctl secrets unset <KEY>
# View app logs
flyctl logs

# Check app status
flyctl status
# Scale the app (e.g., set the number of instances)
flyctl scale count <number>

# Set app memory size
flyctl scale memory <size-in-mb>
# Open a shell to the app's instance
flyctl ssh console

# List allocated IP addresses
flyctl ips list

# Allocate a new IP address
flyctl ips allocate
# Restart the app
flyctl apps restart <app-name>

# Validate the fly.toml configuration file
flyctl config validate

# Check Fly.io CLI version
flyctl version
```

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.