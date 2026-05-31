#!/bin/sh
set -e

if [ -n "$POSTGRES_HOST" ]; then
  echo "Esperando a PostgreSQL..."
  until python - <<'EOF'
import os
import socket
import sys

host = os.environ.get("POSTGRES_HOST", "db")
port = int(os.environ.get("POSTGRES_PORT", "5432"))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((host, port))
except OSError:
    sys.exit(1)
finally:
    sock.close()
sys.exit(0)
EOF
  do
    echo "PostgreSQL no disponible, reintentando..."
    sleep 2
  done
  echo "PostgreSQL listo."
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn core.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers "${GUNICORN_WORKERS:-2}" \
  --timeout "${GUNICORN_TIMEOUT:-60}"
