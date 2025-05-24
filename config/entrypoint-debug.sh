#!/bin/bash
echo "=== DEBUG ==="
echo "DB_HOST: $DB_HOST"
echo "DB_PORT: $DB_PORT"
echo "DB_NAME: $DB_NAME"
echo "DB_USER: $DB_USER"
echo "=== PING TEST ==="
timeout 5 bash -c "echo -n '' > /dev/tcp/$DB_HOST/$DB_PORT" && echo "SUCCESS" || echo "FAILED"
echo "=== WAIT A BIT ==="
sleep infinity