Microservices-Based Video-to-Audio Converter Project
Project Overview
This project is a distributed system built for learning purposes, deployed on a local machine using Docker and Kubernetes (Minikube). It consists of four microservices, each designed to perform specific tasks:

Gateway Service
Authentication Service
Converter Service
Notification Service
Each service is containerized into Docker images, published to Docker Hub, and deployed in a Minikube Kubernetes cluster. The system enables users to convert video files into audio files and incorporates robust error handling and logging mechanisms to ensure smooth operation.

Program Flow
User Login

The user sends a request to the /login endpoint.
The request is routed to the Gateway Service, which forwards it to the Authentication Service.
The Authentication Service validates the user, signs a JWT token, and returns it to the Gateway Service.
File Upload

The user uploads a video file to the /upload endpoint.
The Gateway Service validates the JWT token, uploads the video to MongoDB, and publishes a message with the file ID to the RabbitMQ video queue.
Video-to-Audio Conversion

The Converter Service consumes messages from the RabbitMQ video queue.
It fetches the video from MongoDB, converts it to MP3 using the MoviePy library, and uploads the audio file to the MongoDB MP3 database.
Notification Service

The Notification Service consumes messages from the RabbitMQ mp3 queue and sends an email with the MP3 file details to the user.
Audio Download

The user can download the audio by sending a request to the /download endpoint with the MP3 file ID.
Technologies and Tools Used
Docker: Containerized each service into Docker images.
Kubernetes (Minikube): Orchestrated the deployment of microservices in a local cluster.
RabbitMQ: Used as a message broker for communication between services.
MongoDB: Stored video and audio files in separate databases.
Python Libraries:
Pika: To interact with RabbitMQ.
MoviePy: To convert video files into MP3 format.
Tempfile: For creating temporary files during the conversion.
Smtplib and EmailMessage: For sending email notifications.
JWT: For secure authentication and token validation.
Prerequisites
Before running this project on your machine, make sure the following software is installed:

Minikube v1.34.0: Minikube installation guide
Docker Desktop: Docker installation guide
Kubernetes (kubectl): Kubectl installation guide
K9s (optional for monitoring pods/logs via terminal): K9s installation guide
Python 3.x: Python installation guide
Pip (Python package manager): Install Pip via Python: python -m ensurepip --upgrade
MongoDB: MongoDB installation guide
SQL Database: MySQL or any SQL-compatible database (e.g., PostgreSQL).
Getting Started
1. Clone the Repository
Clone this repository to your local machine:

bash
Copy code
git clone https://github.com/yourusername/video-to-audio-converter.git
cd video-to-audio-converter
2. Set Up Dependencies
Ensure that Docker, Kubernetes, and other tools are installed on your machine. Then, install the required Python libraries:

bash
Copy code
pip install -r requirements.txt
3. Set Up the Local Kubernetes Cluster (Minikube)
Start Minikube and enable the Kubernetes cluster:

bash
Copy code
minikube start --kubernetes-version=v1.34.0
4. Docker Setup
Build and push the Docker images to your Docker Hub account:

bash
Copy code
docker build -t yourdockerhubusername/gateway-service .
docker build -t yourdockerhubusername/auth-service .
docker build -t yourdockerhubusername/convert-service .
docker build -t yourdockerhubusername/notification-service .
docker push yourdockerhubusername/gateway-service
docker push yourdockerhubusername/auth-service
docker push yourdockerhubusername/convert-service
docker push yourdockerhubusername/notification-service
Make sure you replace yourdockerhubusername with your actual Docker Hub username.

5. Kubernetes Configuration
Deploy the services to the Minikube Kubernetes cluster:

bash
Copy code
kubectl apply -f k8s/
This will deploy all your services based on the configuration files (such as deployment.yaml and service.yaml) in the k8s/ directory.

6. Expose Services with Ingress
Create an Ingress to expose your Gateway Service on a custom domain (e.g., mp3Converter.com):

bash
Copy code
kubectl apply -f k8s/ingress.yaml
Make sure to update the Ingress configuration with your desired domain and port.

7. Verify Services
To verify that everything is running correctly, use kubectl and K9s (optional):

bash
Copy code
kubectl get pods
kubectl get services
Or, use K9s for a terminal-based UI to monitor your Kubernetes cluster:

bash
Copy code
k9s
8. Interact with the Application
Login: Use /login endpoint to authenticate and receive a JWT token.
Upload Video: Use /upload endpoint to upload a video file.
Convert Video: The system will automatically convert the video to audio.
Download Audio: Use /download endpoint to download the converted MP3 audio file.
9. Error Handling and Logs
If you need to troubleshoot, you can check the logs of any pod using:

bash
Copy code
kubectl logs <pod-name>
Or use K9s to view logs interactively.

Notes
Ensure that the correct versions of Minikube, Docker, and Kubernetes are used as per the prerequisites.
MongoDB should be configured with appropriate databases (video and mp3) for storing video and audio files.
JWT authentication is implemented for secure access to the endpoints.
Conclusion
This project is a great example of using a microservices architecture to build a video-to-audio conversion system. It leverages various modern technologies such as Docker, Kubernetes, RabbitMQ, and Python libraries to provide an efficient, scalable, and distributed solution
