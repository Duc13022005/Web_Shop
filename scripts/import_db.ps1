# Import database data
Write-Host "Importing database data from src/db/dump.sql..."

if (-not (Test-Path "src/db/dump.sql")) {
    Write-Error "File src/db/dump.sql does not exist!"
    exit 1
}

# Clear existing data might be risky, but 'init.sql' creates schema. 
# Usually we append? Or truncate?
# For now, we assume a fresh DB or the user wants to populate data.
# Note: Foreign key constraints might cause issues if we don't truncate in order.
# A safer way requires -c (clean) in pg_dump, but we used --data-only.

Get-Content src/db/dump.sql | docker exec -i shop_db psql -U shop_user -d shop_db

if ($?) {
    Write-Host "Import successful."
}
else {
    Write-Host "Import failed."
}
