; installer.iss
[Setup]
AppName=Snake Ultimate
AppVersion=1.0
DefaultDirName={pf}\SnakeUltimate
DefaultGroupName=SnakeUltimate
OutputDir=installer_build
OutputBaseFilename=SnakeUltimateInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\*"; DestDir: "{app}\assets"; Flags: recursesubdirs createallsubdirs
Source: "skins\*"; DestDir: "{app}\skins"; Flags: recursesubdirs createallsubdirs
Source: "musica\*"; DestDir: "{app}\musica"; Flags: recursesubdirs createallsubdirs
Source: "economia.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "tienda.py"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Snake Ultimate"; Filename: "{app}\main.exe"
Name: "{userdesktop}\Snake Ultimate"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Tasks]
Name: desktopicon; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Tareas opcionales"; Flags: unchecked
