# Export database data only (no schema if possible, or full dump if needed, but user asked for data)
# --data-only --column-inserts ensures we just get the data, assuming schema is created by alembic or init.sql
Write-Host "Exporting database data to src/db/dump.sql..."
docker exec shop_db pg_dump -U shop_user -d shop_db --data-only --column-inserts > src/db/dump.sql
if ($?) {
    Write-Host "Export successful: src/db/dump.sql"
}
else {
    Write-Host "Export failed. Make sure Docker is running and the container 'shop_db' is active."
}
