# Export database data using docker cp to avoid encoding issues
Write-Host "Exporting database data to src/db/dump.sql..."

# 1. Dump to a temp file inside the container (Linux handles UTF-8 natively)
docker exec db pg_dump -U shop_user -d shop_db --data-only --column-inserts -f /tmp/dump.sql

# 2. Copy the file from container to host
docker cp db:/tmp/dump.sql src/db/dump.sql

# 3. Clean up temp file inside container
docker exec db rm /tmp/dump.sql

if ($?) {
    Write-Host "Export successful: src/db/dump.sql"
}
else {
    Write-Host "Export failed. Make sure Docker is running and the container 'db' is active."
}
