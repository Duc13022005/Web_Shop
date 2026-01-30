# Import database data using docker cp to avoid encoding issues
Write-Host "Importing database data from src/db/dump.sql..."

if (-not (Test-Path "src/db/dump.sql")) {
    Write-Error "File src/db/dump.sql does not exist!"
    exit 1
}

# 1. Copy file from host to container temp
docker cp src/db/dump.sql db:/tmp/dump.sql

# 2. Execute psql using the file inside container
docker exec db psql -U shop_user -d shop_db -f /tmp/dump.sql

# 3. Clean up
docker exec db rm /tmp/dump.sql

if ($?) {
    Write-Host "Import successful."
}
else {
    Write-Host "Import failed."
}
