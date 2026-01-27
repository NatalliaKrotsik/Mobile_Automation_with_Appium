# load_env.ps1
Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*#') { return }  # skip comments
    $parts = $_ -split '=', 2
    if ($parts.Length -eq 2) {
        Set-Item -Path env:$($parts[0].Trim()) -Value $parts[1].Trim()
    }
}
