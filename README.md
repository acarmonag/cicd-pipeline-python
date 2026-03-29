# CI/CD Pipeline — Python App on AWS ECS Fargate

A production-grade CI/CD pipeline built with GitHub Actions that deploys a containerized Python application to AWS ECS Fargate across two environments (staging and production), with automatic rollback on failure.

Infrastructure is fully defined as code using CloudFormation. The pipeline includes linting, unit tests with coverage, SonarCloud quality gate, acceptance tests against staging, smoke tests against production, and image promotion to a `:stable` tag on success.

---

## Pipeline overview

```
push to main
      │
      ▼
┌─────────────────────────────────────────────────────────┐
│ 1. deploy-cfn-base                                      │
│    Validate CloudFormation template                     │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│ 2. build-test-publish                                   │
│    Pylint + Flake8 → pytest + coverage → SonarCloud    │
│    Build Docker image → Push to ECR (:sha, :latest)    │
└──────┬────────────────────────────────────────────────--┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 3. deploy-cfn-staging                                   │
│    CloudFormation deploy → ECS cluster + ALB + task     │
│    Stack rollback guard (polls until stable/not found)  │
└──────┬──────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 4. update-service-staging                               │
│    Force new ECS deployment → wait for service stable  │
└──────┬──────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 5. test-staging                                         │
│    Run acceptance tests against staging ALB URL         │
└──────┬──────────────────────────────────────────────────┘
       │  only if staging tests pass
       ▼
┌─────────────────────────────────────────────────────────┐
│ 6. deploy-cfn-prod + update-service-prod                │
│    Same pattern as staging, targeting production stack  │
└──────┬──────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│ 7. smoke-test-prod                                      │
│    Run smoke tests against production ALB URL           │
│    On success → retag image as :stable in ECR           │
└──────┬──────────────────────────────────────────────────┘
       │  if smoke tests fail
       ▼
┌─────────────────────────────────────────────────────────┐
│ 8. rollback-on-failure                                  │
│    Force deploy :stable image → wait for stable         │
└─────────────────────────────────────────────────────────┘
```

---

## Infrastructure (CloudFormation — `template.yaml`)

Parameterized stack deployed independently per environment (`staging` / `production`):

| Resource | Details |
|---|---|
| `ECSCluster` | Fargate cluster per environment |
| `ECSTaskDefinition` | 0.25 vCPU / 0.5 GB, awsvpc networking, CloudWatch logs |
| `ECSService` | Rolling deploy (50% min healthy, 200% max) |
| `ApplicationLoadBalancer` | Internet-facing ALB |
| `ALBListener` | HTTP:80 → target group |
| `ECSTargetGroup` | IP-based, health check on `/health:8000` |
| `ALBSecurityGroup` | Allows HTTP:80 from internet |
| `ECSServiceSecurityGroup` | Allows :8000 from ALB SG only |
| `ECSLogGroup` | CloudWatch log group, 7-day retention |
| `ECRRepository` | Per-environment repo with scan-on-push |

Stack outputs (`ALBDnsName`, `ECSClusterName`, `ECSServiceName`, `ECRRepositoryUri`) are passed between jobs via GitHub Actions outputs.

---

## Test strategy

| Test type | File | When |
|---|---|---|
| Unit tests | `tests/test_calculadora.py`, `tests/test_app.py` | Before build — blocks image push on failure |
| Acceptance tests | `tests/test_acceptance_app.py` | Against live staging ALB — blocks prod deploy |
| Smoke tests | `tests/test_smoke_app.py` | Against live production ALB — triggers rollback on failure |

Coverage report uploaded as GitHub Actions artifact on every run.

---

## Code quality

- **Pylint** — enforces score ≥ 9.0
- **Flake8** — style linting
- **SonarCloud** — quality gate with coverage, duplication, and reliability checks (`sonar-project.properties`)

---

## Stack

`Python 3.12` `Flask` `Docker` `GitHub Actions` `AWS ECS Fargate` `AWS ALB` `AWS ECR` `AWS CloudFormation` `AWS CloudWatch` `SonarCloud` `pytest` `Pylint` `Flake8`

---

## Project structure

```
app/
  app.py                      # Flask application + /health endpoint
  calculadora.py              # Core logic
  templates/index.html        # UI
tests/
  test_calculadora.py         # Unit tests
  test_app.py                 # App-level unit tests
  test_acceptance_app.py      # Acceptance tests (runs against staging)
  test_smoke_app.py           # Smoke tests (runs against production)
.github/workflows/
  ci.yml                      # Full 8-job CI/CD pipeline
template.yaml                 # CloudFormation stack (ECS + ALB + ECR)
sonar-project.properties      # SonarCloud config
Dockerfile
requirements.txt
pytest.ini
```

---

## Required GitHub Secrets

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS credentials |
| `AWS_SECRET_ACCESS_KEY` | AWS credentials |
| `AWS_SESSION_TOKEN` | AWS session token (if using temporary credentials) |
| `SONAR_TOKEN` | SonarCloud authentication token |
| `LAB_ROLE_ARN` | ARN of the IAM role used by ECS tasks and execution |
| `VPC_ID` | Target VPC ID for deployment |
| `SUBNET_IDS` | Comma-separated public subnet IDs (min 2 AZs) |

---

## Key design decisions

**Stack rollback guard** — before each CloudFormation deploy, the pipeline polls the stack status and auto-deletes stacks stuck in `ROLLBACK_COMPLETE`, preventing deploy failures due to broken stack state.

**Image promotion** — images are tagged with the Git SHA on build. Only after smoke tests pass in production does the pipeline retag the image as `:stable`. This tag is the rollback target.

**Automatic rollback** — if smoke tests fail, the `rollback-on-failure` job forces a new ECS deployment using the last known `:stable` image, with `aws ecs wait services-stable` to confirm recovery.

**Environment parity** — staging and production use the same CloudFormation template parameterized by `EnvironmentName`, ensuring both environments are structurally identical.

---

## What I'd improve in a production setup

- Add approval gate between staging and production (GitHub Environments with required reviewers)
- Replace `sleep 30` before acceptance/smoke tests with active polling on ALB health
- Use OIDC-based AWS authentication instead of long-lived access keys in secrets
- Add CloudWatch alarms + SNS notifications on ECS service failures
- Enable blue/green deployments via CodeDeploy instead of rolling updates
