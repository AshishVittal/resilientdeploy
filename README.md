# ResilientDeploy 🚀

**An AWS-based CI/CD pipeline with Docker, automated testing, security scanning, health checks, and rollback for failed deployments.**

## 📌 Project Overview

ResilientDeploy automates the process of testing, packaging, and deploying a Python FastAPI application to an AWS EC2 instance.

The project demonstrates how DevOps practices can reduce manual deployment work and improve recovery when a new application release fails its health check.

The deployment pipeline uses GitHub Actions to run automated tests, build a Docker image, scan it for known vulnerabilities, push the image to Amazon Elastic Container Registry (ECR), and deploy it to EC2 through AWS Systems Manager (SSM).

A rollback mechanism attempts to restore the previously running image if the new deployment fails its health check.

## 🎯 Problem Statement

Manual deployments can be time-consuming and error-prone. A newly deployed application may also start incorrectly or fail its health check, potentially interrupting service.

ResilientDeploy addresses these challenges by automating deployment steps and testing a recovery mechanism that attempts to restore the previous application version when a deployment fails.

## 🏗️ Architecture

```text
Developer pushes code to GitHub
              |
              v
       GitHub Actions
              |
       +------+------+
       |      |      |
     Tests  Docker  Trivy
       |    Build   Scan
       +------+------+
              |
              v
       AWS Authentication
       GitHub OIDC + IAM
              |
              v
        Amazon ECR
       Store Docker Image
              |
              v
       AWS Systems Manager
          Run Command
              |
              v
          Amazon EC2
        Ubuntu + Docker
              |
              v
       Start New Container
              |
              v
        Health Check
          /       \
       Pass       Fail
        |           |
     Success    Attempt Rollback
                    |
                    v
           Check Previous Version
```

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application programming language |
| FastAPI | REST API framework |
| Docker | Containerization |
| Git and GitHub | Source control |
| GitHub Actions | CI/CD automation |
| pytest | Automated application tests |
| Trivy | Container vulnerability scanning |
| AWS IAM and OIDC | Secure authentication and permissions |
| Amazon ECR | Docker image registry |
| Amazon EC2 | Application hosting |
| AWS Systems Manager (SSM) | Remote deployment command execution |
| Ubuntu Linux | Server operating system |
| Bash | Deployment and rollback scripting |

## ⚙️ CI/CD Pipeline

The GitHub Actions workflow automates the following stages:

1. **Checkout:** Retrieves the source code from the repository.
2. **Testing:** Installs development dependencies and runs pytest.
3. **Docker build:** Builds a container image for the application.
4. **Security scanning:** Uses Trivy to identify known vulnerabilities in the image.
5. **AWS authentication:** Uses GitHub OIDC to obtain temporary AWS credentials through an IAM role.
6. **Image publishing:** Pushes the Docker image to Amazon ECR, tagged with the Git commit SHA.
7. **Deployment:** Uses AWS Systems Manager Run Command to execute a deployment script on EC2.
8. **Health verification:** Checks the application's `/health` endpoint.
9. **Rollback attempt:** If the new deployment fails its health check, attempts to restore the previous image and verify its health.

The deployment steps are configured for pushes to `main` and manual workflow runs on `main`. Pull requests run the configured CI checks without deploying the application.

## 🔄 Rollback Mechanism

Before replacing the running container, the deployment script records the image reference used by the existing container and pulls the new image.

After starting the new container, it checks the application's health endpoint.

If the health check fails, the script attempts to:

- Collect diagnostic logs from the failed container.
- Remove the failed container.
- Start a container using the previously recorded image.
- Check whether the restored application is healthy.

The manual `rollback_test` workflow input deliberately uses an invalid health-check path to simulate a failed deployment.

**Verification:** The rollback test completed successfully, reporting that the previous application was restored and healthy. The EC2 container was subsequently observed running, and the health endpoint returned HTTP 200.

> This is a single-instance deployment with a possible interruption during container replacement. Rollback is best-effort recovery, not a guarantee of zero downtime.

## 🔐 Security Practices

- Uses GitHub OIDC with AWS IAM roles instead of relying on long-lived AWS access keys in GitHub.
- Uses IAM permissions to control access to AWS services.
- Scans the Docker image using Trivy for known vulnerabilities.
- Uses commit-SHA image tags to improve release traceability.
- Keeps application deployment commands within the AWS Systems Manager workflow.

**Security-scan limitation:** The current Trivy configuration reports matching CRITICAL and HIGH findings but uses `exit-code: '0'`. Therefore, those findings do not automatically fail the workflow. The scan is a visibility measure, not yet an enforced vulnerability gate.

## 🧪 Application Endpoints

| Endpoint | Description |
|---|---|
| `/` | Returns application information |
| `/health` | Returns application health and version |
| `/version` | Returns the application version |

Example health response:

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

## 📚 Key Learnings

Through this project, I practised:

- Building and testing a Python API.
- Creating and running Docker images and containers.
- Writing a GitHub Actions CI/CD workflow.
- Using GitHub OIDC and AWS IAM roles for authentication.
- Publishing Docker images to Amazon ECR.
- Deploying applications to EC2 through AWS Systems Manager.
- Writing Bash deployment scripts with health checks and rollback logic.
- Testing a simulated deployment failure and verifying recovery.
- Understanding the difference between successful deployment, health verification, and rollback recovery.

## 🚀 Future Improvements

- Enforce a defined security-vulnerability policy in CI.
- Improve deployment diagnostics, alerting, and monitoring.
- Add more robust recovery handling for edge cases.
- Explore a multi-instance architecture with a load balancer to reduce deployment interruptions.
- Add infrastructure provisioning using Terraform.
- Improve automated integration and deployment tests.

## 👨‍💻 Author

**Ashish Vittal**

GitHub: [AshishVittal](https://github.com/AshishVittal)

---

*ResilientDeploy is a hands-on DevOps learning project demonstrating CI/CD automation, containerization, AWS deployment, security scanning, and deployment recovery.*
