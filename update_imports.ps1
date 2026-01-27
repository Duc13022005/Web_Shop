
$files = Get-ChildItem -Path 'd:\DNU\Web_Shop\src\backend' -Recurse -Filter *.py
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    if ($content -match 'from src\.') {
        $newContent = $content -replace 'from src\.', 'from '
        Set-Content -Path $file.FullName -Value $newContent
        Write-Host "Updated: $($file.Name)"
    }
}
