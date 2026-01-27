# load_env.ps1
Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*#' -or $_ -match '^\s*$') { return }
    $parts = $_ -split '=', 2
    if ($parts.Length -eq 2) {
        $key = $parts[0].Trim()
        $value = $parts[1].Trim()
        Set-Item -Path "env:$key" -Value "$value"
    }
}

# Export ANDROID_SDK_ROOT for Node.js / Appium
if ($env:ANDROID_HOME -and -not $env:ANDROID_SDK_ROOT) {
    Set-Item -Path env:ANDROID_SDK_ROOT -Value "$env:ANDROID_HOME"
}
