# Observability (Loki, Promtail, Prometheus, Grafana)

This guide explains how to run, use, and extend the logging and metrics stack bundled with this project.

- Logs: Promtail collects Docker/container logs and ships them to Loki
- Metrics: Prometheus scrapes targets and stores time series
- Dashboards: Grafana visualizes logs and metrics

## Ports
- Loki: 3100
- Promtail: 9080 (internal HTTP)
- Prometheus: 9090
- Grafana: 3000 (default admin/admin)

## File layout
- monitoring/loki/config.yml: Loki configuration
- monitoring/promtail/config.yml: Promtail configuration
- monitoring/prometheus/prometheus.yml: Prometheus scrape config
- monitoring/grafana/provisioning/datasources/*.yml: Pre-provisioned data sources
- monitoring/grafana/provisioning/dashboards/json/*.json: Pre-provisioned dashboards

## Quickstart (local)
`
docker compose -f docker-compose.yaml -f docker-compose.local.yml up -d loki promtail prometheus grafana
`
Open:
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090
- Loki readiness: http://localhost:3100/ready

## Production quickstart
`
cp .env.example .env  # set real credentials

docker compose -f docker-compose.yaml -f docker-compose.prod.yml up -d loki promtail prometheus grafana
`

## Log queries (Grafana Explore Loki)
- All container logs: {job=" docker-logs\}
- Only bot service logs: {job=\docker-logs\, service=\bot\}
- Only stderr: {job=\docker-logs\, stream=\stderr\}
- Text search: {job=\docker-logs\} |= \ERROR\

## Metrics (Prometheus)
Prometheus scrapes itself and the bot service (at /metrics on port 8080). Add more jobs in monitoring/prometheus/prometheus.yml if needed.

Useful pages:
- Targets: http://localhost:9090/targets
- Graph: http://localhost:9090/graph

## Security & hardening
- Change Grafana admin password via env vars or UI
- Restrict published ports in production (use reverse proxy)
- Consider authentication in front of Prometheus/Loki in production

## Troubleshooting
- Promtail logs: docker compose logs -f promtail
- Loki readiness: curl http://localhost:3100/ready
- Grafana data sources: UI -> Configuration -> Data sources
- Prometheus targets: http://localhost:9090/targets

## Extending
- Add Alertmanager for alerting
- Add more dashboards by dropping JSON files into monitoring/grafana/provisioning/dashboards/json/
- Add more Prometheus scrape jobs (Kubernetes SD, EC2 SD, etc.)
