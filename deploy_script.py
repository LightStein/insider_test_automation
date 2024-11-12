import subprocess

def deploy_kubernetes_resources():
    # Apply Helm Chart
    subprocess.run(["helm", "upgrade", "--install", "selenium-tests", "./selenium-helm-chart"], check=True)

def main():
    try:
        deploy_kubernetes_resources()
        print("Kubernetes resources deployed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during deployment: {e}")

if __name__ == "__main__":
    main()
