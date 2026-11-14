# MLflow + PostgreSQL Engineering Lab

A local Docker Compose reference stack for experiment tracking.

## Prerequisites
- Docker Engine / Docker Desktop with Compose v2
- Python 3.10–3.12 for the sample experiment

## Start
1. Copy \`.env.example\` to \`.env\` and set a non-default local password.
2. Run \`docker compose up -d --build\`.
3. Wait until \`docker compose ps\` shows PostgreSQL healthy and MLflow running.
4. Open http://localhost:5000.

The service is bound to 127.0.0.1. PostgreSQL is not published to the host.

## Log a sample experiment
\`\`\`bash
python -m venv .venv
# Activate the virtual environment, then:
pip install -r requirements.txt
python experiment.py
\`\`\`

The script creates a synthetic regression dataset, trains three Ridge models and logs parameters, metrics and model artifacts to MLflow.

## Persistence
- \`postgres_data\`: MLflow backend metadata.
- \`mlflow_artifacts\`: run and model artifacts.

Back up and restore both volumes as a coordinated operation. For production, use managed PostgreSQL or a separately operated database, object storage for artifacts, TLS, authentication, authorization, secret management, network isolation, monitoring and tested recovery.

## Useful commands
\`\`\`bash
docker compose ps
docker compose logs -f mlflow
docker compose logs -f postgres
docker compose down
# Preserve data volumes:
docker compose down
# Destructive reset (removes DB and artifacts):
docker compose down -v
\`\`\`

## Scope
This is a learning lab, not a production-ready ML platform. The synthetic dataset is only for validating the tracking workflow.
