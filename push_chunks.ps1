$files = git ls-files --others --exclude-standard
$modified = git ls-files --modified
$allFiles = $files + $modified | Select-Object -Unique

$chunkSize = 0
$maxChunk = 10MB
$commitCount = 1

foreach ($file in $allFiles) {
    if (-not (Test-Path $file)) { continue }
    git add $file
    $size = (Get-Item $file).Length
    $chunkSize += $size
    
    if ($chunkSize -gt $maxChunk) {
        git commit -m "Upload chunk $commitCount"
        $pushResult = git push origin main 2>&1
        Write-Host "Pushed chunk $commitCount. Result: $pushResult"
        $chunkSize = 0
        $commitCount++
    }
}

$status = git status --porcelain
if ($status) {
    git commit -m "Upload final chunk"
    $pushResult = git push origin main 2>&1
    Write-Host "Pushed final chunk. Result: $pushResult"
}
