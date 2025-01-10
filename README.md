# Microservices-Based Video-to-Audio Converter Project

## Project Overview

This project is a distributed system built for learning purposes, deployed on a local machine using Docker and Kubernetes (Minikube). It consists of four microservices, each designed to perform specific tasks:

1. **Gateway Service**
2. **Authentication Service**
3. **Converter Service**
4. **Notification Service**

Each service is containerized into Docker images, published to Docker Hub, and deployed in a Minikube Kubernetes cluster. The system enables users to convert video files into audio files and incorporates robust error handling and logging mechanisms to ensure smooth operation.

## Program Flow

### 1. User Login
- The user sends a request to the `/login` endpoint.
- The request is routed to the Gateway Service, which forwards it to the Authentication Service.
- The Authentication Service validates the user, signs a JWT token, and returns it to the Gateway Service.

### 2. File Upload
- The user uploads a video file to the `/upload` endpoint.
- The Gateway Service validates the JWT token, uploads the video to MongoDB, and publishes a message with the file ID to the RabbitMQ video queue.

### 3. Video-to-Audio Conversion
- The Converter Service consumes messages from the RabbitMQ video queue.
- It fetches the video from MongoDB, converts it to MP3 using the MoviePy library, and uploads the audio file to the MongoDB MP3 database.

### 4. Notification Service
- The Notification Service consumes messages from the RabbitMQ mp3 queue and sends an email with the MP3 file details to the user.

### 5. Audio Download
- The user can download the audio by sending a request to the `/download` endpoint with the MP3 file ID.

## Technologies and Tools Used

1. **Docker**: Containerized each service into Docker images.
2. **Kubernetes (Minikube)**: Orchestrated the deployment of microservices in a local cluster.
3. **RabbitMQ**: Used as a message broker for communication between services.
4. **MongoDB**: Stored video and audio files in separate databases.
5. **Python Libraries**:
    - **Pika**: To interact with RabbitMQ.
    - **MoviePy**: To convert video files into MP3 format.
    - **Tempfile**: For creating temporary files during the conversion.
    - **Smtplib and EmailMessage**: For sending email notifications.
6. **JWT**: For secure authentication and token validation.

## Prerequisites

Before running this project on your machine, make sure the following software is installed:

1. **Minikube v1.34.0**: [Minikube installation guide](https://minikube.sigs.k8s.io/docs/)
2. **Docker Desktop**: [Docker installation guide](https://www.docker.com/products/docker-desktop)
3. **Kubernetes (kubectl)**: [Kubectl installation guide](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
4. **K9s** (optional for monitoring pods/logs via terminal): [K9s installation guide](https://k9scli.io/)
5. **Python 3.x**: [Python installation guide](https://www.python.org/downloads/)
6. **Pip (Python package manager)**: Install Pip via Python: `python -m ensurepip --upgrade`
7. **MongoDB**: [MongoDB installation guide](https://www.mongodb.com/try/download/community)
8. **SQL Database**: MySQL or any SQL-compatible database (e.g., PostgreSQL).

## Getting Started

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/video-to-audio-converter.git
cd video-to-audio-converter

This project is a great example of using a microservices architecture to build a video-to-audio conversion system. It leverages various modern technologies such as Docker, Kubernetes, RabbitMQ, and Python libraries to provide an efficient, scalable, and distributed solution.

