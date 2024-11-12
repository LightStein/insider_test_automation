# TestOps Selenium Test Automation System

## Overview of the System

This system is designed for the automated testing of the Insider website using Selenium WebDriver in Python. The project is containerized and orchestrated via Kubernetes, making it scalable and portable for both local and cloud-based environments. The architecture is composed of:

1. **Test Controller Pod**: Responsible for running the Selenium test cases. This pod uses pytest to execute test cases defined in the `/tests` directory.
2. **Chrome Node Pod**: Runs Selenium WebDriver in a headless Chrome browser, executing commands received from the Test Controller Pod.
3. **Inter-Pod Communication**: The Test Controller Pod sends Selenium commands to the Chrome Node Pod via HTTP requests, enabling remote testing in a Kubernetes cluster.
4. **Persistent S3 Storage**: Test results are saved locally and then uploaded to AWS S3 for permanent storage.

The solution is designed to automatically scale the Chrome Node Pod according to load, using Kubernetes deployments with configurable replica counts.

## Deployment Instructions

### Local Deployment

### Prerequisites

- Docker installed on your local machine.
- Python 3.9 installed.
- Kubernetes Minikube or Docker Desktop Kubernetes for running the local cluster.

### Steps

1. **Clone the Repository**:
    
    ```
    git clone https://github.com/LightStein/insider_test_automation.git
    cd insider_test_automation
    ```
    
2. **Build the Docker Image**:
    
    ```
    docker build -t selenium-test-runner:latest .
    ```
    
3. **Deploy Kubernetes Resources**: Ensure that Kubernetes is up and running (via Minikube):
    
    ```
    python3 deploy_script.py
    ```
    
4. **Verify the Deployment**:
Use the following command to check if the pods are running successfully:
    
    ```
    kubectl get pods
    ```
    
5. **Run Tests**:
Tests will automatically be triggered upon deployment of the Test Controller Pod. Logs of the execution can be accessed using:
    
    ```
    kubectl logs <test-controller-pod-name>
    ```
    

### AWS EKS Deployment

### Prerequisites

- AWS CLI configured with credentials.
- AWS EKS cluster set up.
- kubectl and eksctl installed on your EC2 instance.

### Steps

1. **Create an EKS Cluster**:
Use `eksctl` to create an EKS cluster:
    
    ```bash
    eksctl create cluster --name selenium-cluster --version 1.21 --region us-east-1 --nodegroup-name selenium-nodes --node-type t2.micro --nodes 2
    ```
    
2. **Build and Push Docker Image to Docker Hub**:
Build the Docker image and push it to Docker Hub:
    
    ```bash
    docker build -t nautilus444/test-controller:latest .
    docker push nautilus444/test-controller:latest
    ```
    
3. **Deploy Kubernetes Resources**: Automatically applies the Kubernetes YAML files to the EKS cluster:
    
    ```bash
    python3 deploy_script.py
    ```
    
4. **Verify Deployment and Execute Tests**:
Use `kubectl get pods` to ensure all pods are running, then monitor the logs:
    
    ```bash
    kubectl logs <test-controller-pod-name>
    ```
    
5. **Access Test Results**:
Test results are uploaded to an S3 bucket defined in the configuration. Check the bucket for the results after execution.

## Inter-Pod Communication Explanation

The TestOps system leverages Kubernetes services to establish communication between the Test Controller Pod and the Chrome Node Pod. The Chrome Node Pod hosts a Selenium server that listens for commands sent by the Test Controller Pod.

- **Service Discovery**: Kubernetes services expose the Chrome Node Pod via a DNS address (`chrome-node-service:4444`), making it accessible from within the Kubernetes cluster.
    
    ```yaml
    # Source: selenium-tests-chart/templates/chrome-node-service.yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: chrome-node-service
    spec:
      selector:
        app: chrome-node
      ports:
        - protocol: TCP
          port: 4444
          targetPort: 4444
      type: ClusterIP
    ```
    
- **Communication Flow**: The Test Controller Pod sends commands to the Chrome Node Pod over HTTP using the WebDriver protocol. The Chrome Node Pod executes these commands in a headless Chrome browser and returns the responses to the Test Controller Pod.
- **Scaling**: The system is designed to handle multiple Chrome Node Pods (from 1 to 5 replicas). The Test Controller can distribute the Selenium tests across available Chrome Node Pods, enhancing parallel execution and reducing test run times.