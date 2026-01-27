#!/bin/bash
set -e

echo "🔄 Waiting for PostgreSQL..."
until PGPASSWORD=${POSTGRES_PASSWORD:-password} psql -h db -U ${POSTGRES_USER:-user} -d ${POSTGRES_DB:-shop_db} -c '\q' 2>/dev/null; do
    echo "   PostgreSQL is unavailable - sleeping"
    sleep 2
done
echo "✅ PostgreSQL is ready!"

echo "🔄 Waiting for Redis..."
until redis-cli -h redis ping 2>/dev/null | grep -q PONG; do
    echo "   Redis is unavailable - sleeping"
    sleep 2
done
echo "✅ Redis is ready!"

echo "🔄 Running database migrations..."
alembic upgrade head || echo "⚠️ Migration skipped (tables may already exist)"

echo "✅ Starting server..."
exec "$@"
