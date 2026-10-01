param(
    [string]$Source = 'github profile.png'
)

# Make display-sized JPEG copies; keep the supplied source photo untouched.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$profileRoot = Split-Path -Parent $PSScriptRoot
$sourcePath = if ([IO.Path]::IsPathRooted($Source)) { $Source } else { Join-Path $profileRoot $Source }
$sourceImage = [Drawing.Image]::FromFile($sourcePath)
$jpegCodec = [Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() |
    Where-Object { $_.MimeType -eq 'image/jpeg' }

try {
    foreach ($variant in @(
        @{ Name = 'portrait-desktop.jpg'; Width = 640; Quality = 86 },
        @{ Name = 'portrait-mobile.jpg'; Width = 320; Quality = 84 }
    )) {
        $targetWidth = [Math]::Min($variant.Width, $sourceImage.Width)
        $targetHeight = [int][Math]::Round($sourceImage.Height * $targetWidth / $sourceImage.Width)
        $bitmap = New-Object Drawing.Bitmap($targetWidth, $targetHeight)
        $graphics = [Drawing.Graphics]::FromImage($bitmap)
        $parameters = New-Object Drawing.Imaging.EncoderParameters(1)
        try {
            $graphics.Clear([Drawing.Color]::FromArgb(8, 12, 18))
            $graphics.CompositingQuality = [Drawing.Drawing2D.CompositingQuality]::HighQuality
            $graphics.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $graphics.PixelOffsetMode = [Drawing.Drawing2D.PixelOffsetMode]::HighQuality
            $graphics.DrawImage($sourceImage, 0, 0, $targetWidth, $targetHeight)
            $parameters.Param[0] = New-Object Drawing.Imaging.EncoderParameter(
                [Drawing.Imaging.Encoder]::Quality, [long]$variant.Quality
            )
            $destination = Join-Path $profileRoot $variant.Name
            $bitmap.Save($destination, $jpegCodec, $parameters)
            Write-Output "$($variant.Name): $targetWidth x $targetHeight, $((Get-Item -LiteralPath $destination).Length) bytes"
        }
        finally {
            $parameters.Dispose()
            $graphics.Dispose()
            $bitmap.Dispose()
        }
    }
}
finally {
    $sourceImage.Dispose()
}
