[Setup]
AppName=YouTube Downloader
AppVersion=1.0
DefaultDirName={pf}\YouTube Downloader
DefaultGroupName=YouTube Downloader
OutputDir=dist
OutputBaseFilename=YouTubeDownloaderInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\app.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\YouTube Downloader"; Filename: "{app}\app.exe"
Name: "{userdesktop}\YouTube Downloader"; Filename: "{app}\app.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear ícono en el escritorio"; GroupDescription: "Opciones adicionales:"
