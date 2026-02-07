#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="briefing-app"
CONTAINER_NAME="briefing-app"
PORT="${PORT:-5000}"

if ! docker info >/dev/null 2>&1; then
  echo "Docker não está disponível. Inicie o Docker e tente novamente." >&2
  exit 1
fi

docker build -t "$IMAGE_NAME" .

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
fi

docker run --name "$CONTAINER_NAME" \
  -p "${PORT}:5000" \
  -e SECRET_KEY="${SECRET_KEY:-dev-secret-key}" \
  -e ADMIN_USER="${ADMIN_USER:-}" \
  -e ADMIN_PASSWORD="${ADMIN_PASSWORD:-}" \
  "$IMAGE_NAME"
