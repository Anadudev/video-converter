# Video Converter Application

This repository contains the microservices for a distributed video-to-MP3 converter application. It is primarily built with Python and Flask, utilizing a microservices architecture designed to be deployed on Kubernetes.

## Architecture Overview

The system consists of the following components:

### 1. Gateway Service (`python/gateway`)
The API Gateway acts as the entry point for all client requests. It exposes public REST endpoints and orchestrates communication between the necessary internal services, message queues, and databases.

**Key Responsibilities:**
- Exposes public REST endpoints on `mp3converter.com`.
- **Authentication**: Proxies login requests to the Auth service.
- **Upload (`/upload`)**: Validates JWT tokens, saves uploaded video files into MongoDB (GridFS), and publishes a conversion task message to a RabbitMQ `video` queue.
- **Download (`/download`)**: Validates JWT tokens and allows authorized users to download stored files from MongoDB GridFS using file IDs.

**Tech Stack**: Python, Flask, PyMongo (GridFS), Pika (RabbitMQ client).

### 2. Auth Service (`python/auth`)
The Auth service handles user authentication and authorization using JSON Web Tokens (JWT). 

**Key Responsibilities:**
- **Login (`/login`)**: Validates user credentials against a MySQL database and issues short-lived JWTs.
- **Token Validation (`/validate`)**: Decodes and verifies the signatures of JWTs to ensure requests to the gateway are authorized.

**Tech Stack**: Python, Flask, Flask-MySQLdb, PyJWT.

### 3. Infrastructure & Dependencies
- **MySQL**: Relational database storing user credentials (schema defined in `python/auth/init.sql`).
- **MongoDB**: NoSQL document store utilizing GridFS for handling large file storage (both the original videos and converted MP3 files).
- **RabbitMQ**: Message broker used for asynchronous communication, receiving video conversion jobs from the gateway.
- **Kubernetes**: The primary deployment platform. Each service includes a `manifests/` directory containing necessary Deployment, Service, ConfigMap, Secret, and Ingress YAML definitions.

## Project Structure

```text
video-converter/
├── python/
│   ├── auth/
│   │   ├── manifests/        # Kubernetes manifests for the Auth service
│   │   ├── compose.yml       # Docker Compose for local MySQL testing
│   │   ├── init.sql          # MySQL database initialization script
│   │   ├── requirements.txt  # Python dependencies
│   │   ├── server.py         # Main Auth service application
│   │   └── Dockerfile
│   └── gateway/
│       ├── auth/             # Internal module for validating tokens
│       ├── auth_svc/         # Internal module for login proxy logic
│       ├── manifests/        # Kubernetes manifests (including Ingress)
│       ├── storage/          # GridFS & RabbitMQ storage utility logic
│       ├── requirements.txt  # Python dependencies
│       ├── server.py         # Main API Gateway application
│       └── Dockerfile
```

## Setup & Deployment

1. **Local Auth Database**: You can start the MySQL database locally using `docker-compose` from the `python/auth/` directory:
   ```bash
   cd python/auth
   docker-compose down
   docker-compose up -d
   ```

2. **Kubernetes Deployment**:
   The application is deployed using standard Kubernetes manifests. Execute the following commands against your cluster:
   ```bash
   kubectl apply -f python/auth/manifests/
   kubectl apply -f python/gateway/manifests/
   ```

   **Ingress Setup**: The gateway relies on an Ingress controller configured for the host `mp3converter.com`. To test locally (e.g., using Minikube), you will need to update your local hosts file (`C:\Windows\System32\drivers\etc\hosts`) to point `mp3converter.com` to your Minikube IP.
