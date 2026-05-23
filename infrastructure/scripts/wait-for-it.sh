#!/bin/sh
# wait-for-it.sh: simple script to wait for a service to be ready

host="$1"
shift
cmd="$@"

until nc -z "$host" 2>/dev/null; do
  echo "▶ Ожидание доступности $host..."
  sleep 1
done

echo "✅ Сервис $host доступен!"
exec $cmd
