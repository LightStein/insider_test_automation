# Project Folder Structure

The following guide explains how to implement the Helm chart for deploying Selenium Test Controller and Chrome Node.

## Folder Structure:
```
selenium-helm-chart/
│
├── Chart.yaml                # Helm chart metadata
├── values.yaml               # Default values for the Helm chart
└── templates/                # Directory containing Kubernetes manifests
    ├── test-controller-deployment.yaml  # Deployment for Test Controller
    ├── chrome-node-deployment.yaml      # Deployment for Chrome Node
    └── chrome-node-service.yaml         # Service for Chrome Node
```

## Step-by-Step Guide

### 1. Set Up Folder Structure

- Create a root directory named `selenium-helm-chart/`.
- Create a file named `Chart.yaml` inside the root directory to define the Helm chart metadata.
- Create a file named `values.yaml` in the root directory to set default values.
- Create a folder named `templates/` inside the root directory, which will contain Kubernetes manifests.

### 2. Create Files

#### 2.1. Chart.yaml
Define the chart metadata:

```yaml
apiVersion: v2
name: selenium-tests-chart
description: A Helm chart for deploying Selenium Test Controller and Chrome Node
version: 0.1.0
type: application
```

#### 2.2. values.yaml
Define the values used by the Helm templates:

```yaml
testController:
  image: "your-dockerhub-user/test-controller:latest"

chromeNode:
  replicas: 3
```

#### 2.3. templates/test-controller-deployment.yaml
Define the deployment for the Test Controller:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-controller-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test-controller
  template:
    metadata:
      labels:
        app: test-controller
    spec:
      containers:
        - name: test-controller
          image: "{{ .Values.testController.image }}"
          env:
            - name: REMOTE_SELENIUM_URL
              value: "http://chrome-node-service:4444/wd/hub"
          ports:
            - containerPort: 8000
```

#### 2.4. templates/chrome-node-deployment.yaml
Define the deployment for Chrome Node:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chrome-node-deployment
spec:
  replicas: "{{ .Values.chromeNode.replicas }}"
  selector:
    matchLabels:
      app: chrome-node
  template:
    metadata:
      labels:
        app: chrome-node
    spec:
      containers:
        - name: chrome-node
          image: selenium/standalone-chrome:latest
          ports:
            - containerPort: 4444
```

#### 2.5. templates/chrome-node-service.yaml
Define the service for Chrome Node:

```yaml
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

## 3. Package and Deploy the Helm Chart

### 3.1. Package the Helm Chart
Use the following command to package the Helm chart:

```sh
helm package selenium-helm-chart
```

### 3.2. Install the Helm Chart
To install the Helm chart, use the command:

```sh
helm install selenium-tests selenium-helm-chart/
```
This command will deploy both the Test Controller Pod and Chrome Node Pod along with the necessary services.

### 3.3. Verify Deployments
To verify that the pods are running:

```sh
kubectl get pods
```
You should see two different deployments (`test-controller-deployment` and `chrome-node-deployment`) and the respective pods.

## 4. Updating the Deployment
If you need to update the Helm chart (e.g., change the number of replicas or update the image), edit the `values.yaml` file and use the following command:

```sh
helm upgrade selenium-tests selenium-helm-chart/
```
This command will apply the changes to the existing deployments.

### Notes
- Ensure you have Helm and `kubectl` installed and configured to communicate with your Kubernetes cluster.
- The Docker images (`your-dockerhub-user/test-controller:latest`) should be built and pushed to a container registry before deploying.
